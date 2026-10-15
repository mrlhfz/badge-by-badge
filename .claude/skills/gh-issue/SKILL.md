---
name: gh-issue
description: Creates a GitHub issue for mrlhfz/badge-by-badge with a validated title and body, adds it to the Project as Backlog, then optionally creates and switches to the linked branch so issue and branch numbers match. Use when the developer asks to create, file or open an issue, or says "gh issue".
model: claude-sonnet-5-5
---

# GH Issue

> **Model pin:** Sonnet 5.5 (`claude-sonnet-5-5`): drafting compliant issue text and validating a title format.
> The override applies only for the rest of the current turn and is skipped when an `availableModels`
> allowlist does not allow the model.

Creates the issue, links it to the Project with status Backlog, and (second approval) creates the branch
`{category}/{number}-{slug}` from the number GitHub just assigned, so `CLAUDE.md` R2 holds from the start.
Project identifiers (`{{PROJECT_NUMBER}}`, field and option ids) live in `CLAUDE.md` § GitHub. If any still
reads `{{...}}`, stop and tell the developer to fill it in.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your
context, read that file first. Run each command as its own Bash call. Pass multi-line text with
`--body-file`, never inline.

0. **Announce the model pin** in one short line: "This skill is pinned to Sonnet 5.5."

1. **Gather intent.** Ask only for what is missing: category, scope, purpose, task list.

2. **Validate the category:** `feature`, `bugfix`, `hotfix`, `docs` or `chore`. If the wording does not map
   cleanly, ask the developer to pick one.

3. **Validate the scope** against `CLAUDE.md` § Git conventions. If it is not listed, do not edit
   `CLAUDE.md`. Ask: use the closest existing scope, omit the scope, or add "Add `{scope}` scope to
   CLAUDE.md" as a task in this issue's `## Tasks`.

4. **Compose the title:** `{category}[{scope}]: {title}`, present tense ("Add", "Update", "Remove"), omit
   `[scope]` if none. No hard length cap.

5. **Compose the body:**
   - `# {title description}` (no category prefix)
   - `## Purpose`: why the issue exists
   - `## Tasks`: `- [ ] {action item}` lines, with optional indented sub-bullets
   - `## References` (optional): related issues, docs, PRs; omit if none

6. **Resolve the label:** `feature` = `enhancement`, `bugfix` = `bug`, `hotfix` = `hotfix`,
   `docs` = `documentation`, `chore` = `chore`. Run `gh label list --repo mrlhfz/badge-by-badge`; if the label
   is missing, the draft must say it will be created.

7. **Preview the branch name:** `{category}/{N}-{slug}`. `N` is unknown until the issue exists, so show it as
   `{N}`. The slug is the title description in kebab-case: lowercase `a-z0-9` and hyphens, at most 40
   characters, no trailing hyphen.

8. **Approval gate 1 (GitHub write).** Show the title, body, label (and whether it is new), Project
   `{{PROJECT_NUMBER}}` with status Backlog, no assignee, and the branch preview. Ask with `AskUserQuestion`:
   **"Create the issue"**, **"Edit the draft"**, **"Cancel"**. Touch GitHub only after the first.

9. **On approval, create it.** Write the body to `temp/gh-issue-body.md` with the Write tool. Then, each as
   its own call:
   - Only if the label is missing: `gh label create {label} --repo mrlhfz/badge-by-badge`
   - `gh issue create --repo mrlhfz/badge-by-badge --title "{title}" --body-file temp/gh-issue-body.md --label {label}`
     and read the issue number `N` from the URL it prints.
   - `gh project item-add {{PROJECT_NUMBER}} --owner mrlhfz --url {issue-url} --format json` and read `id`.
   - `gh project item-edit --id {item-id} --project-id {{PROJECT_ID}} --field-id {{STATUS_FIELD_ID}} --single-select-option-id {{STATUS_BACKLOG_OPTION_ID}}`
   Never set an assignee. After the issue is created, delete `temp/gh-issue-body.md`.

10. **Approval gate 2: the linked branch.** Skip this step and say why if the working tree is not clean.
    Otherwise, as separate calls:
    - `git status --porcelain`. Any output means uncommitted work: skip and tell the developer.
    - `git fetch`
    - `git log origin/main..main --oneline`. If it prints anything, warn the developer: the new branch is
      cut from `origin/main`, so those local `main` commits will NOT be on it (push `main` first, or accept).

    Then ask with `AskUserQuestion`: **"Create and switch to `{category}/{N}-{slug}`"** or **"Skip the
    branch"**. On the first, run
    `gh issue develop {N} --repo mrlhfz/badge-by-badge --base main --name {category}/{N}-{slug} --checkout`,
    then `git branch --show-current` to confirm. This never touches `main` and never runs `git add`,
    `commit` or `push`. Finally write the issue URL as the only line of `branch-tasks.txt` (gitignored).

11. **Report back:** the issue URL and number, the title, the label, the Project link and Backlog status, and
    the branch result (created and checked out, or skipped and why).
