"""Thin wrapper around the Firecrawl v2 SDK (firecrawl-py 4.x: `Firecrawl`,
`.search()`, `.map()`, `.scrape()`).

The client is created lazily, so a fully cached run never touches Firecrawl.
Every call is counted so we can report estimated credits per run.
"""

import logging
import math
from dataclasses import dataclass, field

import httpx
from firecrawl import Firecrawl
from firecrawl import InternalServerError, RateLimitError, RequestTimeoutError
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import Settings

log = logging.getLogger(__name__)

_RETRYABLE = (RateLimitError, InternalServerError, RequestTimeoutError,
              httpx.TransportError)
_retry = retry(
    retry=retry_if_exception_type(_RETRYABLE),
    stop=stop_after_attempt(6),            # rate limits clear within a minute or two
    wait=wait_exponential(multiplier=3, min=5, max=90),
    reraise=True,
)


class CreditBudgetExceeded(RuntimeError):
    """The per-company Firecrawl credit cap would be exceeded by the next call."""


@dataclass
class CreditMeter:
    """Estimated credits: search 2 per 10 results, map 1 per call, scrape 1 per page."""
    calls: list[tuple[str, str, int]] = field(default_factory=list)

    def add(self, kind: str, target: str, credits: int) -> None:
        self.calls.append((kind, target, credits))
        log.info("Firecrawl %s (%s): ~%d credit(s)", kind, target, credits)

    @property
    def total(self) -> int:
        return sum(c for _, _, c in self.calls)


class FirecrawlClient:
    def __init__(self, settings: Settings, max_credits: int | None = None):
        """max_credits: per-company cap; a call that would exceed it raises
        CreditBudgetExceeded instead of spending."""
        self._settings = settings
        self._app: Firecrawl | None = None
        self.credits = CreditMeter()
        self.max_credits = max_credits

    def _afford(self, kind: str, cost: int) -> None:
        if self.max_credits is not None and self.credits.total + cost > self.max_credits:
            raise CreditBudgetExceeded(
                f"Per-company cap of {self.max_credits} Firecrawl credits reached "
                f"({self.credits.total} spent; {kind} would cost {cost})")

    @property
    def app(self) -> Firecrawl:
        if self._app is None:
            self._settings.require("firecrawl_api_key")
            # We do our own retries with tenacity.
            self._app = Firecrawl(api_key=self._settings.firecrawl_api_key, max_retries=0)
        return self._app

    @_retry
    def search(self, query: str, limit: int) -> list[dict]:
        self._afford("search", 2 * math.ceil(limit / 10))
        data = self.app.search(query, limit=limit)
        self.credits.add("search", query, 2 * math.ceil(limit / 10))
        return [_as_link(r) for r in (data.web or [])]

    @_retry
    def map(self, url: str, search: str | None, limit: int) -> list[dict]:
        self._afford("map", 1)
        data = self.app.map(url, search=search, limit=limit, include_subdomains=True)
        self.credits.add("map", f"{url} search={search!r}", 1)
        return [_as_link(r) for r in (data.links or [])]

    @_retry
    def scrape(self, url: str, formats: list[str]) -> dict:
        self._afford("scrape", 1)
        doc = self.app.scrape(url, formats=formats, only_main_content=False)
        self.credits.add("scrape", url, 1)
        return {"markdown": doc.markdown or "", "links": list(doc.links or [])}


def _as_link(item) -> dict:
    """Search/map items are SearchResultWeb, Document or plain str depending on options."""
    if isinstance(item, str):
        return {"url": item, "title": None, "description": None}
    if getattr(item, "url", None):
        return {"url": item.url, "title": getattr(item, "title", None),
                "description": getattr(item, "description", None)}
    meta = getattr(item, "metadata", None)
    return {"url": getattr(meta, "source_url", None) or getattr(meta, "url", None),
            "title": getattr(meta, "title", None),
            "description": getattr(meta, "description", None)}
