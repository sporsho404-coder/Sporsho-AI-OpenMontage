# Client Template

Copy this folder to `SPORSHO/CLIENTS/<client-slug>/` and fill it in.
Client folders are **never** modified by upstream updates.

---

## Create A New Client

```bash
cp -r SPORSHO/CLIENTS/_TEMPLATE SPORSHO/CLIENTS/acme-corp
```

Use a kebab-case slug. Then fill in every `{{PLACEHOLDER}}` below and delete
`_TEMPLATE`-only wording.

---

## What Goes In A Client Folder

| File | Purpose | Required |
|---|---|---|
| `PROFILE.md` | Who they are, what they want, their specs | Yes |
| `EDITING-RULES.md` | Their specific cut/pacing/caption rules | Yes |
| `BRAND.md` | Colours, fonts, logos, tone of voice | If they have brand assets |
| `REVISION-LOG.md` | Every client feedback round, and what changed | Yes — this is the learning input |
| `DELIVERY.md` | Export specs, naming, where files go | Yes |
| `references/` | **Notes about** reference videos (never the video files) | Optional |

---

## PROFILE.md Template

```markdown
# {{CLIENT NAME}}

- **Slug:** {{client-slug}}
- **Since:** {{YYYY-MM-DD}}
- **Contact:** {{name, role}}
- **Primary pipeline:** {{talking-head | clip-factory | hybrid | cinematic | ...}}
- **Content types:** {{e.g. 9:16 short-form talking head, 3 per week}}

## What They Want

{{2-3 sentences in their own words. Quote them if possible.}}

## Audience

{{Who watches this, on what platform, in what mood.}}

## Non-Negotiables

- {{e.g. Never crop the speaker's hands off frame.}}
- {{e.g. Captions must be on for every platform.}}

## Known Dislikes

- {{e.g. Hates hard cuts mid-sentence.}}
- {{e.g. No stock footage of people shaking hands.}}

## Approval Chain

{{Who signs off. How many revision rounds are included.}}
```

---

## EDITING-RULES.md Template

Start from [`../../EDITING-RULES/HOUSE-STYLE.md`](../../EDITING-RULES/HOUSE-STYLE.md)
and **only record differences.** Do not restate the house style — if the house style
changes, you do not want 40 client files to go stale.

```markdown
# {{CLIENT NAME}} — Editing Rules

Base: SPORSHO/EDITING-RULES/HOUSE-STYLE.md
Only differences from the house style are listed here.

## Cut Behaviour
- {{e.g. Longer holds: minimum 1.2s per shot, not the house 0.8s.}}

## Pacing
- {{e.g. Slower: they want "calm authority", not "high energy".}}

## Captions
- {{e.g. Brand font, always bottom-third, never more than 6 words per card.}}

## Audio
- {{e.g. Music bed at -22 LUFS under voice, not -18.}}

## Colour
- {{e.g. Playbook: styles/custom/{{client}}-look.yaml}}
```

---

## REVISION-LOG.md Template

This is the single most valuable file in the folder. It is what makes the system learn.

```markdown
# Revision Log — {{CLIENT NAME}}

| Round | Date | Deliverable | Feedback | Root cause | Rule added |
|---|---|---|---|---|---|
| 1 | {{date}} | {{project}} | "Cuts feel rushed" | House default is aggressive; they are slower-paced | Set min shot hold 1.2s |
| 2 | {{date}} | {{project}} | "Logo wrong shade" | Brand hex not recorded | Added to BRAND.md |

## Root Cause Vocabulary

Use one of these, so patterns become visible across clients:

- `taste-mismatch` — we made it well, they wanted something else
- `rule-missing` — no rule existed, so a default was applied
- `rule-ignored` — a rule existed but was not applied
- `asset-quality` — source footage or generated asset was too weak
- `spec-error` — wrong resolution, codec, loudness, or naming
- `technical-defect` — an actual bug in the edit
```
