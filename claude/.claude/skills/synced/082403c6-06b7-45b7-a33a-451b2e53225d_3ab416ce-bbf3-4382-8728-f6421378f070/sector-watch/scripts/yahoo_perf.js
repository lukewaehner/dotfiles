// sector-watch — Yahoo Finance perf snippet (HARDENED v2)
// Validated May 26, 2026 — 18/18 stress-test pass including:
//   AAPL, NVDA, MSFT          (mega-caps, splits, dividends)
//   CRCL, KDK, RDDT           (recent IPOs / partial 1Y)
//   BRK-B, BRK.B, BF.B        (class-share dot->dash auto-normalize)
//   ^GSPC, ^IXIC              (indices with caret)
//   SPY, IBIT                 (ETFs)
//   ASML, BABA                (foreign ADRs)
//   BTC-USD                   (crypto, weekend trading)
//   ZZZZZZZ, TSLAA            (bad symbols, cleanly fail)
//
// HOW TO USE:
//   1. Connect Chrome via list_connected_browsers + select_browser.
//   2. tabs_context_mcp(createIfEmpty=true).
//   3. Paste this entire file as the `text` parameter to javascript_tool —
//      EDIT the TICKERS array at the top first.
//   4. Poll window._perfResult with a follow-up javascript_tool call until
//      it returns the JSON-stringified perf table.
//
// HARDENING vs v1 (May 26 PM):
//   • Symbol normalization: BRK.B -> BRK-B, BF.B -> BF-B (Yahoo's canonical
//     form is dash, not dot). Auto-applied — keywords.md can use either form.
//   • Defensive null checks at every nested field (indicators / quote / close).
//   • Yahoo's HTTP-200 + chart.error pattern detected and surfaced.
//   • Single retry on transient 5xx / network failure (1s backoff).
//   • Uses adjclose primary, raw close fallback (handles splits + dividends).
//   • regularMarketPrice fallback when fewer than 2 valid closes available.
//
// METHODOLOGY (Yahoo quote-page-aligned):
//   • Range: range=2y (gives ~500 closes; range=1y returns 251 and breaks 1Y).
//   • Anchor = closes[-2] (most recent COMPLETED close, stable mid-session).
//   • 1D/1W: trading-day-based (anchor_idx - 1 and -5).
//   • 1M/6M/1Y: calendar-based — most recent close ON OR BEFORE (anchor - delta).
//   • YTD: Dec 31 PRIOR-YEAR close (NOT Jan 2 of current year).
//   • 1Y_partial: true => ticker has <1Y trading history (recent IPO).

// ============================================================
// EDIT THIS LINE before pasting into javascript_tool:
const TICKERS = ['AUR', 'KDK', 'UBER', 'EH'];   // replace with sector's tickers
// ============================================================

// Symbol normalization: Yahoo uses dash, not dot, for class shares.
// BRK.B -> BRK-B, BF.B -> BF-B, RDS.A -> RDS-A, etc.
function normalizeTicker(t) {
    return t.replace(/\./g, '-');
}

