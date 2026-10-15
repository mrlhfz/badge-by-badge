// @ts-check
'use strict';

/**
 * SessionStart hook: emit the command-execution rules.
 *
 * Reads CLAUDE.command-rules.md from the repo root and writes it to stdout behind
 * a short preamble. Claude Code adds a SessionStart hook's plain-text stdout to
 * the session context, so the rules are injected once per session boundary
 * (startup / resume / clear / compact).
 *
 * The file is resolved from this script's location, so the working directory
 * does not matter. Any failure is reported on stderr and the process still exits
 * 0: a broken hook must never block session start.
 *
 * Wired in .claude/settings.json under hooks.SessionStart.
 */

const fs = require('fs');
const path = require('path');

/** Absolute path to the rules file (.claude/hooks/ up to the repo root). */
const RULES_FILE = path.join(__dirname, '..', '..', 'CLAUDE.command-rules.md');

/** One-line preamble so the reader knows what follows and where it came from. */
const PREAMBLE =
  "The following are this project's command-execution rules, injected once at " +
  'session start from CLAUDE.command-rules.md (repo root). Follow them before ' +
  'running any shell command in this session.\n\n---\n\n';

/**
 * Read the rules file and write it to stdout. Never throws, never exits non-zero.
 *
 * @returns {void}
 */
function emitCommandRules() {
  let contents;
  try {
    contents = fs.readFileSync(RULES_FILE, 'utf8');
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    process.stderr.write(`emit-command-rules: could not read ${RULES_FILE}: ${message}\n`);
    return;
  }
  process.stdout.write(PREAMBLE + contents);
}

emitCommandRules();
