# MVP spec

## Levels

The five sections of Persekutuan Pengakap Malaysia (PPM). Each one is a level in the app, in this order. Each
level has its own highest award, and a Scout's progress is shown toward the award for their current level.

| Section (Malay) | English term | Age group | Target audience | Highest award |
| --- | --- | --- | --- | --- |
| Pengakap Lebah | Joey / Beaver Scouts | 5–8 years | Pre-school and lower primary | Lencana Lebah |
| Pengakap Kanak-Kanak (PKK) | Cub Scouts | 9–12 years | Primary school (Tahun 3–6) | Anugerah Rambu Pengakap Kanak-Kanak |
| Pengakap Muda (PM) | Junior / Troop Scouts | 13–15 years | Lower secondary (Tingkatan 1–3) | Anugerah Rambu Pengakap Muda |
| Pengakap Remaja (PR) | Senior Scouts | 16–17 years | Upper secondary (Tingkatan 4–5) | Anugerah Pengakap Raja (King's Scout) |
| Pengakap Kelana (PK) | Rover Scouts | 18–26+ years | Post-secondary, tertiary and young adults | Anugerah BP Award (Baden-Powell Award) |

## Streams

Each Scout belongs to one stream. Streams add tailored training on top of the level journey. A stream can only
start or continue at a level where it is open.

| Stream | Focus |
| --- | --- |
| Pengakap | Bushcraft, pioneering, camping and survival (Land) |
| Pengakap Laut | Seamanship, navigation, canoeing, sailing and water rescue (Sea) |
| Pengakap Udara | Aviation, fundamentals of flight, rocketry and air navigation (Air) |
| Pengakap Khas | Adapted training for Scouts with physical, intellectual or sensory disabilities (Special Needs) |

| Level | Pengakap | Pengakap Laut | Pengakap Udara | Pengakap Khas |
| --- | --- | --- | --- | --- |
| Pengakap Lebah | Yes | No | No | Yes |
| Pengakap Kanak-Kanak | Yes | Yes | No | Yes |
| Pengakap Muda | Yes | Yes | Yes | Yes |
| Pengakap Remaja | Yes | Yes | Yes | Yes |
| Pengakap Kelana | Yes | Yes | Yes | Yes |

Streams and their levels are fixed in the MVP. The Admin does not edit them. Pengakap Laut is the only stream in
the MVP; the others are WIP.

Each badge has general requirements, which apply to every stream, and stream-specific requirements. A Scout's
checklist is the general requirements plus the ones for their stream.

**MVP scope for the deployment and presentation:** the Pengakap Laut path from Pengakap Muda, through Pengakap
Remaja, to Anugerah Pengakap Raja. Other levels and streams are work in progress (WIP).

## Top award prerequisites

### Anugerah Pengakap Raja

- A Scout may start at any level open to their stream.
- Their Pengakap Muda and Pengakap Remaja must be in the same stream, and Remaja must follow Muda.
- To be eligible, their level history must include Pengakap Muda, and Pengakap Remaja must come after it (Muda's start date is earlier than Remaja's).
- Holding the level is enough; the Muda and Remaja badges do not have to be complete.
- A Scout who starts at Remaja is allowed in the app but is not eligible for Raja.

## User stories

Tier: **MUST** = needed for the demo, **SHOULD** = good to have, **CUT** = drop first if time runs short.

### Admin

- As an admin, I want to create Leader PINs, so that a new Leader can claim their account. **MUST**
- As an admin, I want to create troops and assign Leaders to them, so that every Leader has a troop to run. **MUST**
- As an admin, I want to set how many Leaders each troop has, so that troops of different sizes are each staffed properly. **MUST**
- As an admin, I want to create, edit and delete badges for each level, so that Scouts work from an up-to-date catalog. **MUST**
- As an admin, I want to manage each badge's general and stream-specific requirements, so that Scouts know exactly what to do. **MUST**
- As an admin, I want to see a list of unverified Scouts with their troop, stream, current level and Leaders, so that I can check them against the official Persekutuan Pengakap Malaysia list. **MUST**
- As an admin, I want to mark a Scout as verified (and undo it), so that only officially registered Scouts count as verified. **MUST**
- As an admin, I want the system to record who verified a Scout and when, so that verification can be audited. **MUST**
- As an admin, I want to change my full name, username and password, so that my account details stay correct. **MUST**

### Leader

- As a leader, I want to add Scouts to my troop, enter each Scout's full name, choose their stream and choose their starting level, so that they begin at the right place. **MUST**
- As a leader, I want to generate a PIN for a new Scout and show it to them, so that they can create their own account. **MUST**
- As a leader, I want to see only the Scouts in my own troop, with each Scout's stream and current level, so that I manage my troop and nobody else's. **MUST**
- As a leader, I want to correct a Scout's full name in my troop, so that records match the official list. **MUST**
- As a leader, I want to change my full name, username and password, so that my account details stay correct. **MUST**
- As a leader, I want to deactivate a Scout in my troop, so that people who have left no longer appear as active. **MUST**
- As a leader, I want to review each Scout's dated entries and confirm them, so that the badges reflect what really happened. **MUST**
- As a leader, I want to comment on an entry, so that I can ask the Scout for more detail without rejecting it. **SHOULD**
- As a leader, I want to see a progress bar for each Scout toward their level's top award, so that I know who needs help. **MUST**
- As a leader, I want to promote a Scout to the next level once they have passed the top award in person, so that their history moves on. I want to see the next level open to the Scout's stream before I promote them. **MUST**
- As a leader, I want to be notified when a Scout in my troop reaches 70% progress, so that I can plan their next step. **CUT**

### Scout

- As a scout, I want to enter the PIN from my Leader and create an account, so that I can start tracking my badges. **MUST**
- As a scout, I want to log in and see only my own progress, so that my records stay private. **MUST**
- As a scout, I want to see my stream and current level, and the badges for that level with their status (not started, in progress, complete), so that I know what is left. **MUST**
- As a scout, I want to see the requirement checklist for a badge, including the general and stream-specific steps for my stream, so that I know what each step needs. **MUST**
- As a scout, I want to mark a requirement done with a date and a note, so that I keep a record of what I did. **MUST**
- As a scout, I want to edit or delete my own entries, so that I can fix mistakes. **MUST**
- As a scout, I want to see how many badges I have completed toward the top award, so that I know how close I am. **MUST**
- As a scout, I want to see my level journey (past levels and the current one), so that I can see how far I have come. **MUST**
- As a scout, I want to see a short explanation on my badges when my account is not yet verified, so that I understand why they look different. **MUST**
- As a scout, I want to change my username and password, so that my account stays correct and secure. **MUST**
- As a scout, I want to get a notification when I reach 70% progress, so that I know I am close to the top award. **CUT**
- As a scout, I want a printable, chronological list of my entries for the current level, with my name, stream and current level in the header, so that I can write my logbook for the top award. **SHOULD**
- As a scout, I want to filter my printable entries by badge, so that I can print only what I need. **SHOULD**
