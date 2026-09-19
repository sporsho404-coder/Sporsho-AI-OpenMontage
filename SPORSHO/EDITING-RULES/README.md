# EDITING-RULES — Your Editorial Constitution

How Sporsho edits. This is taste written down so it can be applied consistently.

---

## Files

| File | Purpose |
|---|---|
| [`HOUSE-STYLE.md`](HOUSE-STYLE.md) | Default rules for all work |
| [`CUT-RULES.md`](CUT-RULES.md) | Cut behaviour: J/L-cuts, holds, transitions |
| [`CAPTIONS-TYPOGRAPHY.md`](CAPTIONS-TYPOGRAPHY.md) | Caption and type treatment |
| [`AUDIO-RULES.md`](AUDIO-RULES.md) | Mixing, music, sound design |
| [`BROLL-PACING.md`](BROLL-PACING.md) | B-roll selection and pacing |

Client-specific rules live in `SPORSHO/CLIENTS/<client>/EDITING-RULES.md` and
should contain **only differences** from these files.

---

## The Precedence Chain

```
1. Explicit instruction from the user in this session
2. Client profile rules                SPORSHO/CLIENTS/<client>/
3. Sporsho house style                 SPORSHO/EDITING-RULES/ (this folder)
4. OpenMontage defaults                skills/creative/*.md
```

Lower numbers win. When 2 overrides 3 or 4, log it in the client's `REVISION-LOG.md`
so the divergence stays visible.

---

## The One Rule About Rules

**Never restate an OpenMontage rule here.**

If `skills/creative/video-editing.md` says cut filler words, and this folder also says
cut filler words, you now have two sources of truth. When upstream improves their rule,
yours silently contradicts it.

This folder contains **only Sporsho decisions** — the things no upstream file could know
because they're about your taste, your clients, and your market.
