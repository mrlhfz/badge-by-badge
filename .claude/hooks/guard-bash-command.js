// @ts-check
'use strict';

/**
 * PreToolUse hook (matcher `Bash`): enforce the three command rules that can be
 * decided from the command text alone (see CLAUDE.command-rules.md):
 *
 *   1. A text/search utility (grep, rg, cat, head, tail, nl, tac, sed, awk, find)
 *      pointed at a file/glob path, or walking the tree with no path
 *      (`rg PATTERN`, `grep -r PATTERN`). Piping another command's stdout into the
 *      utility is allowed.
 *   2. `cd` / `Set-Location` into the repo root (already the working directory).
 *   3. Chaining with `&&`, `;` or a bare newline. Pipes are not chaining; heredoc
 *      bodies and multi-line quoted strings are exempt.
 *
 * On a violation it prints a `deny` decision with a corrective reason. On no
 * violation, or on ANY error, it prints nothing and exits 0: a broken hook must
 * never wedge the Bash tool. The judgment rules in CLAUDE.command-rules.md are
 * not checked here; they rely on the SessionStart injection.
 *
 * Wired in .claude/settings.json under hooks.PreToolUse.
 */

const fs = require('fs');
const path = require('path');

// --- Constants ---

/** Utilities that must not read the filesystem; Read / Grep / Glob cover those cases. */
const FILE_TOOLS = new Set(['grep', 'rg', 'cat', 'head', 'tail', 'nl', 'tac', 'sed', 'awk', 'find']);

/** Utilities whose FIRST bare argument is a pattern or script, not a file. */
const SCRIPT_FIRST_TOOLS = new Set(['grep', 'rg', 'sed', 'awk']);

/** A standalone redirection token; it and the target token after it are dropped. */
const REDIRECT_RE = /^(?:[0-9]*(?:>>|>|<<<|<<|<)&?|&>>?)$/;

/** A redirection written with its target attached, e.g. `>out.txt` or `2>&1`. */
const INLINE_REDIRECT_RE = /^(?:[0-9]*(?:>>|>|<)|&>>?)\S/;

/** grep/rg options that consume the next token as a value, not a file. */
const GREP_VALUE_OPTS = /^(?:-e|-f|--regexp|--file|--include|--exclude|--exclude-dir)$/;

// --- Deny reasons ---

/**
 * @param {string} tool The offending utility name.
 * @returns {string}
 */
function reasonFileTool(tool) {
  return (
    `Blocked by guard-bash-command (CLAUDE.command-rules.md): this command runs the ` +
    `text/search utility "${tool}" to read the filesystem (a file/glob path argument, ` +
    `or a recursive walk of the working tree). Use a dedicated tool instead: Read to ` +
    `view a file, Grep to search file contents, Glob to find files by name. Piping ` +
    `another command's stdout into "${tool}" to filter it is fine and is not blocked.`
  );
}

const REASON_CD_ROOT =
  `Blocked by guard-bash-command (CLAUDE.command-rules.md): this command "cd"s into the ` +
  `repo root, which is already the working directory. Drop the "cd <root>" (and any ` +
  `"&&" or ";" joining it to the real command) and run the command on its own. A "cd" ` +
  `to a non-root path is still allowed.`;

/**
 * @param {'&&' | ';' | 'newline'} sep Which separator was found.
 * @returns {string}
 */
function reasonChaining(sep) {
  const shown = sep === 'newline' ? 'a newline' : `"${sep}"`;
  return (
    `Blocked by guard-bash-command (CLAUDE.command-rules.md): this command chains ` +
    `multiple commands with ${shown}. Issue each command as its own Bash tool call so ` +
    `it can be matched against permissions.allow. Pipes ("|") are fine. Heredoc file ` +
    `writes and multi-line quoted strings are exempt; if this was one of those and was ` +
    `misdetected, simplify the quoting and retry.`
  );
}

// --- Tokenizer ---

/**
 * Single-pass scan that understands single quotes, double quotes, backslash
 * escapes and heredoc bodies. Splits the command into segments at every TOP-LEVEL
 * `|`, `||`, `&&`, `;` and bare newline, and reports the first chaining separator
 * (`&&`, `;` or a content-bearing newline). `|` and `||` split segments but are not
 * chaining violations. Heredoc bodies are dropped so they never look like arguments.
 *
 * `pipeTargets[k]` is true when segment k reads its stdin from a `|`.
 *
 * @param {string} cmd
 * @returns {{segments: string[], chainSeparator: ('&&' | ';' | 'newline' | null), pipeTargets: boolean[]}}
 */
