# Claude Rules for Badge-by-Badge

Digital Scout badge tracker for Malaysian troops: Admin verifies, Leaders award badges, Scouts track
progress. Solo MVP (JomCode Bootcamp final project), to be grown after the MVP presentation.

## Stack and layout

| Part | Stack |
| --- | --- |
| `backend/` | Python, FastAPI, Pydantic, SQLAlchemy + Alembic, PostgreSQL on Supabase (Auth + Row Level Security). Tests: pytest. Lint/format: Ruff. |
| `frontend/` | React, Vite, TypeScript (strict), npm. Lint: ESLint. Format: Prettier. Tests: Vitest. |

- One repo, one `.claude/`, one `CLAUDE.md` (this file). `backend/` and `frontend/` sit side by side.
- Start Claude sessions at the repo root: the hooks resolve their paths from it.
- Ruff, Prettier and Vitest are decided but installed by the developer by hand. Check
  `frontend/package.json` and `backend/requirements-dev.txt` before running them; if one is missing, say
  so instead of installing it.

## Commands

Run from the repo root unless noted.

| Task | Command |
| --- | --- |
| Frontend dev server | `npm run dev --prefix frontend` |
| Frontend lint | `npm run lint --prefix frontend` |
| Frontend type-check + build | `npm run build --prefix frontend` (runs `tsc -b`) |
| Frontend format / tests | `npm run format --prefix frontend` / `npm run test --prefix frontend` |
| Backend dev server | `uvicorn main:app --reload` (from `backend/`, venv active) |
| Backend tests | `python -m pytest` (from `backend/`, venv active) |
| Backend lint / format | `ruff check .` / `ruff format .` (from `backend/`) |

If you `cd` into `backend/`, `cd` back to the repo root afterwards. Never `pip install` globally; if the
venv is not active, ask the developer.

## Git conventions

- **Branch:** `{category}/{issue-number}-{slug}`, for example `chore/1-claude-setup`.
- **Issue title:** `{category}[{scope}]: {title}`. Categories: `feature`, `bugfix`, `hotfix`, `docs`, `chore`.
- **Commit:** `{type}[{scope}]: {description} (#{issue})` for a single line. With a body, drop the `(#...)` from
  the subject and end with `Refs: #{issue}`. Present tense, subject under 72 characters, breaking change =
  `!` after the type plus a `BREAKING CHANGE:` footer.
- **Types:** `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. Category to type: feature = feat,
  bugfix/hotfix = fix, docs = docs, chore = chore.
- **Scopes:** `backend`, `frontend`, `db`, `auth`, `docs`, `tooling`. Omit `[scope]` if none fits. To add a
  scope, change this list in its own commit.
- **PRs:** squash-merge, so the PR title becomes the commit on `main` (GitHub appends the PR number).
  The `pr-message` skill drafts the title and body. After approval, `pr-create` opens the PR as a draft and
  adds it to the Project. The developer marks it ready and reviews it. `pr-commit-message` drafts the
  squash-merge commit message.

## GitHub

- Repo `mrlhfz/badge-by-badge`. Issues and a GitHub Project are used. Project owner: `mrlhfz`.
- Project number: `4`
- Project id: `PVT_kwHOCOvsj84BnHK3`
- Status field id: `PVTSSF_lAHOCOvsj84BnHK3zhltR2w`
- Status option ids: Backlog `f75ad846`, In review `df73e18b`
- Find them with `gh project list --owner mrlhfz`, then `gh project field-list <number> --owner mrlhfz --format json`
  (fields and options) and `gh project view <number> --owner mrlhfz --format json` (project id).

## Temporary files

Scratch output goes in `temp/` (gitignored). Do not `mkdir temp` as a precaution; create it only if a write
fails because it is missing. Delete a temp file as soon as the command that needed it has finished. Drafts
the skills write for later reference (`temp/pr-message-{n}.md`, `temp/code-review-{n}.md`,
`temp/pr-commit-message-{n}.md`) stay until the developer removes them. `{n}` is the issue number from the
branch name.

## Command Execution

How Claude runs shell commands lives in [`CLAUDE.command-rules.md`](CLAUDE.command-rules.md). It is injected
at session start by a `SessionStart` hook, and a `PreToolUse` hook on `Bash` blocks the three rules that can
be decided from the command text.

## Project rules

### R1: Main protection and staging

- **What:** `main` stays clean; the developer owns every git write.
- **MUST:** run `git branch --show-current` before changing any file. On `main`, stop and tell the developer.
  Ask before staging anything.
- **MUST NOT:** edit tracked files on `main`; run `git add`, `git commit`, `git push` or `git reset --hard`.
- **Exemptions:** gitignored scratch files (`temp/`, `branch-tasks.txt`) and `.git/COMMIT_EDITMSG` written by
  the `commit-message` skill after approval. The `gh-issue` skill may switch branches in its approved
  branch step.
- **Exception:** the developer explicitly approves one named action in the session.
- **Enforced by:** the first step of every skill; the allowlist deliberately omits git writes so each one
  prompts; `code-review` dimension 11.

### R2: Branch and issue sync

- **What:** one branch is one GitHub issue, and both carry the same number.
- **MUST:** name branches `{category}/{issue-number}-{slug}` using the number GitHub assigned; end commits with
  `Refs: #{that number}`; make the PR close that issue.
