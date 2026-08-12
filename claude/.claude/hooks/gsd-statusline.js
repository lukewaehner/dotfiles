#!/usr/bin/env node
// gsd-hook-version: 1.42.3
// Claude Code Statusline - GSD Edition
// Shows: model | current task (or GSD state) | directory | context usage

const fs = require('fs');
const path = require('path');
const os = require('os');

// --- Config + last-command readers ------------------------------------------

/**
 * Walk up from dir looking for .planning/config.json and return its parsed contents.
 * Returns {} if not found or unreadable.
 */
function readGsdConfig(dir) {
  const home = os.homedir();
  let current = dir;
  for (let i = 0; i < 10; i++) {
    const candidate = path.join(current, '.planning', 'config.json');
    if (fs.existsSync(candidate)) {
      try {
        return JSON.parse(fs.readFileSync(candidate, 'utf8')) || {};
      } catch (e) {
        return {};
      }
    }
    const parent = path.dirname(current);
    if (parent === current || current === home) break;
    current = parent;
  }
  return {};
}

/**
 * Lookup a dotted key path (e.g. 'statusline.show_last_command') in a config
 * object that may use either nested or flat keys.
 */
function getConfigValue(cfg, keyPath) {
  if (!cfg || typeof cfg !== 'object') return undefined;
  if (keyPath in cfg) return cfg[keyPath];
  const parts = keyPath.split('.');
  let cur = cfg;
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object' || !(p in cur)) return undefined;
    cur = cur[p];
  }
  return cur;
}

/**
 * Extract the most recently invoked slash command from a Claude Code JSONL
 * transcript file. Returns the command name (no leading slash) or null.
 *
 * Claude Code embeds slash invocations in user messages as
 *   <command-name>/foo</command-name>
 * We scan lines from the end of the file, stopping at the first match.
 */