function scanTopLevel(cmd) {
  /** @type {string[]} */
  const segments = [];
  /** @type {boolean[]} */
  const pipeTargets = [];
  let cur = '';
  /** @type {'&&' | ';' | 'newline' | null} */
  let chainSeparator = null;
  /** @type {'|' | '||' | '&&' | ';' | 'newline' | null} */
  let prevSep = null;
  let sQuote = false;
  let dQuote = false;
  let i = 0;
  const n = cmd.length;

  /** @param {'|' | '||' | '&&' | ';' | 'newline' | null} sepAfter */
  const endSegment = (sepAfter) => {
    segments.push(cur);
    pipeTargets.push(prevSep === '|');
    cur = '';
    prevSep = sepAfter;
  };

  while (i < n) {
    const c = cmd[i];

    if (sQuote) {
      cur += c;
      if (c === "'") sQuote = false;
      i += 1;
      continue;
    }

    if (dQuote) {
      if (c === '\\' && i + 1 < n) {
        cur += c + cmd[i + 1];
        i += 2;
        continue;
      }
      cur += c;
      if (c === '"') dQuote = false;
      i += 1;
      continue;
    }

    if (c === '\\' && i + 1 < n) {
      cur += c + cmd[i + 1];
      i += 2;
      continue;
    }
    if (c === "'") {
      sQuote = true;
      cur += c;
      i += 1;
      continue;
    }
    if (c === '"') {
      dQuote = true;
      cur += c;
      i += 1;
      continue;
    }

    // Heredoc introducer `<<` or `<<-` (not the `<<<` here-string).
    if (c === '<' && cmd[i + 1] === '<' && cmd[i + 2] !== '<') {
      let j = i + 2;
      let dash = false;
      if (cmd[j] === '-') {
        dash = true;
        j += 1;
      }
      while (j < n && cmd[j] !== '\n' && /\s/.test(cmd[j])) j += 1;

      let quote = '';
      if (cmd[j] === '"' || cmd[j] === "'") {
        quote = cmd[j];
        j += 1;
      }
      let delim = '';
      if (quote) {
        const close = cmd.indexOf(quote, j);
        delim = close === -1 ? cmd.slice(j) : cmd.slice(j, close);
        j = close === -1 ? n : close + 1;
      } else {
        const m = /^[A-Za-z_][A-Za-z0-9_]*/.exec(cmd.slice(j, j + 256));
        if (m) {
          delim = m[0];
          j += m[0].length;
        }
      }

      cur += ' ';
      if (!delim) {
        i = j;
        continue;
      }

      // Skip the rest of the introducer line, then the body up to the terminator line.
      const introEnd = cmd.indexOf('\n', j);
      if (introEnd === -1) {
        i = n;
        continue;
      }
      let k = introEnd + 1;
      while (k < n) {
        let lineEnd = cmd.indexOf('\n', k);
        if (lineEnd === -1) lineEnd = n;
        const line = cmd.slice(k, lineEnd).replace(/\r$/, '');
        const compare = dash ? line.replace(/^\t+/, '') : line;
        k = lineEnd < n ? lineEnd + 1 : n;
        if (compare === delim) break;
      }
      i = k;
      continue;
    }

    if (c === '|' && cmd[i + 1] === '|') {
      endSegment('||');
      i += 2;
      continue;
    }
    if (c === '|') {
      endSegment('|');
      i += 1;
      continue;
    }
    if (c === '&' && cmd[i + 1] === '&') {
      if (!chainSeparator) chainSeparator = '&&';
      endSegment('&&');
      i += 2;
      continue;
    }
    if (c === ';') {
      if (!chainSeparator) chainSeparator = ';';
      endSegment(';');
      i += 1;
      continue;
    }
    if (c === '\n') {
      // A chain only when real content sits on both sides (blank lines do not count).
      const before = cur.trim();
      const after = cmd.slice(i + 1);
      if (before && /\S/.test(after) && !chainSeparator) chainSeparator = 'newline';
      endSegment('newline');
      i += 1;
      continue;
    }

    cur += c;
    i += 1;
  }

  endSegment(null);
  return { segments, chainSeparator, pipeTargets };
}

