# Permission matrix

Who may do what. Rows come from the MUST and SHOULD stories in [mvp-spec.md](mvp-spec.md). CUT stories are left out.

## Legend

Fill each cell with one value:

- `yes`: allowed for any record
- `own`: allowed only for records the user owns
- `troop`: allowed only for records in the user's own troop
- `no`: not allowed

## Matrix

| Action | Admin | Leader | Scout | Not logged in |
| --- | --- | --- | --- | --- |
| **Accounts and setup** | | | | |
| Enter a Leader PIN to claim a Leader account | no | no | no | yes |
| Create Leader PINs | yes | no | no | no |
| Create troops and assign Leaders to them | yes | no | no | no |
| Set how many Leaders each troop has | yes | no | no | no |
| **Badges and requirements** | | | | |
| Create, edit and delete badges for each level | yes | no | no | no |
| Manage a badge's requirement checklist | yes | no | no | no |
| Set how many skill badges each level and stream requires | yes | no | no | no |
| View a badge's requirement checklist | yes | yes | yes | no |
| View badges for current level with status | no | no | own | no |
| **Verification** | | | | |
| View unverified Scouts with their troop and Leaders | yes | no | no | no |
| Mark a Scout as verified (and undo it) | yes | no | no | no |
| Read who verified a Scout and when | yes | no | no | no |
| **Scouts and troop** | | | | |
| Enter a Scout PIN and create a Scout account | no | no | no | yes |
| Add a Scout to a troop and set their stream and starting level | no | troop | no | no |
| Generate a PIN for a new Scout | no | troop | no | no |
| Enter or correct a Scout's full name | no | troop | no | no |
| View the list of Scouts in a troop | no | troop | no | no |
| View a Scout's stream and current level | yes | troop | own | no |
| Deactivate a Scout | no | troop | no | no |
| Update own full name | own | own | no | no |
| Update own username and password | own | own | own | no |
| **Entries (requirements done)** | | | | |
| Mark a requirement done with a date and note | no | no | own | no |
| View a Scout's dated entries | no | troop | own | no |
| Confirm a Scout's entry | no | troop | no | no |
| Comment on a Scout's entry (SHOULD) | no | troop | no | no |
| Edit an entry | no | no | own | no |
| Delete an entry | no | no | own | no |
| Print chronological entries for current level (SHOULD) | no | no | own | no |
| Filter printable entries by badge (SHOULD) | no | no | own | no |
| **Progress and levels** | | | | |
| Log in and see own progress | no | no | own | no |
| View progress bar toward top award for a Scout | no | troop | own | no |
| View count of completed badges toward top award | no | no | own | no |
| View level journey (past and current levels) | no | no | own | no |
| See explanation on badges when not yet verified | no | no | own | no |
| Promote a Scout to the next level | no | troop | no | no |

## Decisions

- **Unverified Scouts can add entries.** They can't fully unlock a badge until verified. An unverified badge shows a duller look (see the Scout story about the explanation).
- **Deactivated Scouts can't log in.** They keep their troop so their history stays linked, but they no longer appear as active.
- **Admins cannot see Scout entries.** They see verification data only.
- **Troops have no fixed size.** Admin sets the number of Leaders for each troop, and a troop can hold Scouts at any mix of levels.
- **Scout full names come from the Leader.** Leaders enter and correct them for Scouts in their troop. Scouts cannot change their own full name.
- **Passwords are managed by Supabase Auth.** The app never stores them.
- **A Scout's stream is set by the Leader when the Scout is added.** The starting level must be open to that
  stream. Streams and their levels are fixed in the MVP.
- **Requirement checklists combine general and stream-specific requirements.** The Admin sets both. The Scout sees
  the combined checklist for their stream.

## Open questions

None left.
