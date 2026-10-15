---
name: code-review
description: Reviews the current branch's full diff against main across 11 fixed dimensions (FastAPI, React, TypeScript, Supabase, project rules) and writes findings to temp/code-review-{n}.md. Use when the developer asks to "review this branch" or "code review", or before opening a PR.
model: claude-opus-5-5
---

# Code Review

> **Model pin:** Opus 5.5 (`claude-opus-5-5`): a judgment-heavy review where a missed finding costs more than
> the tokens. The override applies only for the rest of the current turn and is skipped when an
> `availableModels` allowlist does not allow the model.

Acts as a senior full-stack reviewer. The developer is learning (`CLAUDE.md` R6), so every finding says what is
wrong, why it matters, and offers fix **options** as hints or small snippets, never a full rewrite. This skill
writes only `temp/code-review-{n}.md` (gitignored). It never writes to GitHub or `.git`.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your
context, read that file first. Run each command as its own Bash call.

0. **Announce the model pin** in one short line: "This skill is pinned to Opus 5.5."

1. **Gate: branch.** Run `git branch --show-current`. If it is `main`, stop: a review needs a feature branch.
   Read the issue number `N` from the branch name `{category}/{N}-{slug}`.

2. **Gather context.**
   - Read `branch-tasks.txt` with the Read tool (scope), and `CLAUDE.md` (the rules to review against).
   - `git diff main...HEAD` (the full diff)
   - `git log main..HEAD --oneline` (commit hygiene)
   - `git log -1 --format=%H` (the reviewed commit)
   - Open the files the diff touches whenever the diff alone hides what matters: the model a route returns, the
     migration that creates a table, the component a prop flows into, `.env.example` for any new env var.

3. **Evaluate every dimension:**
   1. **Intent alignment:** does it match issue `N`? Scope creep? Edge and error paths consistent with the goal?
   2. **Architecture and design:** routes thin and logic elsewhere; database access through SQLAlchemy sessions;
      React state kept as local as it can be; no coupling that blocks the planned growth after the MVP.
   3. **Types and validation:** TypeScript strict with no unwarranted `any` or `as`; Pydantic models on every
      request and response; Python type hints on public functions.
   4. **Correctness:** off-by-one, unhandled nulls, missing `await`, wrong HTTP status codes, React hook
      dependency arrays, error paths that swallow exceptions.
   5. **Tests:** new behavior covered by pytest (backend) or Vitest (frontend); tests assert behavior, not
      implementation; no over-mocking.
   6. **Performance:** N+1 queries, missing pagination on list endpoints, avoidable re-renders, unbounded
      payloads.
   7. **Security and data integrity:** every endpoint checks the caller's role (Admin, Leader, Scout);
      RLS on every new table (R4); no secrets in the frontend or in logs (R3); CORS stays restricted; raw SQL
      is parameterized; user input is validated.
   8. **Readability:** intention-revealing names, comments that explain why, no dead code, debug prints or
      commented-out blocks.
   9. **Project rule compliance:** R1 to R6 in `CLAUDE.md`. Every new env var is in the matching
      `.env.example`; roles and statuses come from the single enum (R5); each new table has RLS in its
      migration (R4); commit format and scopes match `CLAUDE.md`; new files are in the right folder.
   10. **Dependencies:** each new package in `requirements.txt`, `requirements-dev.txt` or `package.json` is
       justified, pinned the way the file already pins, and not duplicating something already installed.
   11. **Git and commit hygiene:** the branch number equals the issue number in the commits' `Refs:` and in
       `branch-tasks.txt` (R2); messages follow the format; commits are atomic; no `.env`, `temp/` or build
       artifacts committed. A branch/issue mismatch is a finding.

4. **Write `temp/code-review-{N}.md`** in this shape. A re-run overwrites the file and renumbers findings
   from 1.

   ```text
   # Code Review for {branch-name}

   Reviewed: {commit sha} on {today's date}

   ## Verdict: {✅ Approve | 💬 Comment | 🚫 Request Changes}

   {one-paragraph summary}

   ## Findings

   ### Finding {index}: {short title}

   **Status**: ⏳ Open
   **Severity**: {🔴 Critical | 🟡 Warning | 🔵 Suggestion}
   **Dimension**: {number and name}

   **Finding**: {what is wrong}
   **Why it matters**: {the consequence}

   **Locations**
   - L.{index}.1: {path}:{line}

   **Recommended Fixes**
   - F.{index}.1: {option, as a hint or small snippet}
   ```

   Verdict rule: any 🔴 or 🟡 means Request Changes; only 🔵 means Comment; no findings means Approve (keep
   `## Findings` with the single line `No findings.`). Order findings most severe first.

5. **Report back:** confirm the file path, the verdict, and the finding counts by severity.

## Marking a finding resolved

When the developer says a finding is fixed, skipped or needs no change, check that the fix is committed for
the `fixed` outcome: `git status --porcelain` must show nothing for the files in its Locations. Then replace
`**Status**: ⏳ Open` with `✅ RESOLVED (fixed)`, `⏭️ SKIPPED (skipped)` or `ℹ️ NO CHANGE NEEDED
(no_change_needed)`, and add an `**Outcome**:` line naming the applied `F.{index}.{n}` option or the
developer's reason. Leave every other field unchanged.