/**
 * Split one segment into shell words, honoring quotes and backslash escapes.
 *
 * @param {string} segment
 * @returns {string[]}
 */
function tokenizeWords(segment) {
  /** @type {string[]} */
  const words = [];
  let cur = '';
  let has = false;
  let sQuote = false;
  let dQuote = false;

  for (let i = 0; i < segment.length; i += 1) {
    const c = segment[i];

    if (sQuote) {
      if (c === "'") sQuote = false;
      else {
        cur += c;
        has = true;
      }
      continue;
    }
    if (dQuote) {
      if (c === '\\' && i + 1 < segment.length && '"\\$`'.indexOf(segment[i + 1]) !== -1) {
        cur += segment[i + 1];
        has = true;
        i += 1;
      } else if (c === '"') {
        dQuote = false;
      } else {
        cur += c;
        has = true;
      }
      continue;
    }
    if (c === '\\' && i + 1 < segment.length) {
      cur += segment[i + 1];
      has = true;
      i += 1;
      continue;
    }
    if (c === "'") {
      sQuote = true;
      has = true;
      continue;
    }
    if (c === '"') {
      dQuote = true;
      has = true;
      continue;
    }
    if (/\s/.test(c)) {
      if (has) {
        words.push(cur);
        cur = '';
        has = false;
      }
      continue;
    }
    cur += c;
    has = true;
  }

  if (has) words.push(cur);
  return words;
}

// --- Detection helpers ---

/**
 * Drop leading `VAR=value` tokens so `FOO=bar grep x f` is still seen as `grep`.
 *
 * @param {string[]} words
 * @returns {string[]}
 */
function stripEnvPrefix(words) {
  let start = 0;
  while (start < words.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(words[start])) start += 1;
  return start === 0 ? words : words.slice(start);
}

/**
 * Remove redirection operators and their targets from an argument list.
 *
 * @param {string[]} args
 * @returns {string[]}
 */
function stripRedirects(args) {
  /** @type {string[]} */
  const out = [];
  for (let i = 0; i < args.length; i += 1) {
    if (REDIRECT_RE.test(args[i])) {
      i += 1; // also skip the target token
      continue;
    }
    if (INLINE_REDIRECT_RE.test(args[i])) continue;
    out.push(args[i]);
  }
  return out;
}

/**
 * Basename of a command word, so `/usr/bin/grep` still resolves to `grep`.
 *
 * @param {string} word
 * @returns {string}
 */
function commandBasename(word) {
  const normalized = word.replace(/\\/g, '/');
  const idx = normalized.lastIndexOf('/');
  return idx === -1 ? normalized : normalized.slice(idx + 1);
}

/**
 * Whether a segment is a text/search utility pointed at a file path, or walking
 * the tree on its own.
 *
 * @param {string[]} rawWords Words of one segment.
 * @param {boolean} [pipedInput] True when the segment reads its stdin from a pipe.
 * @returns {string | null} The offending tool name, or null if fine.
 */