- **MUST NOT:** guess or invent an issue number; reference a different issue from this branch without
  approval; add work beyond the branch's issue (scope creep) without the developer choosing how: update
  that issue, make a sub-issue, or run a new `gh-issue`.
- **Exemptions:** `main`, and the bootstrap commits made before this workflow existed.
- **Exception:** the developer renames the branch (`git branch -m`) or moves the work to its own branch;
  otherwise they confirm the mismatch for that single action.
- **Enforced by:** `gh-issue` (creates issue and branch from one number; step 1a asks on added work); `commit-message` (warns);
  `pr-message` (hard stop); `pr-create` and `pr-commit-message` (hard stop); `code-review` dimension 11.

### R3: Secrets and env vars

- **What:** `.env` files hold secrets and stay on one machine; `.env.example` documents names only.
- **MUST:** list every env var the code reads in the matching `.env.example` (names, no real values) in the same
  PR; keep `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL` and any other secret in `backend/` only; in `frontend/`
  use only public `VITE_` values (Supabase URL and anon key, API URL).
- **MUST NOT:** commit a `.env`; read or print `.env` contents; put a secret in `frontend/` or in a `VITE_`
  variable; hard-code a key.
- **Exemptions:** `.env.example` files; the public Supabase anon key in the frontend.
- **Exception:** a new public `VITE_` variable needs a one-line PR note on why it is safe to expose. There is no
  exception for secrets.
- **Enforced by:** `.gitignore`; `permissions.deny` on reading `.env`; the guard hook blocks `cat .env`;
  `code-review` dimensions 7 and 9.

### R4: Row Level Security on every table

- **What:** every table has RLS enabled, so the public key cannot read or write rows it should not.
- **MUST:** enable RLS and define policies for the allowed roles in the same migration that creates the
  table (migrations live in `backend/migrations`).
- **MUST NOT:** ship a table without RLS; disable RLS to make a bug go away.
- **Exemptions:** Alembic's own `alembic_version` table.
- **Exception:** a deliberately public table is allowed if a comment in its migration and the PR description
  both say why.
- **Enforced by:** `code-review` dimensions 7 and 9, which check every new table in the diff.

### R5: Roles and statuses in one place

- **What:** roles (Admin, Leader, Scout) and badge statuses are defined once, not retyped.
- **MUST:** define each as an enum in the backend at `backend/app/enums.py` and mirror it once in the
  frontend at `frontend/src/enums.ts`; import from those files everywhere else.
- **MUST NOT:** write role or status string literals (`"verified"`, `"Leader"`) in routes, queries or
  components.
- **Exemptions:** tests asserting exact values; past Alembic migrations (frozen in time).
- **Exception:** add a new role or status by editing the definition, its mirror and a migration in one PR.
- **Enforced by:** `code-review` dimension 9.

### R6: Teaching mode

- **What:** the developer is learning full-stack and writes the code; Claude is the coach.
- **MUST:** explain with plain analogies, point to the file and the reason, give hints and small snippets, ask
  before writing feature code, and name best practices as they come up.
- **MUST NOT:** generate whole features, endpoints or components unprompted; silently fix a bug without saying
  what was wrong.
- **Exemptions:** tooling and config (`.claude/`, `CLAUDE*.md`, `.gitignore`, `docs/`), and anything asked for
  explicitly.
- **Exception:** "write this for me" lifts the rule for that one request only.
- **Enforced by:** this instruction only; no hook checks it.

## Skills

| Skill | Use it to |
| --- | --- |
| `commit-message` | Draft a commit message for staged changes into `.git/COMMIT_EDITMSG`. |
| `gh-issue` | Create an issue, add it to the Project as Backlog, and create the matching branch. |
| `update-branch-tasks` | Rebuild `branch-tasks.txt` from the branch number and its commits. |
| `pr-message` | Draft the PR title and body, then move the issue to In review. |
| `pr-commit-message` | Draft the squash-merge commit message for the whole branch (not staged changes). |
| `pr-create` | Run the pre-PR gates and review, then open the PR as a draft after confirmation. |
| `code-review` | Review the whole branch against `main` across 11 dimensions. |
