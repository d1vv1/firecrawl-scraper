"""Settings from .env, project paths, and name helpers (step 1)."""

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# The scraper version stamped on every value when a company is extracted (column
# scraper_version). Raise it by one whenever a change means a re-run would give other
# values: prompts, sources, how reports are found or read, the fields asked for. Not for
# changes applied to saved results when the CSV is written (refresh, repair_quotes): those
# reach old values without a re-run. Values saved before versioning read "0".
# `python -m extractor.datapoints ... --outdated` re-runs the companies below this version.
# 1: 10 Nov 2026, the first versioned extraction (after Wave 1).
SCRAPER_VERSION = 1

# Tunables. Kept here so a later batch runner can override them in one place.
WORD_BUDGET_PER_GROUP = 6_000
CHUNK_WORDS = 1_500
CHUNK_OVERLAP_WORDS = 150
WEBSITE_MIN_SCORE = 0.5
MIN_CHARS_PER_PAGE = 200
SEARCH_LIMIT = 10
MAP_LIMIT = 500

# Legal-form suffixes removed when building the "clean" name used for matching.
LEGAL_SUFFIXES = {
    "plc", "ltd", "limited", "ag", "se", "sa", "nv", "inc", "incorporated",
    "gmbh", "corp", "corporation", "co", "company", "llc", "bv", "spa", "sas",
    "ab", "asa", "oyj", "as", "kgaa", "holding", "holdings",
    # Nordic
    "aktiebolag", "aktiebolaget", "publ", "abp", "oy", "aps", "hf", "ehf", "aktieselskab",
}


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    firecrawl_api_key: str | None
    foundry_endpoint: str | None
    foundry_api_key: str | None
    foundry_deployment: str | None
    llm_provider: str = "foundry"            # "foundry" or "vertex"
    vertex_project: str | None = None
    vertex_location: str = "global"
    vertex_model: str = "google/gemini-2.5-flash"

    def require(self, *names: str) -> None:
        missing = [n.upper() for n in names if not getattr(self, n)]
        if missing:
            raise ConfigError(
                f"Missing setting(s): {', '.join(missing)}. "
                f"Copy .env.example to .env and fill them in.")


def load_settings() -> Settings:
    # override=True: .env is re-read for each company, so a key changed mid-run (a new
    # Firecrawl key when credits run out) is used from the next company on.
    load_dotenv(PROJECT_ROOT / ".env", override=True)
    return Settings(
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY") or None,
        foundry_endpoint=os.getenv("FOUNDRY_ENDPOINT") or None,
        foundry_api_key=os.getenv("FOUNDRY_API_KEY") or None,
        foundry_deployment=os.getenv("FOUNDRY_DEPLOYMENT") or None,
        llm_provider=(os.getenv("LLM_PROVIDER") or "foundry").strip().lower(),
        vertex_project=os.getenv("VERTEX_PROJECT") or None,
        vertex_location=os.getenv("VERTEX_LOCATION") or "global",
        vertex_model=os.getenv("VERTEX_MODEL") or "google/gemini-2.5-flash",
    )


def clean_name(legal_name: str) -> str:
    """Lowercase, drop punctuation and legal suffixes: 'Unilever PLC' -> 'unilever'."""
    # Light fold (Ørsted -> orsted) without collapsing "aa": domains keep "aarhus".
    text = fold(legal_name, collapse_digraphs=False).replace("&", " and ").replace("a/s", " as ")
    text = re.sub(r"(?<=\b[a-z])\.(?=[a-z]\b)", "", text)  # n.v. -> nv., s.a. -> sa.
    tokens = re.findall(r"[a-z0-9]+", text)
    kept = [t for t in tokens if t not in LEGAL_SUFFIXES]
    return " ".join(kept or tokens)


# A share class or listing line after the company's name in a listing ("SCA A",
# "Besqab Pref B", "Corem Property D", "Alvotech SDB", "BayWa AG na o.N."): not part of
# the name a register, Wikidata or a web search knows the company by.
_SHARE_CLASS = re.compile(
    r"\s+(?:pref(?:erence)?(?:\s+[a-d])?|(?:ser(?:ies)?|class)\.?\s*[a-d]|sdb"
    r"|(?:vink\.?\s*)?na\s+o\.?\s*n\.?|o\.?\s*n\.?|[a-d]"
    # German listing lines (DACH): "Porsche AG VZO", "BMW AG ST", "Rheinmetall AG INH",
    # "Sixt SE VZO O.N.", "Henkel AG&CO.KGAA VZO", "DRAEGERWERK ST.A.O.N.", "BAYWA AG VINK.NA.",
    # a nominal value ("PROCREDIT HOLDING AG NA EO 5", "STABILUS SE INH. EO-,01")
    r"|vzo|vz|st|stamm|inh(?:\.?\s*on)?|vna|vink\.?\s*na|namens?(?:aktien)?|st\.?\s*a\.?(?:\s*o\.?\s*n)?"
    r"|(?:eo|sf|chf|dl)\s*-?\s*,?\s*\d+(?:[.,]\d+)?)\.?\s*$"
    # joined to the name by a dot: "MUENCH.RUECKVERSICHERUNGS GESELLSCHAFT.VNA"
    r"|\.(?:vna|vzo|inh|na)\.?\s*$", re.I)


def without_share_class(name: str) -> str:
    """'SCA A' -> 'SCA', 'Besqab Pref B' -> 'Besqab', 'BayWa AG na o.N.' -> 'BayWa AG'."""
    while True:
        short = _SHARE_CLASS.sub("", name).strip()
        # "NA" (registered shares) right after the legal form: "DT.TELEKOM AG NA"
        short = re.sub(r"(\b(?:ag|se|kgaa|a-sp|sa|nv)\.?)\s+na\.?$", r"\1", short, flags=re.I)
        if short == name or not short:
            return name
        name = short


def slugify(legal_name: str) -> str:
    """'Unilever PLC' -> 'unilever-plc' (used for cache and output file names)."""
    return re.sub(r"[^a-z0-9]+", "-", fold(legal_name, collapse_digraphs=False)).strip("-")


def fold(text: str, collapse_digraphs: bool = True) -> str:
    """Lowercase ASCII without diacritics, and with the common transliterations
    collapsed, so 'Årsrapport' / 'arsrapport' / 'aarsrapport' and
    'Geschäftsbericht' / 'geschaeftsbericht' compare equal."""
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.translate(str.maketrans({"ø": "o", "æ": "ae", "ß": "ss", "ð": "d", "þ": "th", "œ": "oe"}))
    if collapse_digraphs:
        for digraph, single in (("aa", "a"), ("ae", "a"), ("oe", "o"), ("ue", "u")):
            t = t.replace(digraph, single)
    return t
