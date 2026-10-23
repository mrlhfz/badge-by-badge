# Wireframes

Screen wireframes for the Badge-by-Badge MVP. They show the layout, the states and the actions on each screen.
They are not final visuals: colours, fonts, icons and the badge images are placeholders.

The wireframes follow the rules in [mvp-spec.md](../mvp-spec.md) and [permission-matrix.md](../permission-matrix.md).
If a wireframe and those documents disagree, the documents win until they are changed on purpose.

The frontend issues use these wireframes to check their layouts:
[#11](https://github.com/mrlhfz/badge-by-badge/issues/11) (login, PIN claim and protected routes),
[#17](https://github.com/mrlhfz/badge-by-badge/issues/17) (Admin and Leader screens) and
[#18](https://github.com/mrlhfz/badge-by-badge/issues/18) (Scout progress dashboard).

## Screens

Fifteen screens, grouped by role. The file names start with `bbb-`. The "Feeds" column names the frontend issue
that builds the screen.

### Account setup and login

| File | Screen | What it shows | Feeds |
| --- | --- | --- | --- |
| [bbb-auth-login.png](bbb-auth-login.png) | Log in | Email and password, "Forgot password?", and a "Claim your account" button for people who have a PIN. | #11 |
| [bbb-auth-claim-pin.png](bbb-auth-claim-pin.png) | Claim your account | Two steps. Step 1 takes the 6-digit PIN. Step 2 (email and password) appears only after the PIN is accepted. | #11 |

### Scout

| File | Screen | What it shows | Feeds |
| --- | --- | --- | --- |
| [bbb-scout-my-badges.png](bbb-scout-my-badges.png) | My badges (home) | Top-award progress bar, a "not verified yet" notice, and the badge cards for the current level with their status. Bottom tabs: Badges, Logbook, Profile. | #18 |
| [bbb-scout-badge-detail.png](bbb-scout-badge-detail.png) | Badge detail | The requirement checklist with each requirement's status, and the Scout's log entries with Edit and Delete. | #18 |
| [bbb-scout-level-journey.png](bbb-scout-level-journey.png) | My journey | Past, current and next levels as a timeline. The current level shows progress toward its badges. | #18 |
| [bbb-scout-logbook.png](bbb-scout-logbook.png) | My logbook | All the Scout's entries, newest first, with search, filter chips and "Copy all as text". | #18 |
| [bbb-scout-profile.png](bbb-scout-profile.png) | Profile | Level, troop, Leader and email, a username form, and links to the level journey, change password and log out. | #18 |

### Leader

| File | Screen | What it shows | Feeds |
| --- | --- | --- | --- |
| [bbb-leader-my-troop.png](bbb-leader-my-troop.png) | My troop | Summary counts (Scouts, logs to confirm, waiting for Admin), a search and filter bar, and the Scout table with actions. | #17 |
| [bbb-leader-scout-progress.png](bbb-leader-scout-progress.png) | Scout progress | One Scout's badges for their level, the entries to confirm, and the Confirm / Send back with a note / Reopen actions. | #17 |
| [bbb-leader-add-scout.png](bbb-leader-add-scout.png) | Add Scout (dialog) | A form for the Scout's name, level and school year. After saving, the new PIN is shown with a Copy button. | #17 |
| [bbb-leader-promote-scout.png](bbb-leader-promote-scout.png) | Promote Scout (dialog) | From and To levels, a checkbox confirming the top award was earned, and a note on what changes. The Promote button stays disabled until the box is ticked. | #17 |

### Admin

| File | Screen | What it shows | Feeds |
| --- | --- | --- | --- |
| [bbb-admin-verify-scouts.png](bbb-admin-verify-scouts.png) | Scout verification | Tabs for Waiting, Verified and Rejected, with Verify and Reject for each Scout. | #17 |
| [bbb-admin-leaders.png](bbb-admin-leaders.png) | Leaders | The Leader list with troop, Scout count and account status, plus an "Add Leader" panel that makes a PIN. | #17 |
| [bbb-admin-badge-catalog.png](bbb-admin-badge-catalog.png) | Badge catalog | Badges filtered by level, with requirement count and the top award each one counts toward. | #17 |
| [bbb-admin-badge-form.png](bbb-admin-badge-form.png) | Add / edit badge | Name, level, description and image on the left. The requirement list (add, reorder, remove) on the right. The same form is used for Edit. | #17 |

## Conventions

- **Sample data:** names such as "Aiman bin [Surname]", "[Troop name]" and "Cikgu [Leader name]" are placeholders.
  Real names are not used in wireframes.
- **Grey boxes:** images, avatars and logos are empty placeholders.
- **Unverified state:** an amber "Waiting for verification" tag and a notice. Badges look shaded until the Admin
  verifies the Scout.
- **Status colours:** amber means waiting, green means confirmed or verified, grey means not started, and red
  means a destructive action (Delete, Remove).
- **Mobile first for Scouts:** the Scout screens are phone-sized. The Leader and Admin screens are desktop-sized.

## Checks against the spec

These are points where a wireframe does not yet match the spec or the permission matrix. Fix the wireframe or the
spec on purpose, one at a time.

- **Stream is missing from the Scout screens.** The spec says a Scout sees their stream and current level. The
  header in `bbb-scout-my-badges.png` shows only the level, and the profile in `bbb-scout-profile.png` has no stream.
- **Stream is missing from Add Scout.** The spec says the Leader chooses the stream and starting level. The form in
  `bbb-leader-add-scout.png` has a level and a school year, but no stream.
- **Next level not checked against the stream.** The spec says the Leader sees the next level open to the Scout's
  stream before promoting. `bbb-leader-promote-scout.png` shows the next level but not whether it is open.
- **"Remove" instead of "Deactivate".** The Leader screens use "Remove" for a Scout. The spec and the permission
  matrix say "Deactivate", and a deactivated Scout keeps their history.
- **70% alert on the progress bar.** `bbb-scout-my-badges.png` shows an "Alert at 80%" marker. The spec's 70%
  notification is CUT, so the marker should be removed or the spec changed.
- **Printable logbook.** The spec asks for a printable list, with a filter by badge. `bbb-scout-logbook.png` has
  "Copy all as text" and a search, but no print action and no per-badge filter.
- **Skill badge count is not in the badge form.** The spec says the Admin sets how many skill badges each level and
  stream requires. `bbb-admin-badge-form.png` has no field for this.
- **Stream-specific requirements are not in the badge form.** The spec says the Admin manages general and
  stream-specific requirements. The requirement list has one column and no stream choice.
- **Leader name on Admin verification.** The verification table shows the Leader for each Scout, which matches the
  spec. It does not show the Scout's stream. Add it if the Admin needs it to check the official list.

## Files

- `bbb-*.png`: the wireframe images, one per screen.
- `README.md`: this file.
