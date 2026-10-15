# Command Execution Rules

> **Sync rule:** this file is the authoritative home for how Claude runs shell commands in this repo. Root
> `CLAUDE.md` § Command Execution is a pointer to it, not a second copy. Enforcement has three layers:
> (1) a `SessionStart` hook (`.claude/hooks/emit-command-rules.js`) injects this file once per session
> boundary (startup / resume / clear / compact); (2) each skill carries a one-line fallback to re-read this
> file if the rules are not in context; (3) a `PreToolUse` hook on `Bash`
> (`.claude/hooks/guard-bash-command.js`) hard-blocks the three rules marked **[hook]** below, with a
> corrective reason. The other rules rely on layers 1 and 2.

`.claude/settings.json` `permissions.allow` matches patterns against the literal command string. A command
that follows these rules matches reliably; one that does not triggers avoidable permission prompts.

## Rules

1. **[hook] One command per Bash call.** Do not chain with `&&`, `;` or a bare newline. Pipes (`|`) are fine.
   Exempt: heredoc file writes and multi-line quoted strings (for example a commit-message body).
2. **[hook] Do not `cd` into the repo root.** It is already the working directory. A `cd` to another path
   (such as `backend/`) is allowed; `cd` back to the root immediately afterwards.
3. **[hook] Use the dedicated file tools.** Use Read, Grep, Glob, Edit and Write instead of `cat`, `head`,
   `tail`, `grep`, `rg`, `sed`, `awk` or `find` on files. Piping another command's output into a filter
   (`gh issue view 3 | head -5`) is fine.
4. **Keep commands on one line when they can be.** Heredocs, backslash continuations and multi-line inline
   scripts do not match allowlist patterns reliably. Genuinely multi-line content (a file body) is exempt.
5. **Multi-line text for `gh` goes through a file.** Write the body to `temp/`, pass `--body-file`, then
   delete the file. Never inline a multi-line body in the command.
6. **Use the project's own scripts.** Frontend: `npm run <script> --prefix frontend`. Backend: run inside the
   project virtual environment; if it is not active, ask the developer. Never `pip install` or
   `npm install -g` as a workaround.
7. **Never read `.env` files.** They hold secrets. Check variable names in `.env.example` instead.
8. **When a command is refused or fails twice, stop and ask** instead of trying variations.
