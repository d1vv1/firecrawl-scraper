"""Euro reference rates from the European Central Bank, for the market-cap band.

The ECB publishes a rate per working day (units of a currency per 1 EUR), free and
without a key. A year-end date that is a holiday takes the last rate before it. Rates
are cached in cache/ecb_rates.json, so each (currency, date) is asked for once.
"""

import csv
import datetime as dt
import io
import json
import logging

import httpx

from .config import CACHE_DIR

log = logging.getLogger(__name__)

URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.{cur}.EUR.SP00.A"
CACHE = CACHE_DIR / "ecb_rates.json"
SOURCE = "ECB euro reference rates"


def eur_rate(currency: str, date: str) -> tuple[float, str] | None:
    """(units of currency per EUR, the rate's date) on the last ECB working day on or
    before date (YYYY-MM-DD); None when the ECB has no rate or can't be reached."""
    currency = currency.upper()
    if currency == "EUR":
        return 1.0, date
    try:
        day = dt.date.fromisoformat(date[:10])
    except ValueError:
        return None
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    key = f"{currency}/{day}"
    if key not in cache:
        start = (day - dt.timedelta(days=10)).isoformat()
        try:
            r = httpx.get(URL.format(cur=currency), timeout=30,
                          params={"startPeriod": start, "endPeriod": day.isoformat(), "format": "csvdata"})
            if r.status_code != 404:        # 404: the ECB has no rate for this currency (kept)
                r.raise_for_status()
        except httpx.HTTPError as e:
            log.warning("ECB rate %s on %s: %s", currency, day, e)
            return None
        obs = sorted((x["TIME_PERIOD"], float(x["OBS_VALUE"])) for x in csv.DictReader(io.StringIO(r.text))
                     if x.get("OBS_VALUE"))
        cache[key] = [obs[-1][1], obs[-1][0]] if obs else None
        CACHE_DIR.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    hit = cache[key]
    return (hit[0], hit[1]) if hit else None