// Fetch with single retry on 5xx or network failure.
async function fetchChart(rawTicker, attempt) {
    if (attempt === undefined) attempt = 0;
    const norm = normalizeTicker(rawTicker);
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(norm)}?interval=1d&range=2y`;
    try {
        const r = await fetch(url);
        if (!r.ok) {
            // Retry on transient 5xx; do NOT retry on 4xx (won't fix itself)
            if (r.status >= 500 && attempt === 0) {
                await new Promise(res => setTimeout(res, 1000));
                return fetchChart(rawTicker, 1);
            }
            return { ok: false, error: `HTTP ${r.status}`, normalized: norm };
        }
        const j = await r.json();
        // Yahoo can return 200 + chart.error for bad symbols. Check both paths.
        if (j.chart && j.chart.error) {
            return { ok: false, error: `${j.chart.error.code}: ${j.chart.error.description}`, normalized: norm };
        }
        const res = j.chart && j.chart.result && j.chart.result[0];
        if (!res) return { ok: false, error: 'No chart.result[0]', normalized: norm };
        const quote = res.indicators && res.indicators.quote && res.indicators.quote[0];
        if (!quote || !Array.isArray(quote.close)) {
            return { ok: false, error: 'No close series in indicators.quote[0]', normalized: norm };
        }
        // Prefer adjclose (handles splits + dividends). Fallback to raw close.
        // Use RAW close (not adjclose). Yahoo's published 1D/5D/1M/6M/YTD/1Y
        // pills on the quote page are PRICE return (raw close), not total
        // return (adjclose). Using adjclose introduces a divergence equal to
        // the trailing dividend yield (~2-3% for typical dividend payers).
        // Reverse-engineered May 26, 2026 — confirmed exact match on SBUX.
        return {
            ok: true,
            ts: res.timestamp,
            series: quote.close,
            usingAdjclose: false,
            meta: res.meta,
            normalized: norm
        };
    } catch (e) {
        if (attempt === 0) {
            await new Promise(res => setTimeout(res, 1000));
            return fetchChart(rawTicker, 1);
        }
        return { ok: false, error: String(e), normalized: norm };
    }
}

window._perfPromise = (async () => {
    const out = {};

    for (const t of TICKERS) {
        const fetched = await fetchChart(t);
        if (!fetched.ok) {
            out[t] = { ok: false, error: fetched.error, normalized: fetched.normalized };
            continue;
        }

        // Strip nulls, keep (timestamp, value) pairs
        const pairs = [];
        for (let i = 0; i < fetched.ts.length; i++) {
            if (fetched.series[i] !== null && fetched.series[i] !== undefined) {
                pairs.push([fetched.ts[i], fetched.series[i]]);
            }
        }
        if (pairs.length < 2) {
            // Last-resort fallback: use live meta price; no perf
            if (fetched.meta && fetched.meta.regularMarketPrice) {
                out[t] = {
                    ok: 'partial',
                    warning: 'fewer than 2 valid closes — perf unavailable, live price only',
                    live: fetched.meta.regularMarketPrice,
                    normalized: fetched.normalized
                };
            } else {
                out[t] = { ok: false, error: 'fewer than 2 valid closes and no regularMarketPrice', normalized: fetched.normalized };
            }
            continue;
        }

        const ts = pairs.map(p => p[0]);
        const closes = pairs.map(p => p[1]);

        // Anchor = closes[-1] (the most recent close Yahoo reports — same value
        // shown on the quote page header). Behavior across session states:
        //   • after close: closes[-1] = today's settled close (stable)
        //   • premarket:   closes[-1] = prior trading day's close (stable)
        //   • mid-session: closes[-1] = live intraday quote (moves with tape)
        // The live-intraday case means re-running mid-day will shift numbers,
        // but they will always match what's shown on the Yahoo page AT THAT
        // MOMENT — which is the point. Reverse-engineered May 26, 2026.
        const ai = closes.length - 1;
        const anchor = closes[ai];
        const anchorD = new Date(ts[ai] * 1000);
        const anchorDate = anchorD.toISOString().slice(0, 10);

        const tdBack = (n) => (ai - n >= 0) ? closes[ai - n] : null;
        const tdBackDate = (n) => (ai - n >= 0) ? new Date(ts[ai - n] * 1000).toISOString().slice(0, 10) : null;

        function calBack(deltaSpec) {
            const target = new Date(anchorD);
            if (deltaSpec.months) target.setUTCMonth(target.getUTCMonth() - deltaSpec.months);
            if (deltaSpec.years)  target.setUTCFullYear(target.getUTCFullYear() - deltaSpec.years);
            // CRITICAL: set target to END of UTC day. Without this, the DST
            // shift between May (EDT, UTC-4) and Nov (EST, UTC-5) makes the
            // target one hour BEFORE the recorded Nov close timestamp, and the
            // "on-or-b