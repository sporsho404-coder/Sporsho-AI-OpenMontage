# CLIENTS — Client Profiles & Rules

**One folder per client. This is a genuine gap upstream — OpenMontage has no concept
of a client.**

Verified by searching the source at `08e2151`: zero references to client profiles,
client-specific rules, or per-client configuration. Every pipeline is client-agnostic.

This folder is where your client knowledge lives.

---

## Create A Client

```bash
cp -r SPORSHO/CLIENTS/_TEMPLATE SPORSHO/CLIENTS/acme-corp
```

Kebab-case slug. Then fill in every file and delete the template wording.

## Structure

```
CLIENTS/
├── README.md              ← this file
├── _TEMPLATE/             ← copy this
│   ├── PROFILE.md
│   ├── EDITING-RULES.md
│   ├── BRAND.md
│   ├── REVISION-LOG.md
│   └── DELIVERY.md
└── acme-corp/             ← a real client
```

## Rules

### 1. Only record differences from house style
`EDITING-RULES.md` should contain **only what differs** from
`SPORSHO/EDITING-RULES/HOUSE-STYLE.md`. If the house style changes, you do not want
forty client files to go stale.

### 2. Precedence: client rules win
```
1. Explicit instruction in this session
2. Client rules                    ← wins over house style
3. Sporsho house style
4. OpenMontage defaults
```
When a client rule overrides house style, **log it** in their `REVISION-LOG.md` so the
divergence stays visible rather than becoming folklore.

### 3. Revision log is mandatory
Every client feedback round gets a row with a **root cause**. This is what feeds
`SPORSHO/MEMORY/` and `CLIENT-TASTE.md`. See
`SPORSHO/WORKFLOWS/REVISION-ROUND.md`.

### 4. Ask the register, don't guess
`urgent` / `steady` / `calm` changes pacing, cut style, and music choice. If a client's
register is unclear, **ask**. Guessing the register is the most common cause of a
`taste-mismatch` revision and a wasted render cycle.

### 5. No client footage in this repo
Only text. Footage lives at `D:\SPORSHO AI\clients\<slug>\`. See
`docs/sporsho/LOCAL-MEDIA.md`.

### 6. Clients are never deleted, only archived
When a client leaves, move the folder to `CLIENTS/_archived/<slug>/`. The taste
knowledge stays available, and the revision history stays intact if they return.

## Where Things Belong

| Information | Goes in |
|---|---|
| Client's brand colours, fonts, tone | `PROFILE.md` / `BRAND.md` |
| "Cuts feel rushed, slow them down" | `EDITING-RULES.md` — plus a `REVISION-LOG.md` row |
| "They said 'energetic' but approved slow edits" | `SPORSHO/MEMORY/CLIENT-TASTE.md` |
| Export spec, naming convention | `DELIVERY.md` |
| Client's footage | `D:\SPORSHO AI\clients\<slug>\footage\` |
| Their reference videos | `D:\SPORSHO AI\clients\<slug>\references\` |
| Analysis of those references | `SPORSHO/REFERENCES/<slug>/` (markdown only) |

## Starting Out

Don't build empty client folders speculatively. Create one when you have one.

Start with the two files that pay off immediately: `PROFILE.md` (who they are) and
`EDITING-RULES.md` (how they differ). `BRAND.md`, `DELIVERY.md`, and `REVISION-LOG.md`
fill in as you actually work with them.
