"""Company name folding and slugs of the CDP report bucket (ported unchanged from the
GCS storage kit, cdp_bucket/slug.py), so a company is matched to its bucket folder by
the same rules that named it."""

import hashlib
import re
import unicodedata

# Letters NFKD does not decompose into ASCII on its own.
_SPECIAL = {"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "ß": "ss", "đ": "d", "Đ": "d",
            "ł": "l", "Ł": "l", "þ": "th", "Þ": "th", "ð": "d", "Ð": "d", "ı": "i", "œ": "oe", "Œ": "oe"}

# Legal-form and share-class words dropped from slugs. Matched as whole words
# after folding to lowercase ASCII with punctuation turned into spaces.
LEGAL_SUFFIXES = [
    "publ", "ab", "a s", "as", "asa", "aps", "oyj", "oy", "abp", "hf", "plc", "ltd", "limited",
    "ag", "se", "sa", "s a", "nv", "n v", "bv", "b v", "inc", "corp", "corporation", "co",
    "llc", "lp", "gmbh", "kgaa", "kg", "spa", "s p a", "srl", "sgps", "socimi", "sicav",
    "o n", "na", "vz", "vzo", "st", "inh", "pref", "class a", "class b", "ser a", "ser b",
]
_SUFFIX_RE = re.compile(r"\b(?:" + "|".join(sorted((re.escape(s) for s in LEGAL_SUFFIXES),
                                                    key=len, reverse=True)) + r")\b")
# A trailing single share-class letter ("SEB A", "Sagax D", "Besqab Pref B").
_TRAILING_CLASS_RE = re.compile(r"(?:\s+[a-dr])+$")   # A/B/C/D shares, Finnish R shares

MAX_SLUG = 60


def ascii_fold(text: str) -> str:
    text = "".join(_SPECIAL.get(ch, ch) for ch in (text or ""))
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def _words(text: str) -> str:
    s = ascii_fold(text).lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_legal(text: str) -> str:
    """Lowercase ASCII words with legal forms and share-class markers removed."""
    s = _words(text)
    prev = None
    while prev != s:               # "AB (publ)" etc. may need two passes
        prev = s
        s = re.sub(r"\s+", " ", _SUFFIX_RE.sub(" ", s)).strip()
        s = _TRAILING_CLASS_RE.sub("", s).strip()
    return s or _words(text)


def slugify(name: str, max_len: int = MAX_SLUG) -> str:
    """Company folder slug: ASCII, lowercase, hyphens, legal suffixes dropped, <= max_len."""
    s = strip_legal(name).replace(" ", "-")
    if len(s) > max_len:
        cut = s[:max_len + 1]
        s = cut.rsplit("-", 1)[0] if "-" in cut[:max_len] else s[:max_len]
    s = s.strip("-")
    if not s:
        raise ValueError(f"empty slug for {name!r}")
    return s


def placeholder_id(isin: str | None, country: str, name: str) -> str:
    """Stable stand-in for a missing CDP company id: 'tmp' + 8 hex characters.

    Keyed on the ISIN when there is one, otherwise on country + normalised name,
    so rebuilding gives the same folder.
    """
    key = (isin or "").strip().upper() or f"{country.upper()}|{strip_legal(name)}"
    return "tmp" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]


def is_placeholder_id(company_id: str) -> bool:
    return bool(re.fullmatch(r"tmp[0-9a-f]{8}", company_id or ""))