function fileToolViolation(rawWords, pipedInput = false) {
  const words = stripEnvPrefix(rawWords);
  if (words.length === 0) return null;

  const tool = commandBasename(words[0]);
  if (!FILE_TOOLS.has(tool)) return null;

  const args = stripRedirects(words.slice(1));

  // `find` always works on a path (explicit or the implicit `.`).
  if (tool === 'find') return args.length > 0 ? tool : null;

  if (tool === 'grep' || tool === 'rg') {
    const valueConsumed = new Set();
    for (let i = 0; i < args.length; i += 1) {
      if (GREP_VALUE_OPTS.test(args[i])) valueConsumed.add(i + 1);
    }
    const bare = args.filter(
      (a, i) => !valueConsumed.has(i) && !a.startsWith('-') && !/^[0-9]+$/.test(a)
    );
    const inlinePattern = args.some((a) => /^(?:-e|-f)$/.test(a) || /^--(?:regexp|file)=/.test(a));
    // Without -e/-f, the first bare word IS the pattern.
    const fileCount = inlinePattern ? bare.length : Math.max(0, bare.length - 1);
    if (fileCount >= 1) return tool;

    // No explicit path: fine when filtering piped stdin, not when walking the tree.
    const hasPattern = inlinePattern || bare.length >= 1;
    if (pipedInput || !hasPattern) return null;
    const grepRecursive =
      tool === 'grep' &&
      args.some((a) => a === '--recursive' || /^-[A-Za-z]*[rR][A-Za-z]*$/.test(a));
    if (tool === 'rg' || grepRecursive) return tool;
    return null;
  }

  if (SCRIPT_FIRST_TOOLS.has(tool)) {
    // sed / awk: the first bare word is the script; a file needs a second.
    const bare = args.filter((a) => !a.startsWith('-') && !/^[0-9]+$/.test(a));
    return bare.length >= 2 ? tool : null;
  }

  // cat / head / tail / nl / tac: any bare, non-numeric argument is a file name.
  const bare = args.filter((a) => !a.startsWith('-') && !/^[0-9]+$/.test(a));
  return bare.length >= 1 ? tool : null;
}

/**
 * Normalize a path for comparison: forward slashes, lowercase, MSYS `/c/x` to
 * `c:/x`, no trailing slash.
 *
 * @param {string} p
 * @returns {string}
 */
function normalizePath(p) {
  let s = p.trim().replace(/\\/g, '/').toLowerCase();
  s = s.replace(/^\/([a-z])\//, '$1:/');
  s = s.replace(/\/+$/, '');
  return s;
}

/**
 * Whether a segment is a `cd` / `Set-Location` whose target is the repo root.
 *
 * @param {string[]} rawWords
 * @returns {boolean}
 */
function cdRootViolation(rawWords) {
  const words = stripEnvPrefix(rawWords);
  if (words.length === 0) return false;

  const head = words[0].toLowerCase();
  if (head !== 'cd' && head !== 'set-location') return false;

  const target = words.slice(1).find((w) => !w.startsWith('-'));
  if (!target) return false; // bare `cd` goes home, not to the repo root
  if (/[$`]/.test(target)) return false; // variable or substitution: not resolvable
  if (target === '.' || target === './') return true;

  const root = normalizePath(process.cwd());
  let resolved = normalizePath(target);
  const isAbsolute = /^[a-z]:\//.test(resolved) || resolved.startsWith('/');
  if (!isAbsolute) resolved = normalizePath(path.resolve(process.cwd(), target));
  return resolved === root;
}

// --- Evaluation ---

/**
 * Evaluate a command string against the three enforced rules.
 *
 * @param {unknown} command The value of `tool_input.command`.
 * @returns {string | null} A deny reason, or null when the command is fine.
 */
function evaluate(command) {
  if (typeof command !== 'string' || command.trim() === '') return null;

  const { segments, chainSeparator, pipeTargets } = scanTopLevel(command);
  const wordsPerSegment = segments.map(tokenizeWords);

  for (let i = 0; i < wordsPerSegment.length; i += 1) {
    const tool = fileToolViolation(wordsPerSegment[i], pipeTargets[i]);
    if (tool) return reasonFileTool(tool);
  }
  for (const words of wordsPerSegment) {
    if (cdRootViolation(words)) return REASON_CD_ROOT;
  }
  if (chainSeparator) return reasonChaining(chainSeparator);
  return null;
}

// --- Main ---

/**
 * Read the PreToolUse payload from stdin, evaluate the command, and print a deny
 * decision when a rule is violated. Never throws and never exits non-zero.
 *
 * @returns {void}
 */
function main() {
  /** @type {string | null} */
  let reason = null;
  try {
    const raw = fs.readFileSync(0, 'utf8');
    if (!raw) return;
    const payload = JSON.parse(raw);
    const command = payload && payload.tool_input ? payload.tool_input.command : undefined;
    reason = evaluate(command);
  } catch (_err) {
    return; // a broken hook must never wedge the Bash tool
  }
  if (!reason) return;

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny',
        permissionDecisionReason: reason,
      },
    })
  );
}

if (require.main === module) main();

// Exported for hooks.selftest.js.
module.exports = { evaluate, scanTopLevel, tokenizeWords, fileToolViolation, cdRootViolation };
