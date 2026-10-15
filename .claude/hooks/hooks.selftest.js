// @ts-check
'use strict';

/**
 * Self-test for the Claude Code setup: both hooks, settings.json and skill front matter.
 *
 * Run from anywhere:  node .claude/hooks/hooks.selftest.js
 * Prints one PASS/FAIL line per check and exits 1 if any check fails.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
// The cd-into-root rule compares against process.cwd(), so run from the repo root.
process.chdir(ROOT);

const guard = require('./guard-bash-command.js');
const GUARD = path.join(__dirname, 'guard-bash-command.js');
const EMIT = path.join(__dirname, 'emit-command-rules.js');

let passed = 0;
let failed = 0;

/**
 * @param {string} name
 * @param {boolean} ok
 * @param {string} [detail]
 */
function check(name, ok, detail = '') {
  if (ok) {
    passed += 1;
    console.log(`PASS  ${name}`);
  } else {
    failed += 1;
    console.log(`FAIL  ${name}${detail ? `  -> ${detail}` : ''}`);
  }
}

// --- guard-bash-command: commands that must be ALLOWED ---
const ALLOW = [
  'git status',
  'git diff --cached',
  'git log --oneline -5',
  'npm run lint --prefix frontend',
  'ls -la',
  'cd backend',
  'gh issue view 3 --repo mrlhfz/badge-by-badge | head -5',
  'git log --oneline | rg fix',
  'echo "a && b; c"',
  "cat > temp/note.md <<'EOF'\nhello\nEOF\n",
  'git commit -m "subject\n\nbody line one\nbody line two"',
];
for (const cmd of ALLOW) {
  const reason = guard.evaluate(cmd);
  check(`allow: ${JSON.stringify(cmd)}`, reason === null, reason || '');
}

// --- guard-bash-command: commands that must be DENIED ---
/** @type {Array<[string, string]>} */
const DENY = [
  ['cat package.json', 'text/search utility'],
  ['grep foo src/App.tsx', 'text/search utility'],
  ['rg TODO', 'text/search utility'],
  ['grep -rn foo', 'text/search utility'],
  ['find . -name x', 'text/search utility'],
  ['sed -n 1,5p README.md', 'text/search utility'],
  ['head -n 5 CLAUDE.md', 'text/search utility'],
  ['git status && git diff', 'chains multiple commands'],
  ['git status; git diff', 'chains multiple commands'],
  ['git status\ngit diff', 'chains multiple commands'],
  [`cd "${ROOT}"`, 'into the repo root'],
  ['cd .', 'into the repo root'],
];
for (const [cmd, expected] of DENY) {
  const reason = guard.evaluate(cmd);
  check(
    `deny:  ${JSON.stringify(cmd)}`,
    typeof reason === 'string' && reason.includes(expected),
    String(reason)
  );
}

// --- guard-bash-command: end to end through stdin ---
/**
 * @param {string} input
 */
function runGuard(input) {
  return spawnSync(process.execPath, [GUARD], { input, encoding: 'utf8', cwd: ROOT });
}

const denied = runGuard(JSON.stringify({ tool_input: { command: 'git status && git diff' } }));
let decision = '';
try {
  decision = JSON.parse(denied.stdout).hookSpecificOutput.permissionDecision;
} catch (_e) {
  /* leave empty */
}
check('e2e: violation prints a deny decision and exits 0', decision === 'deny' && denied.status === 0);

const allowed = runGuard(JSON.stringify({ tool_input: { command: 'git status' } }));
check('e2e: clean command prints nothing and exits 0', allowed.stdout === '' && allowed.status === 0);

const garbage = runGuard('not json at all');
check('e2e: malformed JSON fails open (silent, exit 0)', garbage.stdout === '' && garbage.status === 0);

const empty = runGuard('');
check('e2e: empty stdin fails open (silent, exit 0)', empty.stdout === '' && empty.status === 0);

// --- emit-command-rules ---
const emitted = spawnSync(process.execPath, [EMIT], { encoding: 'utf8', cwd: os_tmp() });
check(
  'emit-command-rules: prints the preamble and the rules file, exit 0',
  emitted.status === 0 &&
    emitted.stdout.startsWith("The following are this project's command-execution rules") &&
    emitted.stdout.includes('# Command Execution Rules')
);

/** A directory that is not the repo root, to prove the hook ignores the working directory. */
function os_tmp() {
  return require('os').tmpdir();
}

// --- settings.json ---
const settingsPath = path.join(ROOT, '.claude', 'settings.json');
/** @type {any} */
let settings = null;
try {
  settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
} catch (_e) {
  /* checked below */
}
check('settings.json: valid JSON', settings !== null);
if (settings) {
  const raw = fs.readFileSync(settingsPath, 'utf8');
  check('settings.json: SessionStart hook wired', Array.isArray(settings.hooks && settings.hooks.SessionStart));
  check('settings.json: PreToolUse hook wired to Bash', JSON.stringify(settings.hooks && settings.hooks.PreToolUse).includes('"Bash"'));
  check('settings.json: no personal machine paths', !/[A-Za-z]:[\\/]|\/Users\/|\/home\/|AppData/.test(raw));
  check('settings.json: no additionalDirectories', !('additionalDirectories' in (settings.permissions || {})));
  check('settings.json: allowlist stays small (<= 10 entries)', (settings.permissions.allow || []).length <= 10);
  const hookFiles = raw.match(/\.claude\/hooks\/[\w.-]+\.js/g) || [];
  check(
    'settings.json: every hook script it names exists',
    hookFiles.length >= 2 && hookFiles.every((f) => fs.existsSync(path.join(ROOT, f)))
  );
}
check('no settings.local.json was created', !fs.existsSync(path.join(ROOT, '.claude', 'settings.local.json')));

// --- skills: front matter ---
const skillsDir = path.join(ROOT, '.claude', 'skills');
const skillNames = fs.existsSync(skillsDir)
  ? fs.readdirSync(skillsDir).filter((d) => fs.statSync(path.join(skillsDir, d)).isDirectory())
  : [];
for (const name of skillNames) {
  const file = path.join(skillsDir, name, 'SKILL.md');
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n') : '';
  const fm = /^---\n([\s\S]*?)\n---\n/.exec(text);
  const body = fm ? fm[1] : '';
  check(
    `skill ${name}: front matter has matching name and a description`,
    !!fm && new RegExp(`^name: ${name}$`, 'm').test(body) && /^description: .{20,}$/m.test(body)
  );
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
