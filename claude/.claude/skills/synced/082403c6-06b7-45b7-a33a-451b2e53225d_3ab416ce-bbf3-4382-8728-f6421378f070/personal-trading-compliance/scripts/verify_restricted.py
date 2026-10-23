"""
verify_restricted.py — confirm an rlst-check hit is the SAME issuer, not a loose ticker match.

Why this exists: rlst-check matches loosely. A short ticker like "NU" (Nu Holdings) can come back
restricted=true because "NU" appears *inside* a related field of a DIFFERENT company (e.g. "INUV" /
Inuvo Inc). Treating that as a violation would wrongly accuse the employee. So before any
restricted=true becomes PROHIBITED_RESTRICTED, confirm identity.

Identity is decided ONLY on positive evidence — we never infer from fuzzy/substring similarity,
which is the very bug we're guarding against:
  1. exact ticker match                      -> genuine
  2. both CIKs known:  equal -> genuine       ;  different -> false_positive   (CIK is authoritative)
  3. exact normalized company-name match     -> genuine
  4. anything else                           -> unverified  (escalate to NEEDS_REVIEW)

CIK is the right key. Seed references/ticker_cik.json and refresh it from SEC's
https://www.sec.gov/files/company_tickers.json (ticker->cik_str) or the edgar MCP. Without a CIK
for one side we deliberately fall through to 'unverified' rather than guess.

Returns ('genuine' | 'false_positive' | 'unverified', reason).
"""
from __future__ import annotations
import re, json, sys

_STOP = re.compile(r"\b(INC|CORP|CORPORATION|CO|LTD|LIMITED|PLC|LLC|LP|CLASS [A-Z]|COMMON|STOCK|"
                   r"SHARES|HOLDINGS|HOLDING|GROUP|THE|SA|NV|AG|ADR|ORD|USD)\b")


def _norm_name(s: str) -> str:
    s = _STOP.sub(" ", (s or "").upper())
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _cik(t, cik_map):
    v = cik_map.get((t or "").upper())
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def verify(queried_ticker, security_name, primary_ticker, company_name, cik_map=None):
    cik_map = cik_map or {}
    qt = (queried_ticker or "").upper().strip()
    pt = (primary_ticker or "").upper().strip()

    # 1. exact ticker
    if qt and pt and qt == pt:
        return ("genuine", f"exact ticker match ({qt})")

    # 2. CIK — authoritative, both sides required
    qc, pc = _cik(qt, cik_map), _cik(pt, cik_map)
    if qc and pc:
        return ("genuine", f"same CIK ({qc})") if qc == pc else \
               ("false_positive", f"different issuer by CIK (traded {qt}={qc} vs restricted {pt}={pc})")

    # 3. exact normalized company name (NOT substring — substring is the bug we're avoiding)
    qn, pn = _norm_name(security_name), _norm_name(company_name)
    if qn and pn and qn == pn:
        return ("genuine", f"company name matches ('{company_name}')")

    # 4. cannot positively confirm either way -> escalate
    miss = qt if not qc else pt
    return ("unverified",
            f"cannot confirm identity: rlst matched '{company_name or '?'}' ({pt or '?'}) vs traded "
            f"'{security_name or '?'}' ({qt}); no CIK cached for {miss}. Add its CIK to ticker_cik.json "
            f"or escalate to NEEDS_REVIEW.")


if __name__ == "__main__":
    # CLI: verify_restricted.py QUERIED_TICKER "security name" PRIMARY_TICKER "company name" [cik_map.json]
    cm = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
    decision, reason = verify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], cm)
    print(json.dumps({"decision": decision, "reason": reason}, indent=2))
