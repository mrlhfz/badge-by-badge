---
name: update-branch-tasks
description: Regenerates branch-tasks.txt from the issue number in the branch name plus the issues referenced by commits made only on this branch, after the developer approves the list. Use when asked to update or sync branch-tasks.txt, or after resuming or switching branches.
model: claude-haiku-4-5-20251001
---

# Update Branch Tasks

> **Model pin:** Haiku 4.5 (`claude-haiku-4-5-20251001`): a mechanical extract-and-write of issue numbers.
> The override applies only for the rest of the current turn and is skipped when an `availableModels`
> allowlist does not allow the model.

Rebuilds `branch-tasks.txt` (gitignored, never committed) so the issues `pr-message` and `code-review` read
cannot drift from the branch. The file's current contents are ignored; the new list replaces it.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your
context, read that file first. Run each command as its own Bash call.

0. **Announce the model pin** in one short line: "This skill is pinned to Haiku 4.5." When another skill
   runs this one as a step, announce the pin in one line only.

1. **Branch and number.** Run `git branch --show-current`. If it is `main`, stop. Read the issue number `N`
   from the branch name `{category}/{N}-{slug}`; if the name does not match, stop and report that it breaks
   R2 in `CLAUDE.md`. Never guess.

2. **Commits made only on this branch.** Run `git log main..HEAD --first-parent --no-merges` (full messages,
   not `--oneline`, because `Refs:` footers live in the body). `main..HEAD` excludes commits already on
   `main`; `--first-parent` and `--no-merges` skip anything merged in from elsewhere.

3. **Extract issue numbers** using only the two conventions from `CLAUDE.md`: a trailing `(#id)` on a
   single-line subject, and `Refs: #id` footer lines. Ignore any other `#123` mention. Union the results with
   `N` into one set.

4. **Validate** each number: `gh issue view {number} --repo mrlhfz/badge-by-badge --json number,title,state`.
   Drop and report any number that does not resolve.

5. **Approval gate.** Show the full new list (ascending, with titles). Flag every number other than `N` as a
   warning: R2 says one branch is one issue. Ask with `AskUserQuestion`: **"Overwrite branch-tasks.txt"**,
   **"Change the list"**, **"Cancel"**. Never infer approval from silence.

6. **On approval, overwrite `branch-tasks.txt`** at the repo root, one
   `https://github.com/mrlhfz/badge-by-badge/issues/{number}` per line, ascending. The file is gitignored, so
   R1 does not restrict writing it on any branch.

7. **Report back:** the list written, any numbers dropped, and any warnings about numbers other than `N`.
