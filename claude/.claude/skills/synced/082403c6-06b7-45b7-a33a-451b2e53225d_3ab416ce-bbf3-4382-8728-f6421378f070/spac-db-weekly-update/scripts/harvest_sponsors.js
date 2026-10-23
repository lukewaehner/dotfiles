/* harvest_sponsors.js
 * Run this in the Claude-in-Chrome javascript_tool while on https://www.spacresearch.com/sponsor
 * (full logged-in account). It reads the AG-Grid row model for the Sponsors tab and triggers a
 * download of sponsors_<YYYY-MM-DD>.json into the browser's download folder.
 * The Sponsors page has no clean CSV export URL, so we harvest its grid directly.
 */
(() => {
  const api = window.gridApi;
  if (!api || !api.forEachNode) return { ready: false, why: "grid api not found - is the /sponsor page loaded?" };
  const nodes = [];
  api.forEachNode(n => { if (n.data) nodes.push(n.data); });
  if (!nodes.length) return { ready: false, why: "no rows yet - wait for the grid to load and retry" };

  // union of keys across all rows (robust to per-row variation)
  const keySet = [], seen = new Set();
  nodes.forEach(d => Object.keys(d).forEach(k => { if (!seen.has(k)) { seen.add(k); keySet.push(k); } }));
  const defs = ((api.getColumnDefs && api.getColumnDefs()) || []).map(c => ({ field: c.field, header: c.headerName }));
  const rows = nodes.map(d => keySet.map(k => (d[k] === undefined ? null : d[k])));

  const payload = { category: "sponsors", fields: keySet, colDefs: defs, rows, count: nodes.length };
  const date = new Date().toISOString().slice(0, 10);
  const blob = new Blob([JSON.stringify(payload)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "sponsors_" + date + ".json";
  document.body.appendChild(a); a.click();
  setTimeout(() => { try { URL.revokeObjectURL(a.href); a.remove(); } catch (e) {} }, 1500);

  return { ready: true, count: nodes.length, nfields: keySet.length, file: a.download };
})();
