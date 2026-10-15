---
name: pr-create
description: Runs the pre-PR sequence for the current branch end-to-end: validates the branch is clean, pushed, up to date with main and has no open PR, regenerates branch-tasks.txt via update-branch-tasks, runs code-review and enforces its Critical/Warning resolution bar, drafts the PR text via pr-message, then after a separate confirmation opens the PR as a draft and adds it to the Project. Use when the developer asks to create the PR, open a PR for this branch, or says "pr-create".
model: claude-sonnet-5-5
---

# PR Create

> **Model pin:** Sonnet 5.5 (`claude-sonnet-5-5`): this skill orchestrates gates and `gh` calls, and review depth
> is delegated to `code-review`. The override applies only for the rest of the current turn and is skipped when an
> `availableModels` allowlist does not allow the model.

Chains branch validation, `branch-tasks.txt` regeneration, code review and PR-text drafting into one flow that
ends in opening the PR as a draft, so a branch cannot reach PR creation without passing the same bar every time.
It composes `update-branch-tasks`, `code-review` and `pr-message` as steps rather than repeating their logic.

Project identifiers live in `CLAUDE.md` § GitHub. Repo: `mrlhfz/badge-by-badge`. Project number: `4`, owner `mrlhfz`.

> **Sync rule:** Step 4 depends on `.claude/skills/pr-message/SKILL.md`'s drafting and approval flow, its
> `In review` side effect, and its output path `temp/pr-message-{N}.md`. If any of those change shape, review this
> file, and vice versa.
>
> **Sync rule:** Step 2 depends on `.claude/skills/update-branch-tasks/SKILL.md`'s regeneration flow. If it changes
> shape, review this file, and vice versa.
>
> **Sync rule:** Step 3 depends on `.claude/skills/code-review/SKILL.md`'s output path (`temp/code-review-{N}.md`),
> its verdict and `### Finding {index}` / `**Severity**` / `**Status**` / `L.{index}.{n}` / `F.{index}.{n}` format,
> and its `## Marking a finding resolved` section. If any of those change shape, review this file, and vice versa.

## Flow

**Command rules:** injected at session start from `CLAUDE.command-rules.md`; if they are not in your context,
read that file before running any shell command. Run each command as its own Bash call. Skills composed as
steps inherit this.

> **Stop-notification rule:** whenever a step says "stop," the message must give the concrete reason (which check
> failed and what it found), never a bare "stopped."

0. **Announce the model pin** in one short line: "This skill is pinned to Sonnet 5.5." Composed skills announce
   their own pin in one line.

1. **Validate branch.** All checks are read-only. Stop at the first failing check and give the reason:
   1. **Not on main.** `git branch --show-current`. If it is `main`, stop: there is nothing to PR into `main`.
   2. **Branch shape (R2).** The name must match `{category}/{N}-{slug}`. If not, stop and report the R2 breach.
   3. **No open PR.** `gh pr list --repo mrlhfz/badge-by-badge --head {branch} --state open --json number,url`.
      If one is open, stop and name it.
   4. **Clean working tree.** `git diff` and `git diff --cached` must both print nothing. Run each as its own call.
   5. **Pushed.** `git fetch`, then compare `git log -1 --format=%H` with `git log -1 --format=%H origin/{branch}`.
      If they differ, stop and tell the developer to run `git push` themselves, then re-run this skill. This
      skill never pushes.
   6. **Up to date with main.** `git log HEAD..origin/main --oneline` must print nothing. If it does, stop and tell
      the developer to merge `main` into the branch locally and resolve conflicts, then re-run. This skill never
      merges.
   7. **Has something to PR.** `git log main..HEAD --oneline` must print at least one commit.

2. **Regenerate `branch-tasks.txt`.** Execute the `update-branch-tasks` skill. If the developer does not accept its
   proposed list, stop.

3. **Code review gate.**
   - Execute the `code-review` skill against the current branch. It writes `temp/code-review-{N}.md`. Never invoke
     the cloud `/code-review ultra` variant from here; it is billed and user-triggered only.
   - **Verdict short-circuit:** if the verdict is `## Verdict: ✅ Approve`, the gate passes; go to step 4. For any
     other verdict, decide pass or fail finding by finding.
   - **Resolution bar:** every `### Finding {index}` with `**Severity**: 🔴 Critical` or `🟡 Warning` must be
     resolved by a code, test or doc change. Every `🔵 Suggestion` must be either resolved the same way, or closed
     with a recorded reason and marked `skipped` or `no_change_needed` with an `**Outcome**` note pointing to where
     the decision is written down. No finding may still read `**Status**: ⏳ Open` when step 4 starts. A Suggestion
     is never dropped silently.
   - **Halt** while the developer applies fixes. Ask them to say when they are done and to name the
     `F.{index}.{n}` option applied for each fixed finding.
   - **Targeted re-check, not a new review.** Once the developer confirms, re-open `temp/code-review-{N}.md`. For each
     Critical or Warning finding, examine every `L.{index}.{n}` location (and any test it cites) to confirm the
     problem is gone. If the developer named an `F.{index}.{n}` option, confirm the change matches it. Once a
     finding verifies, mark it using `code-review`'s `## Marking a finding resolved` procedure. A finding already
     marked on demand is still re-checked; its marker stays if it verifies.
   - If any Critical or Warning finding does not verify, stop and name the `Finding {index}` and the
     `L.{index}.{n}` locations that still fail. Do not continue on partial fixes.

4. **PR text.** Execute the `pr-message` skill. It writes `temp/pr-message-{N}.md` and asks for its own approval of
   the title and body. Do not infer approval from silence.
   - **Side effect to call out:** pr-message's approval moves issue `#N` to **In review** in the Project right away,
     even if the PR is never created. Say so explicitly when reporting back.

5. **Create the PR.**
   - Ask **one more confirmation**, separate from step 4's approval, with `AskUserQuestion`: **"Create draft PR"**,
     **"Cancel"**. Approving the text is not approving the publish. Do not proceed without an explicit yes.
   - On yes, as two separate single-line Bash calls:

     ```sh
     gh pr create --repo mrlhfz/badge-by-badge --base main --draft --title "{title}" --body-file temp/pr-message-{N}.md --assignee @me
     ```

     Then, using the URL the first call printed:

     ```sh
     gh project item-add 4 --owner mrlhfz --url {pr-url}
     ```

   - Leave the PR as a draft so the developer marks it ready for review.
   - Out of scope: the squash-merge commit message. Run `pr-commit-message` for that, at merge time or after the
     branch changes. Reviewers and labels stay manual.

6. **Report back:**
   - Which step-1 checks passed, or which one stopped the flow and why.
   - The `branch-tasks.txt` result.
   - The code-review summary: the verdict, then each finding grouped by severity with its final `**Status**` and
     either the applied `F.{index}.{n}` option or the skip or no-change reason.
   - The pr-message approval and the issue→**In review** side effect.
   - Once created: the PR URL, that it is a draft, and that it is linked to the Project.
   - Remind the developer that reviewers and labels are still theirs to set.
