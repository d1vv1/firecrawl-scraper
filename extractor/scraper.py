"""Step 4: download the report and turn it into page-tagged markdown.

PDFs are downloaded directly and converted locally with pymupdf4llm (Firecrawl
PDF parsing costs ~1 credit per page). Only HTML reports go through Firecrawl.
"""

import hashlib
import logging
import re
from dataclasses import dataclass
from pathlib import Path

import httpx
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from .config import CACHE_DIR, MIN_CHARS_PER_PAGE
from .firecrawl_client import FirecrawlClient

# An HTML annual report is long; anything shorter is a listing/teaser page.
MIN_HTML_REPORT_CHARS = 20_000

log = logging.getLogger(__name__)

BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"),
    "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}
TIMEOUT_S = 60
_PAGE_MARKER = "<!-- page {n} -->"
_PAGE_MARKER_RE = re.compile(r"^<!-- page (\d+) -->$", re.M)


class DownloadError(RuntimeError):
    pass


class NeedsOCRError(RuntimeError):
    pass


class TeaserPageError(DownloadError):
    """A short HTML page about the report rather than the report; .markdown holds its
    text so the caller can follow its links (no second scrape)."""

    def __init__(self, message: str, markdown: str):
        super().__init__(message)
        self.markdown = markdown


@dataclass
class Page:
    number: int
    text: str


@dataclass
class ReportDocument:
    source_url: str
    kind: str                 # "pdf" or "html"
    pages: list[Page]
    markdown_path: Path
    pdf_path: Path | None
    from_cache: bool


def cache_stem(slug: str, url: str) -> str:
    return f"{slug}_{hashlib.sha1(url.encode()).hexdigest()}"


def looks_like_pdf(content: bytes, content_type: str | None) -> bool:
    if content[:1024].lstrip().startswith(b"%PDF"):
        return True
    ct = (content_type or "").lower()
    return "application/pdf" in ct and not content.lstrip()[:1] == b"<"


# --- markdown cache format: one file with page markers -------------------------

def pages_to_markdown(pages: list[Page]) -> str:
    return "\n\n".join(f"{_PAGE_MARKER.format(n=p.number)}\n{p.text}" for p in pages)


def markdown_to_pages(md: str) -> list[Page]:
    parts = _PAGE_MARKER_RE.split(md)
    if len(parts) == 1:
        return [Page(1, md)]
    return [Page(int(parts[i]), parts[i + 1].strip("\n"))
            for i in range(1, len(parts) - 1, 2)]


# --- download -----------------------------------------------------------------

@retry(retry=retry_if_exception_type(httpx.TransportError),
       stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20), reraise=True)
def _httpx_get(url: str) -> tuple[int, str | None, bytes]:
    with httpx.Client(headers=BROWSER_HEADERS, follow_redirects=True,
                      timeout=TIMEOUT_S, http2=True) as client:
        r = client.get(url)
        return r.status_code, r.headers.get("content-type"), r.content


def _impersonated_get(url: str) -> tuple[int, str | None, bytes]:
    """Some CDNs (e.g. Akamai on unilever.com) block on the TLS fingerprint, so a
    browser User-Agent isn't enough. curl_cffi presents a real Chrome handshake."""
    from curl_cffi import requests as cffi
    r = cffi.get(url, impersonate="chrome", timeout=TIMEOUT_S, allow_redirects=True)
    return r.status_code, r.headers.get("content-type"), r.content


def download(url: str) -> tuple[bytes, str | None]:
    """Return (body, content_type). Tries plain httpx, then a Chrome-impersonating
    client if the response is blocked or isn't a PDF."""
    try:
        status, ct, body = _httpx_get(url)
    except (httpx.ConnectError, httpx.RemoteProtocolError, httpx.ReadError) as e:
        # e.g. CERTIFICATE_VERIFY_FAILED: the server sends an incomplete certificate
        # chain that browsers repair but httpx doesn't. Try the browser-like client.
        log.info("GET %s failed with httpx (%s); trying curl_cffi", url, str(e)[:120])
        status, ct, body = 0, None, b""
    else:
        log.info("GET %s -> %s %s, %d bytes (httpx)", url, status, ct, len(body))
    if status == 200 and looks_like_pdf(body, ct):
        return body, ct
    if status in (0, 401, 403, 429) or (status == 200 and url.lower().endswith(".pdf")):
        try:
            status, ct, body = _impersonated_get(url)
            log.info("GET %s -> %s %s, %d bytes (curl_cffi)", url, status, ct, len(body))
        except ImportError:
            log.warning("curl_cffi not installed; cannot retry with browser TLS fingerprint")
    if status != 200:
        raise DownloadError(f"Download failed: HTTP {status} for {url}")
    return body, ct


