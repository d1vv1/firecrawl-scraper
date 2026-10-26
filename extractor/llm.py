"""LLM access: Microsoft Foundry through its OpenAI-compatible endpoint.

Uses structured outputs (`chat.completions.parse` with a pydantic model). If the
deployment doesn't support them we stop; we never fall back to parsing free text.
"""

import base64
import logging
from functools import lru_cache
from typing import TypeVar

import openai
from openai import OpenAI
from pydantic import BaseModel
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import PROMPTS_DIR, ConfigError, load_settings

log = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class StructuredOutputsUnsupportedError(RuntimeError):
    pass


class LLMRefusalError(RuntimeError):
    pass


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def model_name() -> str | None:
    s = load_settings()
    return s.vertex_model if s.llm_provider == "vertex" else s.foundry_deployment


@lru_cache(maxsize=1)
def _client() -> tuple[OpenAI, str]:
    s = load_settings()
    if s.llm_provider == "vertex":
        return _vertex_client(s)
    if s.llm_provider != "foundry":
        raise ConfigError(f"LLM_PROVIDER must be 'foundry' or 'vertex', not {s.llm_provider!r}")
    s.require("foundry_endpoint", "foundry_deployment")
    return OpenAI(base_url=s.foundry_endpoint, api_key=s.foundry_api_key or _entra_token_provider(),
                  max_retries=0, timeout=180), s.foundry_deployment


def _entra_token_provider():
    """No FOUNDRY_API_KEY: sign in with Microsoft Entra ID instead. Needed when the
    resource has key login switched off (keys then vanish from the portal and any key
    gets 401). Uses `az login`, VS Code or environment credentials (`az` is slow to
    start on Windows, hence the 60s process timeout); the token is
    refreshed automatically. Your account needs the "Azure AI User" (or "Cognitive
    Services OpenAI User") role on the resource."""
    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    except ImportError as e:
        raise ConfigError("FOUNDRY_API_KEY is empty, so Entra ID sign-in is used: "
                          "pip install azure-identity") from e
    log.info("No FOUNDRY_API_KEY: using Microsoft Entra ID sign-in (az login)")
    return get_bearer_token_provider(DefaultAzureCredential(exclude_interactive_browser_credential=True,
                                                            process_timeout=60),
                                     "https://cognitiveservices.azure.com/.default")


def _vertex_client(s) -> tuple[OpenAI, str]:
    """Google Vertex AI (Gemini) through its OpenAI-compatible endpoint. Signs in with
    Application Default Credentials (`gcloud auth application-default login`, or a
    service-account key file in GOOGLE_APPLICATION_CREDENTIALS); tokens last an hour
    and are refreshed here before they expire."""
    s.require("vertex_project")
    try:
        import google.auth
        import google.auth.transport.requests
    except ImportError as e:
        raise ConfigError("LLM_PROVIDER=vertex needs: pip install google-auth requests") from e
    try:
        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    except google.auth.exceptions.DefaultCredentialsError as e:
        raise ConfigError("No Google sign-in found: run `gcloud auth application-default login`") from e
    request = google.auth.transport.requests.Request()

    def token() -> str:
        if not creds.valid:
            creds.refresh(request)
        return creds.token

    host = ("aiplatform.googleapis.com" if s.vertex_location == "global"
            else f"{s.vertex_location}-aiplatform.googleapis.com")
    base = (f"https://{host}/v1/projects/{s.vertex_project}/locations/"
            f"{s.vertex_location}/endpoints/openapi")
    log.info("LLM: Vertex AI %s (%s)", s.vertex_model, s.vertex_location)
    return OpenAI(base_url=base, api_key=token, max_retries=0, timeout=180), s.vertex_model


_no_temperature: set[str] = set()   # deployments that rejected temperature=0


def _user_content(user_prompt: str, images: list[bytes] | None):
    """The user message: text, followed by PNG images (pages of a PDF) if any."""
    if not images:
        return user_prompt
    return [{"type": "text", "text": user_prompt}] + [
        {"type": "image_url",
         "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()}}
        for png in images]


def _parse(client: OpenAI, deployment: str, system_prompt: str, user_prompt: str,
           schema: type[T], images: list[bytes] | None = None):
    """temperature=0 for repeatable extractions. Some models (reasoning models)
    reject the parameter; then we retry once without it and remember that."""
    kwargs = dict(model=deployment, response_format=schema,
                  messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": _user_content(user_prompt, images)}])
    if deployment not in _no_temperature:
        try:
            return client.chat.completions.parse(temperature=0, **kwargs)
        except openai.BadRequestError as e:
            if "temperature" not in str(e).lower():
                raise
            log.info("Deployment %s doesn't accept temperature; retrying without", deployment)
            _no_temperature.add(deployment)
    return client.chat.completions.parse(**kwargs)


_backoff = wait_exponential(multiplier=2, min=5, max=65)
RATE_LIMIT_MIN_WAIT_S = 15


def _wait(retry_state) -> float:
    """Use the server's Retry-After on 429s (Foundry token-per-minute limits reset
    within 60s), else exponential backoff."""
    exc = retry_state.outcome.exception()
    headers = getattr(getattr(exc, "response", None), "headers", None) or {}
    for name in ("retry-after-ms", "retry-after"):
        value = headers.get(name)
        if value:
            try:
                seconds = float(value) / (1000 if name.endswith("ms") else 1)
                # With parallel workers the per-minute token budget is shared: the
                # server's 1-2s hint just loses the race again (Merck, 3 workers).
                floor = RATE_LIMIT_MIN_WAIT_S * retry_state.attempt_number
                return min(max(seconds + 1.0, floor), 90.0)
            except ValueError:
                pass
    return _backoff(retry_state)


def _log_retry(retry_state) -> None:
    exc = retry_state.outcome.exception()
    log.warning("LLM call failed (%s); retry %d in %.0fs", type(exc).__name__,
                retry_state.attempt_number, retry_state.next_action.sleep)


@retry(retry=retry_if_exception_type((openai.RateLimitError, openai.APIConnectionError,
                                      openai.APITimeoutError, openai.InternalServerError)),
       stop=stop_after_attempt(8), wait=_wait, before_sleep=_log_retry, reraise=True)
def call_llm(system_prompt: str, user_prompt: str, schema: type[T],
             images: list[bytes] | None = None) -> T:
    """`images`: PNG pages shown to the model next to the text (pay tables)."""
    client, deployment = _client()
    try:
        completion = _parse(client, deployment, system_prompt, user_prompt, schema, images)
    except openai.BadRequestError as e:
        msg = str(e).lower()
        if any(k in msg for k in ("response_format", "json_schema", "structured output")):
            raise StructuredOutputsUnsupportedError(
                f"Deployment {deployment!r} rejected structured outputs (json_schema "
                f"response_format). Use a model that supports them (e.g. gpt-4o / "
                f"gpt-4.1 / gpt-5 family). Original error: {e}") from e
        raise

    usage = completion.usage
    if usage:
        log.info("LLM %s: %d prompt + %d completion tokens", schema.__name__,
                 usage.prompt_tokens, usage.completion_tokens)
    message = completion.choices[0].message
    if message.refusal:
        raise LLMRefusalError(f"Model refused: {message.refusal}")
    if message.parsed is None:
        raise StructuredOutputsUnsupportedError(
            f"No parsed output returned (finish_reason={completion.choices[0].finish_reason}).")
    return message.parsed
