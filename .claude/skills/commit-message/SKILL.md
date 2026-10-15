---
name: commit-message
description: Drafts a commit message for the currently staged changes and, after approval, writes it to .git/COMMIT_EDITMSG without committing. Use when the developer asks for "a commit message" or says they are ready to commit what is staged.
model: claude-haiku-4-5-20251001
---

# Commit Message

> **Model pin:** Haiku 4.5 (`claude-haiku-4-5-20251001`): a small staged diff turned into a fixed template.
> Claude Code applies the override only for the rest of the current turn, and skips it when an
> `availableModels` allowlist does not allow the model.

Drafts a message for **only what is staged**, in the format from `CLAUDE.md` § Git conventions, and leaves
the commit itself to the developer (`CLAUDE.md` R1).

## Flow

**Command rules:** they are injected at session start from `CLAUDE.command-rules.md`. If they are not in your
context, read that file before running any shell command. Run each command as its own Bash call.

0. **Announce the model pin** in one short line: "This skill is pinned to Haiku 4.5."

1. **Gate: branch and issue number.** Run `git branch --show-current`.
   - If it is `main`, stop: there is nothing to commit to on `main` (R1).
   - Read the issue number `N` from the branch name `{category}/{N}-{slug}`. If the name does not match that
     shape, stop and tell the developer the branch breaks R2; do not guess a number.

2. **Gather staged changes only.** Run `git diff --cached`. If it prints nothing, stop and say nothing is
   staged. Never fall back to unstaged changes or the whole branch.

3. **Map changes to the issue.** By default every staged change belongs to issue `N`. A change that clearly
   belongs to no issue goes in a separate "Unrelated / No Issue" section; never silently drop it. If the
   developer wants a different issue number in `Refs:`, do not accept it silently: say it breaks R2 and ask
   whether to proceed for this one commit.

4. **Pick the shape.**
   - Single line `{type}[{scope}]: {description} (#N)` only when there is one small change needing no
     explanation.
   - Otherwise a body: subject without the `(#N)`, a paragraph on what changed and why (plus the
     "Unrelated / No Issue" section if any), then a `Refs: #N` footer.

5. **Compose.** `{type}` and `{scope}` come from `CLAUDE.md` § Git conventions (omit `[scope]` if none fits).
   Present tense. Count the subject line yourself and keep it under 72 characters. Add `!` and a
   `BREAKING CHANGE:` footer only for a breaking change.

6. **Approval gate.** Show the full draft, the subject length, the issue number and which staged files it
   covers. Ask with `AskUserQuestion` (not free text) with exactly: **"Write to .git/COMMIT_EDITMSG"**,
   **"Edit the draft"**, **"Cancel"**. Write nothing until the first is chosen.

7. **On approval, write the message** to `.git/COMMIT_EDITMSG` and stop. Never run `git add`, `git commit`
   or `git push`.

8. **Report back:** the file was written and nothing was committed, which issue it refs, and any
   "Unrelated / No Issue" items. The developer reviews and commits it themselves.