# --- conversion ---------------------------------------------------------------

def pdf_to_pages(pdf_path: Path) -> list[Page]:
    import pymupdf
    import pymupdf4llm

    doc = pymupdf.open(pdf_path)
    log.info("Converting %d-page PDF to markdown locally (this can take a few minutes)",
             doc.page_count)
    try:
        chunks = pymupdf4llm.to_markdown(doc, page_chunks=True, use_ocr=False,
                                         show_progress=False)
    except TypeError:  # legacy (non-layout) engine has no use_ocr option
        chunks = pymupdf4llm.to_markdown(doc, page_chunks=True, show_progress=False)
    pages = []
    for i, ch in enumerate(chunks):
        meta = ch.get("metadata", {})
        number = meta.get("page_number") or meta.get("page") or i + 1
        pages.append(Page(int(number), ch.get("text", "")))
    return pages


def check_not_scanned(pages: list[Page]) -> None:
    chars = sum(len(p.text.strip()) for p in pages)
    per_page = chars / max(len(pages), 1)
    if per_page < MIN_CHARS_PER_PAGE:
        raise NeedsOCRError(
            f"Only {per_page:.0f} characters of text per page on average "
            f"(< {MIN_CHARS_PER_PAGE}). The PDF is probably scanned and needs OCR, "
            f"which is out of scope.")


def fetch_report(report_url: str, slug: str, fc: FirecrawlClient,
                 use_cache: bool = True) -> ReportDocument:
    CACHE_DIR.mkdir(exist_ok=True)
    stem = cache_stem(slug, report_url)
    pdf_path = CACHE_DIR / f"{stem}.pdf"
    md_path = CACHE_DIR / f"{stem}.md"

    if use_cache and md_path.exists():
        log.info("Using cached markdown %s", md_path.name)
        pages = markdown_to_pages(md_path.read_text(encoding="utf-8"))
        kind = "pdf" if pdf_path.exists() else "html"
        return ReportDocument(report_url, kind, pages, md_path,
                              pdf_path if kind == "pdf" else None, True)

    if use_cache and pdf_path.exists():
        log.info("Using cached PDF %s", pdf_path.name)
        body, ct = pdf_path.read_bytes(), "application/pdf"
    else:
        body, ct = download(report_url)

    if looks_like_pdf(body, ct):
        pdf_path.write_bytes(body)
        pages = pdf_to_pages(pdf_path)
        check_not_scanned(pages)
        kind = "pdf"
    elif report_url.lower().split("?")[0].endswith(".pdf"):
        snippet = body[:200].decode("utf-8", "replace").replace("\n", " ")
        raise DownloadError(
            f"Expected a PDF from {report_url} but got {ct!r} "
            f"(probably a cookie/login/blocked page): {snippet!r}")
    else:
        log.info("Report is an HTML page; scraping it with Firecrawl (1 credit)")
        md = fc.scrape(report_url, formats=["markdown"])["markdown"]
        pages = [Page(1, md)]
        kind, pdf_path = "html", None
        if len(md.strip()) < MIN_HTML_REPORT_CHARS:
            raise TeaserPageError(
                f"{report_url} has only {len(md.strip()):,} characters of text: a listing or "
                f"teaser page, not an annual report. Pass --report-url with the report PDF.", md)

    md_path.write_text(pages_to_markdown(pages), encoding="utf-8")
    log.info("Saved %d page(s) of markdown to %s", len(pages), md_path.name)
    return ReportDocument(report_url, kind, pages, md_path, pdf_path, False)
