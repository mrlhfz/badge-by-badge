---
name: pr-commit-message
description: Drafts the squash-merge commit message for the whole current branch (git diff main...HEAD, every commit since main) and writes it to temp/pr-commit-message-{N}.md for pasting into the squash-merge box. Use when the developer asks for the squash commit message, the merge commit message, or the commit message for the PR. For a message about only the staged changes, use commit-message instead.
model: claude-sonnet-5-5
---

# PR Commit Message

> **Model pin:** Sonnet 5.5 (`claude-sonnet-5-5`): it summarizes a whole branch, as `pr-message` does. The override
> applies only for the rest of the current turn and is skipped when an `availableModels` allowlist does not allow
> the model.

Drafts the message GitHub uses when the PR is squash-merged. The squash commit on `main` takes the PR title as
its subject, and this message as its body. This skill only writes a draft file. It never writes to GitHub or
`.git`, and it never merges (R1).

Scope split: `commit-message` covers **staged changes** for a single commit. This skill covers **the whole branch**
for the squash merge.

> **Sync rule:** The format here must match `CLAUDE.md` § Git conventions. The gates must match steps 1 to 3 of
> `.claude/skills/pr-message/SKILL.md`. The output path must match what `pr-message` step 7b and `pr-create` expect
> (`temp/pr-commit-message-{N}.md`). If any of those change shape, review this file, and vice versa.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your context,
read that file before running any shell command. Run each command as its own Bash call.

0. **Announce the model pin** in one short line: "This skill is pinned to Sonnet 5.5."

1. **Gate: branch.** Run `git branch --show-current`. If it is `main`, stop: there is no squash to draft on `main`.
   Read the issue number `N` from the branch name `{category}/{N}-{slug}`. If the name does not match, stop and
   report the R2 breach. Never guess a number.

2. **Gate: clean tree.** Run `git diff`, then `git diff --cached`. If either prints anything, stop and ask the
   developer to commit or stash first, so the draft matches what will be merged.

3. **Gate: branch-tasks.txt is current.** Read `branch-tasks.txt` with the Read tool.
   - If it is missing, or does not list issue `N`, stop and tell the developer to run `update-branch-tasks`.
   - If it lists any issue other than `N`, stop and report the mismatch (R2). The developer either moves that work
     to its own branch or confirms the mismatch for this squash.

4. **Gather the scope.** Run `git diff main...HEAD` and `git log main..HEAD --oneline`. The draft must describe
   every change in that diff.

5. **Map changes to the issue.** Everything belongs to issue `N`. A change that belongs to no issue goes in a
   clearly labeled "Unrelated / No Issue" section; never silently drop it.

6. **Compose the message** per `CLAUDE.md` § Git conventions:
   - **Subject:** `{type}[{scope}]: {description}`. Type from the Types list, scope from the Scopes list (omit
     `[scope]` if none fits). Present tense. **No** `(#...)` suffix: GitHub appends the PR number on squash. Count
     the subject yourself and keep it **under 72 characters**. Add `!` after the type and a `BREAKING CHANGE:`
     footer only for a breaking change.
   - **Body:** a blank line, then a paragraph on what changed and why, then the "Unrelated / No Issue" section if
     any.
   - **Footer:** a blank line, then `Refs: #N`.
   - **Title check:** if `temp/pr-message-{N}.md` exists, read its title line. If its title differs from this
     subject, warn the developer: the squash commit takes the **PR title**, so the PR title and this subject must
     match. Ask them to fix whichever is wrong.

7. **Write the draft** to `temp/pr-commit-message-{N}.md`, overwriting any earlier draft. The file stays until the
   developer deletes it. Do not write to `.git/`, and do not run `git add`, `git commit`, `git push` or any GitHub
   command.

8. **Report back:**
   - The path written, and the subject with its character count.
   - The issue `N` it refs, and any "Unrelated / No Issue" items.
   - A reminder to paste the file's contents into the squash-merge box on the PR page, and to rerun this skill if
     the branch changes after the draft is written.
