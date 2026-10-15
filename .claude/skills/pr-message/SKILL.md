---
name: pr-message
description: Drafts a pull request title and body for the whole current branch (git diff main...HEAD), saves it to temp/pr-message-{n}.md, and after approval moves the closed issue to In review in the Project. Never creates the PR. Use when the developer asks to draft the PR message or body for the current branch.
model: claude-sonnet-5-5
---

# PR Message

> **Model pin:** Sonnet 5.5 (`claude-sonnet-5-5`): template-driven summarizing of a branch diff. The override
> applies only for the rest of the current turn and is skipped when an `availableModels` allowlist does not
> allow the model.

Drafts the PR text only. Run on its own, the developer creates the PR themselves. When run as a step of
`pr-create`, that skill opens the PR after its own gates. The repo squash-merges, so the PR title becomes the
commit on `main`; GitHub appends the PR number, so the title carries none. Project identifiers live in
`CLAUDE.md` § GitHub.

> **Sync rule:** This skill's steps, approval gate (step 8) and `In review` side effect (step 9) are composed
> by `.claude/skills/pr-create/SKILL.md` step 4. If any of those change shape, review `pr-create` for consistency,
> and vice versa.
>
> **Sync rule:** The Project ids in step 9 must match `CLAUDE.md` § GitHub. If either changes, update both.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your
context, read that file first. Run each command as its own Bash call.

0. **Announce the model pin** in one short line: "This skill is pinned to Sonnet 5.5." When it runs as a step of
   another skill (`pr-create`), announce the pin in one line only.

1. **Gate: branch.** Run `git branch --show-current`. If it is `main`, stop. Read the issue number `N` from the
   branch name `{category}/{N}-{slug}`; if it does not match, stop and report an R2 breach.

2. **Gate: clean tree.** Run `git diff`, then `git diff --cached`. If either prints anything, stop and ask the
   developer to commit or stash first.

3. **Gate: branch-tasks.txt is current and in sync.** Read `branch-tasks.txt` with the Read tool.
   - If it is missing, or does not list issue `N`, stop and tell the developer to run `update-branch-tasks`.
   - If it lists any issue other than `N`, stop and report the mismatch (R2). Do not draft `Closes:` lines
     against the wrong issue. The developer either moves that work to its own branch or confirms the
     mismatch for this PR.

4. **Gather the scope.** Run `git diff main...HEAD` and `git log main..HEAD --oneline`. The draft must
   describe every change in that diff.

5. **Map changes to the issue.** Everything belongs to issue `N`. Changes that belong to no issue go in a
   clearly labeled "Unrelated / No Issue" section; never silently drop them.

6. **Compose the draft.**
   - Title: `{type}[{scope}]: {title description}`, present tense, under 72 characters (count it yourself),
     no `(#...)` suffix.
   - Body: `# {title description}`, `## Summary` (what changed and why), optional `## Breaking Changes` (omit
     if none), and `## Related Issues` with `Closes: #N`.

7. **Write the draft** to `temp/pr-message-{N}.md`. Do not create the PR.

8. **Approval gate (GitHub write).** Show the draft. Say clearly that approving it also moves issue `#N` to
   **In review** in the Project. Ask with `AskUserQuestion`: **"Approve and move to In review"**,
   **"Request changes"**. On changes, revise, rewrite the file, and ask again. Never infer approval.

9. **On approval, transition the issue.** As separate calls:
   - `gh project item-list 4 --owner mrlhfz --format json -L 500 -q ".items[] | select(.content.number == {N}) | {id: .id, status: .status}"`
   - If nothing is printed, the issue is not on the Project: skip and say so. If `status` is not one of
     Backlog, Ready, In progress or In review (for example Done), skip and say why. If it is already
     In review, record it as a no-op.
   - Otherwise: `gh project item-edit --id {item-id} --project-id PVT_kwHOCOvsj84BnHK3 --field-id PVTSSF_lAHOCOvsj84BnHK3zhltR2w --single-select-option-id df73e18b`

10. **Report back:** the file path, the issue grouping used, and the status result (moved, already In review,
    or skipped with the reason). Then, when run standalone, print the command for the developer to run
    themselves, with the real title filled in:
    `gh pr create --repo mrlhfz/badge-by-badge --base main --draft --title "{title}" --body-file temp/pr-message-{N}.md`
    When run as a step of `pr-create`, skip this printout, because `pr-create` creates the PR itself.
    Mention that the draft file stays until they delete it.
