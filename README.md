# Badge-by-Badge

Digital Scout badge tracker for Persekutuan Pengakap Malaysia (PPM) troops. Admins verify Scouts. Leaders award
badges and run their troop. Scouts track their progress toward the top award for their level.

Solo MVP built as the JomCode Bootcamp final project. It will grow after the MVP presentation.

> **MVP scope:** the Pengakap Laut path, from Pengakap Muda through Pengakap Remaja to Anugerah Pengakap Raja.
> Other levels and streams are work in progress (WIP).

## Who uses it

| Role | What they do |
| --- | --- |
| Admin | Creates Leader PINs, troops and badges. Sets how many Leaders each troop has. Verifies Scouts against the official PPM list. Sees verification data only, never Scout entries. |
| Leader | Adds Scouts to their troop, sets their stream and starting level, and generates their PINs. Confirms each Scout's entries and promotes Scouts to the next level. Sees only their own troop. |
| Scout | Claims an account with a PIN from their Leader. Logs each requirement as done, with a date and note. Sees only their own progress. |

## Levels and streams

A Scout moves through five levels, in this order. Each level has its own top award, and a Scout's progress is
shown toward the award for their current level.

| # | Level (Malay) | Level (English) | Top award |
| --- | --- | --- | --- |
| 1 | Pengakap Lebah | Joey / Beaver Scouts | Lencana Lebah |
| 2 | Pengakap Kanak-Kanak | Cub Scouts | Anugerah Rambu Pengakap Kanak-Kanak |
| 3 | Pengakap Muda | Junior / Troop Scouts | Anugerah Rambu Pengakap Muda |
| 4 | Pengakap Remaja | Senior Scouts | Anugerah Pengakap Raja (King's Scout) |
| 5 | Pengakap Kelana | Rover Scouts | Anugerah BP Award (Baden-Powell Award) |

Each Scout belongs to one stream. Streams add training on top of the level journey.

| Stream | Focus |
| --- | --- |
| Pengakap | Bushcraft, pioneering, camping and survival (Land) |
| Pengakap Laut | Seamanship, navigation, canoeing, sailing and water rescue (Sea) **MVP** |
| Pengakap Udara | Aviation, flight, rocketry and air navigation (Air) |
| Pengakap Khas | Adapted training for Scouts with disabilities (Special Needs) |

Streams and their levels are fixed in the MVP. The full level-by-stream matrix is in
[docs/mvp-spec.md](docs/mvp-spec.md#streams).

### Anugerah Pengakap Raja prerequisites

- The Scout's level history must include Pengakap Muda, and Pengakap Remaja must come after it.
- Muda and Remaja must be in the same stream.
- Holding the level is enough. The Muda and Remaja badges do not have to be complete.
- A Scout who starts at Remaja can use the app but is not eligible for Raja.

## How progress is counted

- **Compulsory badges** count toward progress as each one is completed.
- **Skill badges** count up to the number required for the level and stream. Extra skill badges do not raise progress.
- A badge is **complete** when every general and stream-specific requirement has a confirmed entry.
- A badge only counts as unlocked once the Scout is **verified**. Unverified Scouts can still add entries.
- A Scout whose progress reaches 70% (a placeholder) sees an in-app alert when they open the app. A Leader sees
  the same alert for each Scout in their troop who reaches 70%.
  The notification stories are marked CUT, so they are the first features to drop if time runs short.

The formula, with the data behind it, is in [docs/data-model.md](docs/data-model.md#decisions).

## Tech stack

| Part | Stack |
| --- | --- |
| Backend (`backend/`) | Python, FastAPI, Pydantic, SQLAlchemy and Alembic, pytest, Ruff |
| Frontend (`frontend/`) | React, Vite, TypeScript (strict), ESLint, Prettier, Vitest |
| Database and auth | PostgreSQL on Supabase, with Supabase Auth and Row Level Security (RLS) |

## Repository layout

```
badge-by-badge/
├── backend/          FastAPI app, Alembic migrations, pytest tests
├── frontend/         React + Vite + TypeScript app
├── docs/             MVP spec, data model, permission matrix
├── .claude/          Claude Code hooks, skills and settings
├── CLAUDE.md         Project rules for Claude Code
└── README.md
```

## Getting started

You need Python with a virtual environment, Node.js with npm, and a Supabase project.

### Backend

Run these from `backend/`.

1. Create and activate a virtual environment (on Windows: `.venv\Scripts\activate`).
2. Install the dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
3. Copy `.env.example` to `.env` and fill in the values. Never commit `.env`.
4. Start the server: `uvicorn main:app --reload`

Check that it runs:

- `http://localhost:8000/health` returns `{"status": "ok"}`
- `http://localhost:8000/health/db` returns `{"database": "ok"}` once the database is reachable

### Frontend

Run these from the repo root.

1. Install the dependencies: `npm install --prefix frontend`
2. Copy `frontend/.env.example` to `frontend/.env` and fill in the public values.
3. Start the dev server: `npm run dev --prefix frontend`, then open `http://localhost:5173`

### Environment variables

Names only. The real values stay in your local `.env` files.

| Variable | Where | Notes |
| --- | --- | --- |
| `SUPABASE_URL` | `backend/.env` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | `backend/.env` | Secret. Backend only |
| `DATABASE_URL` | `backend/.env` | Secret. Backend only |
| `FRONTEND_ORIGIN` | `backend/.env` | Allowed CORS origin, e.g. `http://localhost:5173` |
| `VITE_SUPABASE_URL` | `frontend/.env` | Public Supabase URL |
| `VITE_SUPABASE_ANON_KEY` | `frontend/.env` | Public anon key, safe to expose |
| `VITE_API_URL` | `frontend/.env` | Backend URL, e.g. `http://localhost:8000` |

## Commands

Run from the repo root unless noted.

| Task | Command |
| --- | --- |
| Frontend dev server | `npm run dev --prefix frontend` |
| Frontend lint | `npm run lint --prefix frontend` |
| Frontend type-check and build | `npm run build --prefix frontend` |
| Frontend format | `npm run format --prefix frontend` |
| Frontend tests | `npm run test --prefix frontend` |
| Backend dev server | `uvicorn main:app --reload` (from `backend/`, venv active) |
| Backend tests | `python -m pytest` (from `backend/`, venv active) |
| Backend lint and format | `ruff check .` and `ruff format .` (from `backend/`) |

## Documentation

- [docs/mvp-spec.md](docs/mvp-spec.md): levels, streams, user stories and their priority (MUST, SHOULD, CUT)
- [docs/permission-matrix.md](docs/permission-matrix.md): who can do what, for each role
- [docs/data-model.md](docs/data-model.md): tables, enums, relationships and design decisions

## Development workflow

- **Branches:** `{category}/{issue-number}-{slug}`, for example `docs/6-write-mvp-spec-and-data-model`.
  Categories: `feature`, `bugfix`, `hotfix`, `docs`, `chore`.
- **Commits:** `{type}[{scope}]: {description} (#{issue})`, in the present tense. Scopes: `backend`, `frontend`,
  `db`, `auth`, `docs`, `tooling`.
- **Pull requests:** squash-merged into `main`, so the PR title becomes the commit on `main`. Each PR closes its issue.
- **Tracking:** GitHub Issues and a GitHub Project board (`mrlhfz/badge-by-badge`).

The full rules are in [CLAUDE.md](CLAUDE.md).

## Security and data

- Every table has RLS enabled in the same migration that creates it. The public key cannot read rows a user
  should not see.
- The service role key and database URL stay in `backend/`. The frontend only uses public `VITE_` values.
- PINs are stored as hashes and shown once. Passwords live in Supabase Auth, never in these tables.
- The app stores only each Scout's full name and PPM membership number. It does not store birth dates, IC
  numbers or contact details, because Scouts are minors.

## Not in the MVP

- Everything outside the Pengakap Laut path from Pengakap Muda to Anugerah Pengakap Raja. Other levels and streams
  are listed in the app in light grey and cannot be clicked (WIP)
- Changing a Scout's stream after it is set
- Email notifications (deferred)
- Entry comments, printable logbook and filtering by badge are SHOULD stories and come after the MUST stories