function readLastSlashCommand(transcriptPath) {
  if (!transcriptPath || typeof transcriptPath !== 'string') return null;
  let content;
  try {
    if (!fs.existsSync(transcriptPath)) return null;
    // Read only the tail — typical transcripts grow large. 256 KiB comfortably
    // covers dozens of recent turns while staying cheap per render.
    const stat = fs.statSync(transcriptPath);
    const MAX = 256 * 1024;
    const start = Math.max(0, stat.size - MAX);
    const fd = fs.openSync(transcriptPath, 'r');
    try {
      const buf = Buffer.alloc(stat.size - start);
      fs.readSync(fd, buf, 0, buf.length, start);
      content = buf.toString('utf8');
    } finally {
      fs.closeSync(fd);
    }
  } catch (e) {
    return null;
  }
  // Find the LAST occurrence — scan right-to-left via lastIndexOf on the tag.
  const tagClose = '</command-name>';
  const idx = content.lastIndexOf(tagClose);
  if (idx < 0) return null;
  const openTag = '<command-name>';
  const openIdx = content.lastIndexOf(openTag, idx);
  if (openIdx < 0) return null;
  let name = content.slice(openIdx + openTag.length, idx).trim();
  // Strip a leading slash if present, and any trailing arguments-on-same-line noise.
  if (name.startsWith('/')) name = name.slice(1);
  // Command names in Claude Code transcripts are plain identifiers like "gsd-plan-phase"
  // or namespaced like "plugin:skill". Reject anything with whitespace/newlines/control chars.
  if (!name || /[\s\\"<>]/.test(name) || name.length > 80) return null;
  return name;
}

// --- GSD state reader -------------------------------------------------------

/**
 * Walk up from dir looking for .planning/STATE.md.
 * Returns parsed state object or null.
 */
function readGsdState(dir) {
  const home = os.homedir();
  let current = dir;
  for (let i = 0; i < 10; i++) {
    const candidate = path.join(current, '.planning', 'STATE.md');
    if (fs.existsSync(candidate)) {
      try {
        return parseStateMd(fs.readFileSync(candidate, 'utf8'));
      } catch (e) {
        return null;
      }
    }
    const parent = path.dirname(current);
    if (parent === current || current === home) break;
    current = parent;
  }
  return null;
}

/**
 * Parse STATE.md frontmatter + Phase line from body.
 *
 * Returns:
 *   { status, milestone, milestoneName, phaseNum, phaseTotal, phaseName,
 *     activePhase, nextAction, nextPhases, completedPhases, totalPhases, percent }
 *
 * Phase-lifecycle fields (issue #2833):
 *   - activePhase  : phase number ("4.5") when an orchestrator is mid-flight, null otherwise
 *   - nextAction   : recommended next command ("execute-phase") when idle, null otherwise
 *   - nextPhases   : array of phase numbers (["4.5"]) for nextAction, null otherwise
 *   - completedPhases / totalPhases / percent : milestone progress dimension
 *
 * All new fields default to undefined when absent — formatGsdState() degrades
 * gracefully so existing STATE.md files (without these fields) keep working.
 */
function parseStateMd(content) {
  const state = {};

  // YAML frontmatter between --- markers (anchored at file start)
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const fm = fmMatch[1];
    // Top-level scalar key: value
    for (const line of fm.split('\n')) {
      const m = line.match(/^(\w+):\s*(.+)/);
      if (!m) continue;
      const [, key, val] = m;
      const v = val.trim().replace(/^["']|["']$/g, '');
      // status / milestone-level fields (existing — preserved exactly)
      if (key === 'status') state.status = v === 'null' ? null : v;
      if (key === 'milestone') state.milestone = v === 'null' ? null : v;
      if (key === 'milestone_name') state.milestoneName = v === 'null' ? null : v;
      // Phase-lifecycle fields (new in issue #2833)
      // active_phase: phase number when an orchestrator is in-flight, null when idle
      if (key === 'active_phase') state.activePhase = (v === 'null' || v === '') ? null : v;
      // next_action: recommended command when idle (discuss-phase / plan-phase / execute-phase / verify-phase)
      if (key === 'next_action') state.nextAction = (v === 'null' || v === '') ? null : v;
    }
    // next_phases supports both flow array and block-list YAML forms.
    const npFlowMatch = fm.match(/^next_phases:\s*\[([^\]]*)\]/m);
    if (npFlowMatch) {
      const items = npFlowMatch[1].split(',').map(s => s.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
      state.nextPhases = items.length > 0 ? items : null;
    } else {
      const npBlockMatch = fm.match(/^next_phases:\s*\n((?:[ \t]*-[ \t]*[^\n]+\n?)*)/m);
      if (npBlockMatch) {
        const items = npBlockMatch[1]
          .split('\n')
          .map(line => line.match(/^[ \t]*-[ \t]*(.+)$/))
          .filter(Boolean)
          .map(m => m[1].trim().replace(/^["']|["']$/g, ''))
          .filter(Boolean);
        state.nextPhases = items.length > 0 ? items : null;
      }
    }
    // progress nested block: completed_phases / total_phases / percent (2-space indent)
    const progMatch = fm.match(/^progress:\s*\n((?:[ \t]+\w+:.+\n?)+)/m);
    if (progMatch) {
      const cp = progMatch[1].match(/^[ \t]+completed_phases:\s*(\d+)/m);
      const tp = progMatch[1].match(/^[ \t]+total_phases:\s*(\d+)/m);
      const pc = progMatch[1].match(/^[ \t]+percent:\s*(\d+)/m);
      if (cp) state.completedPhases = cp[1];
      if (tp) state.totalPhases = tp[1];
      if (pc) state.percent = pc[1];
    }
  }

  // Phase: N of M (name)  or  Phase: none active (...)
  const phaseMatch = content.match(/^Phase:\s*(\d+)\s+of\s+(\d+)(?:\s+\(([^)]+)\))?/m);
  if (phaseMatch) {
    state.phaseNum = phaseMatch[1];
    state.phaseTotal = phaseMatch[2];
    state.phaseName = phaseMatch[3] || null;
  }

  // Fallback: parse Status: from body when frontmatter is absent
  if (!state.status) {
    const bodyStatus = content.match(/^Status:\s*(.+)/m);
    if (bodyStatus) {
      const raw = bodyStatus[1].trim().toLowerCase();
      if (raw.includes('ready to plan') || raw.includes('planning')) state.status = 'planning';
      else if (raw.includes('execut')) state.status = 'executing';
      else if (raw.includes('complet') || raw.includes('archived')) state.status = 'complete';
    }
  }

  return state;
}

/**
 * Render a 10-segment milestone progress bar (matches the context meter style).
 *
 * @param {number|string|null|undefined} percent — 0-100; missing/NaN returns ''
 * @returns {string} '[█████░░░░░] 50%' or '' (so callers can `[bar].filter(Boolean)`)
 */
function renderProgressBar(percent) {
  if (percent == null || isNaN(percent)) return '';
  const pct = Math.max(0, Math.min(100, parseInt(percent, 10)));
  const filled = Math.floor(pct / 10);
  const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);
  return `[${bar}] ${pct}%`;
}

/**
 * Format GSD state into display string.
 *
 * Backward-compatible default (no new fields populated):
 *   "v1.9 Code Quality · executing · fix-graphiti-deployment (1/5)"
 *
 * Phase-lifecycle scenes (issue #2833 — activate when STATE.md frontmatter
 * carries the new fields; otherwise rendering falls through to the default):
 *
 *   active_phase set                       → "v2.0 [██░] X% · Phase 4.5 executing"
 *   active_phase null + next_action set    → "v2.0 [██░] X% · next execute-phase 4.5"
 *   percent=100 (milestone done)           → "v2.0 [██████████] 100% · milestone complete"
 *   none of the above                      → existing "<status> · <phase>" path
 *
 * Progress bar is opt-in: appended to the milestone segment only when
 * progress.percent is present in frontmatter; absent → empty string.
 */
function formatGsdState(s) {
  const parts = [];

  // Milestone segment: version + name + (opt-in) progress bar
  if (s.milestone || s.milestoneName) {
    const ver = s.milestone || '';
    const name = (s.milestoneName && s.milestoneName !== 'milestone') ? s.milestoneName : '';
    const bar = renderProgressBar(s.percent);
    const pieces = [ver, name, bar].filter(Boolean);
    if (pieces.length > 0) parts.push(pieces.join(' '));
  }

  // Phase-lifecycle scenes (issue #2833) — first match wins; falls through to
  // the original "<status> · <phase>" path when none of the new fields apply.
  const phasesStr = (s.nextPhases && s.nextPhases.length > 0) ? s.nextPhases.join('/') : null;

  if (s.activePhase) {
    // Scene 1: an orchestrator is mid-flight on this phase.
    // stage = whichever lifecycle status was written by the orchestrator
    //   (discussing / planning / executing / verifying)
    const stage = s.status || '';
    parts.push(stage ? `Phase ${s.activePhase} ${stage}` : `Phase ${s.activePhase}`);
  } else if (s.nextAction && phasesStr) {
    // Scene 2: idle + a recommended next command is visible to the user.
    // Surfaces "what to run next" without the user opening STATE.md.
    parts.push(`next ${s.nextAction} ${phasesStr}`);
  } else if (Number(s.percent) === 100 || (s.completedPhases && s.totalPhases && s.completedPhases === s.totalPhases)) {
    // Scene 3: milestone complete (every phase done).
    parts.push('milestone complete');
  } else {
    // Backward-compatible default — preserved EXACTLY for STATE.md files that
    // don't carry the new lifecycle fields. Identical output to v1.38.x and
    // earlier so no existing project's status-line changes shape.
    if (s.status) parts.push(s.status);
    if (s.phaseNum && s.phaseTotal) {
      const phase = s.phaseName
        ? `${s.phaseName} (${s.phaseNum}/${s.phaseTotal})`
        : `ph ${s.phaseNum}/${s.phaseTotal}`;
      parts.push(phase);
    }
  }

  return parts.join(' · ');
}

// --- Usage stats (1d / 7d token totals from JSONL history) -----------------

/**
 * Scan JSONL conversation files to compute token usage for the last N days.
 * Only reads files modified within the window to keep it fast.
 * Results are cached in /tmp for 5 minutes.
 */
function computeUsageStats(claudeDir) {
  const cacheWindow = 5 * 60 * 1000; // 5 minutes
  const cacheKey = Math.floor(Date.now() / cacheWindow);
  const cachePath = path.join(os.tmpdir(), `claude-usage-${cacheKey}.json`);

  if (fs.existsSync(cachePath)) {
    try {
      return JSON.parse(fs.readFileSync(cachePath, 'utf8'));
    } catch (e) {}
  }

  const projectsDir = path.join(claudeDir, 'projects');
  if (!fs.existsSync(projectsDir)) return null;

  const now = Date.now();
  const day1Cutoff = now - 24 * 60 * 60 * 1000;
  const day7Cutoff = now - 7 * 24 * 60 * 60 * 1000;
  const day28Cutoff = now - 28 * 24 * 60 * 60 * 1000;

  // Collect tokens per day (YYYY-MM-DD) for all entries in the last 28 days
  const tokensByDay = {};

  // Find all JSONL files modified in the last 28 days
  let jsonlFiles = [];
  try {
    const cutoffMs = day28Cutoff;
    function walkDir(dir) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const ent of entries) {
        const full = path.join(dir, ent.name);
        if (ent.isDirectory()) {
          walkDir(full);
        } else if (ent.isFile() && ent.name.endsWith('.jsonl')) {
          const stat = fs.statSync(full);
          if (stat.mtimeMs >= cutoffMs) jsonlFiles.push(full);
        }
      }
    }
    walkDir(projectsDir);
  } catch (e) {
    return null;
  }

  for (const file of jsonlFiles) {
    let content;
    try {
      content = fs.readFileSync(file, 'utf8');
    } catch (e) {
      continue;
    }
    for (const line of content.split('\n')) {
      if (!line.includes('"usage"') || !line.includes('"timestamp"')) continue;
      let parsed;
      try { parsed = JSON.parse(line); } catch (e) { continue; }
      if (parsed.type !== 'assistant' || !parsed.timestamp || !parsed.message?.usage) continue;
      const ts = new Date(parsed.timestamp).getTime();
      if (isNaN(ts) || ts < day28Cutoff) continue;
      const u = parsed.message.usage;
      const tokens = (u.input_tokens || 0) + (u.output_tokens || 0);
      if (tokens === 0) continue;
      const day = parsed.timestamp.slice(0, 10); // YYYY-MM-DD
      tokensByDay[day] = (tokensByDay[day] || 0) + tokens;
    }
  }

  // Compute 1d, 7d totals and 28d daily values for averages
  const todayStr = new Date().toISOString().slice(0, 10);
  let tokens1d = 0;
  let tokens7d = 0;
  const dailyValues28d = [];

  for (const [day, tokens] of Object.entries(tokensByDay)) {
    const dayTs = new Date(day + 'T12:00:00Z').getTime();
    if (day === todayStr) tokens1d += tokens;
    if (dayTs >= day7Cutoff) tokens7d += tokens;
    if (dayTs >= day28Cutoff) dailyValues28d.push(tokens);
  }

  // Averages: 7d daily avg and 4-week weekly avg
  const avg7dDaily = dailyValues28d.length > 0
    ? dailyValues28d.reduce((a, b) => a + b, 0) / Math.max(7, dailyValues28d.length)
    : 0;

  // Weekly tokens for each of the 4 past weeks (excluding current week)
  const weeklyValues = [];
  for (let w = 1; w <= 4; w++) {
    const wStart = now - w * 7 * 24 * 60 * 60 * 1000;
    const wEnd = now - (w - 1) * 7 * 24 * 60 * 60 * 1000;
    let wTokens = 0;
    for (const [day, tokens] of Object.entries(tokensByDay)) {
      const dayTs = new Date(day + 'T12:00:00Z').getTime();
      if (dayTs >= wStart && dayTs < wEnd) wTokens += tokens;
    }
    if (wTokens > 0) weeklyValues.push(wTokens);
  }
  const avg4wWeekly = weeklyValues.length > 0
    ? weeklyValues.reduce((a, b) => a + b, 0) / weeklyValues.length
    : 0;

  const result = { tokens1d, tokens7d, avg7dDaily, avg4wWeekly };
  try { fs.writeFileSync(cachePath, JSON.stringify(result)); } catch (e) {}
  return result;
}

/**
 * Format token count as compact string: 145k, 2.4M, etc.
 */
function fmtTokens(n) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}k`;
  return `${n}`;
}

/**
 * Pick ANSI color based on usage percentage vs average:
 * <70% green, 70-84% yellow, 85-99% orange, ≥100% red.
 */
function usageColor(pct) {
  if (pct < 70) return '\x1b[32m';
  if (pct < 85) return '\x1b[33m';
  if (pct < 100) return '\x1b[38;5;208m';
  return '\x1b[31m';
}

/**
 * Build a 5-segment progress bar string (no ANSI) for a given percentage.
 */
function fmtUsageBar(pct) {
  const filled = Math.min(5, Math.floor(Math.min(pct, 100) / 20));
  return '█'.repeat(filled) + '░'.repeat(5 - filled);
}

/**
 * Build usage segment string for statusline.
 * Shows colored bars: "D:[████░] 87% W:[██░░░] 35%"
 * Falls back to plain token count when no historical average exists.
 */
function formatUsageSegment(stats) {
  if (!stats || (stats.tokens1d === 0 && stats.tokens7d === 0)) return '';

  const parts = [];

  if (stats.avg7dDaily > 0) {
    const pct = Math.round((stats.tokens1d / stats.avg7dDaily) * 100);
    const col = usageColor(pct);
    parts.push(`D:${col}[${fmtUsageBar(pct)}] ${pct}%\x1b[0m`);
  } else if (stats.tokens1d > 0) {
    parts.push(`D:${fmtTokens(stats.tokens1d)}`);
  }

  if (stats.avg4wWeekly > 0) {
    const pct = Math.round((stats.tokens7d / stats.avg4wWeekly) * 100);
    const col = usageColor(pct);
    parts.push(`W:${col}[${fmtUsageBar(pct)}] ${pct}%\x1b[0m`);
  } else if (stats.tokens7d > 0) {
    parts.push(`W:${fmtTokens(stats.tokens7d)}`);
  }

  return parts.join(' ');
}

// --- stdin ------------------------------------------------------------------

function runStatusline() {
  let input = '';
  // Timeout guard: if stdin doesn't close within 3s (e.g. pipe issues on
  // Windows/Git Bash), exit silently instead of hanging. See #775.
  const stdinTimeout = setTimeout(() => process.exit(0), 3000);
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
  clearTimeout(stdinTimeout);
  try {
    const data = JSON.parse(input);
    const model = data.model?.display_name || 'Claude';
    const dir = data.workspace?.current_dir || process.cwd();
    const session = data.session_id || '';
    const remaining = data.context_window?.remaining_percentage;

    // Context window display (shows USED percentage scaled to usable context)
    // Claude Code reserves a buffer for autocompact. By default this is ~16.5%
    // of the total window, but users can override it via CLAUDE_CODE_AUTO_COMPACT_WINDOW
    // (a token count). When the env var is set, compute the buffer % dynamically so
    // the meter correctly reflects early-compaction configurations (#2219).
    const totalCtx = data.context_window?.total_tokens || 1_000_000;
    const acw = parseInt(process.env.CLAUDE_CODE_AUTO_COMPACT_WINDOW || '0', 10);
    const AUTO_COMPACT_BUFFER_PCT = acw > 0
      ? Math.min(100, (acw / totalCtx) * 100)
      : 16.5;
    let ctx = '';
    if (remaining != null) {
      // Normalize: subtract buffer from remaining, scale to usable range
      const usableRemaining = Math.max(0, ((remaining - AUTO_COMPACT_BUFFER_PCT) / (100 - AUTO_COMPACT_BUFFER_PCT)) * 100);
      const used = Math.max(0, Math.min(100, Math.round(100 - usableRemaining)));

      // Write context metrics to bridge file for the context-monitor PostToolUse hook.
      // The monitor reads this file to inject agent-facing warnings when context is low.
      // Reject session IDs with path separators or traversal sequences to prevent
      // a malicious session_id from writing files outside the temp directory.
      const sessionSafe = session && !/[/\\]|\.\./.test(session);
      if (sessionSafe) {
        try {
          const bridgePath = path.join(os.tmpdir(), `claude-ctx-${session}.json`);
          // used_pct written to the bridge must match CC's native /context reporting:
          // raw used = 100 - remaining_percentage (no buffer normalization applied).
          // The normalized `used` value is correct for the statusline progress bar but
          // inflates the context monitor warning messages by ~13 points (#2451).
          const rawUsedPct = Math.round(100 - remaining);
          const bridgeData = JSON.stringify({
            session_id: session,
            remaining_percentage: remaining,
            used_pct: rawUsedPct,
            timestamp: Math.floor(Date.now() / 1000)
          });
          fs.writeFileSync(bridgePath, bridgeData);
        } catch (e) {
          // Silent fail -- bridge is best-effort, don't break statusline
        }
      }

      // Build progress bar (10 segments)
      const filled = Math.floor(used / 10);
      const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);

      // Color based on usable context thresholds
      if (used < 50) {
        ctx = ` \x1b[32m${bar} ${used}%\x1b[0m`;
      } else if (used < 65) {
        ctx = ` \x1b[33m${bar} ${used}%\x1b[0m`;
      } else if (used < 80) {
        ctx = ` \x1b[38;5;208m${bar} ${used}%\x1b[0m`;
      } else {
        ctx = ` \x1b[5;31m💀 ${bar} ${used}%\x1b[0m`;
      }
    }

    // Current task from todos
    let task = '';
    const homeDir = os.homedir();
    // Respect CLAUDE_CONFIG_DIR for custom config directory setups (#870)
    const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(homeDir, '.claude');
    const todosDir = path.join(claudeDir, 'todos');
    if (session && fs.existsSync(todosDir)) {
      try {
        const files = fs.readdirSync(todosDir)
          .filter(f => f.startsWith(session) && f.includes('-agent-') && f.endsWith('.json'))
          .map(f => ({ name: f, mtime: fs.statSync(path.join(todosDir, f)).mtime }))
          .sort((a, b) => b.mtime - a.mtime);

        if (files.length > 0) {
          try {
            const todos = JSON.parse(fs.readFileSync(path.join(todosDir, files[0].name), 'utf8'));
            const inProgress = todos.find(t => t.status === 'in_progress');
            if (inProgress) task = inProgress.activeForm || '';
          } catch (e) {}
        }
      } catch (e) {
        // Silently fail on file system errors - don't break statusline
      }
    }

    // GSD state (milestone · status · phase) — shown when no todo task
    const gsdStateStr = task ? '' : formatGsdState(readGsdState(dir) || {});

    // GSD update available?
    // Check shared cache first (#1421), fall back to runtime-specific cache for
    // backward compatibility with older gsd-check-update.js versions.
    let gsdUpdate = '';
    const sharedCacheFile = path.join(homeDir, '.cache', 'gsd', 'gsd-update-check.json');
    const legacyCacheFile = path.join(claudeDir, 'cache', 'gsd-update-check.json');
    const cacheFile = fs.existsSync(sharedCacheFile) ? sharedCacheFile : legacyCacheFile;
    if (fs.existsSync(cacheFile)) {
      try {
        const cache = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
        if (cache.update_available) {
          gsdUpdate = '\x1b[33m⬆ /gsd:update\x1b[0m │ ';
        }
        if (cache.stale_hooks && cache.stale_hooks.length > 0) {
          // If installed version is ahead of npm latest, this is a dev install.
          // Running /gsd:update would downgrade — show a contextual warning instead.
          const isDevInstall = (() => {
            if (!cache.installed || !cache.latest || cache.latest === 'unknown') return false;
            const parseV = v => v.replace(/^v/, '').split('.').map(Number);
            const [ai, bi, ci] = parseV(cache.installed);
            const [an, bn, cn] = parseV(cache.latest);
            return ai > an || (ai === an && bi > bn) || (ai === an && bi === bn && ci > cn);
          })();
          if (isDevInstall) {
            gsdUpdate += '\x1b[33m⚠ dev install — re-run installer to sync hooks\x1b[0m │ ';
          } else {
            gsdUpdate += '\x1b[31m⚠ stale hooks — run /gsd:update\x1b[0m │ ';
          }
        }
      } catch (e) {}
    }

    // Last-slash-command suffix and context_position config (#2538, #2937).
    // Reads the active session transcript for the most recent <command-name> tag.
    // Failure here must never break the statusline — wrap the entire lookup.
    let lastCmdSuffix = '';
    let position = 'end';
    try {
      const cfg = readGsdConfig(dir);
      if (getConfigValue(cfg, 'statusline.show_last_command') === true) {
        const transcriptPath = data.transcript_path;
        const lastCmd = readLastSlashCommand(transcriptPath);
        if (lastCmd) {
          lastCmdSuffix = ` │ \x1b[2mlast: /${lastCmd}\x1b[0m`;
        }
      }
      const cfgPos = getConfigValue(cfg, 'statusline.context_position');
      if (cfgPos != null) position = cfgPos;
    } catch (e) {
      // Never break the statusline on config/transcript errors
    }

    // Rate limit bars — real plan usage from stdin payload (five_hour / seven_day)
    let usageSeg = '';
    try {
      const rl = data.rate_limits;
      if (rl && (rl.five_hour || rl.seven_day)) {
        const parts = [];
        if (rl.five_hour) {
          const pct = rl.five_hour.used_percentage || 0;
          parts.push(`5h:${usageColor(pct)}${pct}%\x1b[0m`);
        }
        if (rl.seven_day) {
          const pct = rl.seven_day.used_percentage || 0;
          parts.push(`7d:${usageColor(pct)}${pct}%\x1b[0m`);
        }
        usageSeg = ` │ ${parts.join('  ')}`;
      } else {
        // Fallback: historical token averages when rate_limits not present
        const homeDir2 = os.homedir();
        const claudeDir2 = process.env.CLAUDE_CONFIG_DIR || path.join(homeDir2, '.claude');
        const usageStats = computeUsageStats(claudeDir2);
        const raw = formatUsageSegment(usageStats);
        if (raw) usageSeg = ` ${raw}`;
      }
    } catch (e) {}

    // Output — show ~-relative path for the directory segment
    const homeDir3 = os.homedir();
    const dirDisplay = dir === homeDir3 ? '~'
      : dir.startsWith(homeDir3 + '/') ? '~' + dir.slice(homeDir3.length)
      : dir;
    const dirname = dirDisplay;
    const middle = task
      ? `\x1b[1m${task}\x1b[0m`
      : gsdStateStr
        ? `\x1b[2m${gsdStateStr}\x1b[0m`
        : null;

    process.stdout.write(composeStatusline({ gsdUpdate, model, ctx, usageSeg, middle, dirname, lastCmdSuffix, position }));
  } catch (e) {
    // Silent fail - don't break statusline on parse errors
  }
});
}

// --- Layout composer --------------------------------------------------------

/**
 * Compose the statusline string from pre-built segments.
 *
 * @param {object} opts
 * @param {string} [opts.gsdUpdate='']      - leading update/stale-hooks warning (already formatted)
 * @param {string} opts.model               - model display name (plain text; dim styling applied here)
 * @param {string} [opts.ctx='']            - context-window meter segment (empty string = absent)
 * @param {string|null} [opts.middle=null]  - middle segment (todo task or GSD state), null = absent
 * @param {string} opts.dirname             - project directory basename (dim styling applied here)
 * @param {string} [opts.lastCmdSuffix='']  - last-command suffix, e.g. ' │ last: /foo'
 * @param {'end'|'front'} [opts.position='end']
 *   - 'end'   (default): ctx appended after dirname — preserved byte-for-byte
 *   - 'front': ctx immediately after model name so the meter stays visible in narrow terminals
 *
 * Invalid position values are silently coerced to 'end' — config-set schema rejects
 * invalid values upfront; runtime fallback defends against stale/corrupt configs
 * without breaking the statusline.
 */
function composeStatusline({
  gsdUpdate = '',
  model,
  ctx = '',
  usageSeg = '',
  middle = null,
  dirname,
  lastCmdSuffix = '',
  position = 'end',
} = {}) {
  const modelSeg = `\x1b[2m${model}\x1b[0m`;
  const dirSeg = `\x1b[2m${dirname}\x1b[0m`;
  // Coerce invalid values to 'end' (belt-and-suspenders; see JSDoc above)
  const pos = position === 'front' ? 'front' : 'end';

  if (pos === 'front') {
    if (middle) return `${gsdUpdate}${modelSeg}${ctx} │ ${middle}${usageSeg} │ ${dirSeg}${lastCmdSuffix}`;
    return `${gsdUpdate}${modelSeg}${ctx}${usageSeg} │ ${dirSeg}${lastCmdSuffix}`;
  }
  // 'end' — dir moved to right side
  if (middle) return `${gsdUpdate}${modelSeg} │ ${middle}${ctx}${usageSeg} │ ${dirSeg}${lastCmdSuffix}`;
  return `${gsdUpdate}${modelSeg}${ctx}${usageSeg} │ ${dirSeg}${lastCmdSuffix}`;
}

// Export helpers for unit tests. Harmless when run as a script.
module.exports = {
  readGsdState, parseStateMd, formatGsdState,
  readGsdConfig, getConfigValue, readLastSlashCommand,
  composeStatusline,
};

/**
 * Render the statusline from an already-parsed hook input object. Exported for
 * testing without feeding stdin. Returns the rendered string.
 */
function renderStatusline(data) {
  const model = data.model?.display_name || 'Claude';
  const dir = data.workspace?.current_dir || process.cwd();
  const dirname = path.basename(dir);

  let lastCmdSuffix = '';
  let position = 'end';
  try {
    const cfg = readGsdConfig(dir);
    if (getConfigValue(cfg, 'statusline.show_last_command') === true) {
      const lastCmd = readLastSlashCommand(data.transcript_path);
      if (lastCmd) {
        lastCmdSuffix = ` │ \x1b[2mlast: /${lastCmd}\x1b[0m`;
      }
    }
    const cfgPos = getConfigValue(cfg, 'statusline.context_position');
    if (cfgPos != null) position = cfgPos;
  } catch (e) { /* swallow */ }

  const gsdStateStr = formatGsdState(readGsdState(dir) || {});
  const middle = gsdStateStr ? `\x1b[2m${gsdStateStr}\x1b[0m` : null;
  return composeStatusline({ model, ctx: '', middle, dirname, lastCmdSuffix, position });
}

module.exports.renderStatusline = renderStatusline;

if (require.main === module) runStatusline();
