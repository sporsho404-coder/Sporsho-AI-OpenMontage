# Workflow: Revision Round

- **Applies to:** any pipeline, after a client has seen a deliverable
- **Key file:** `SPORSHO/CLIENTS/<client>/REVISION-LOG.md`

---

## Why This Workflow Exists

OpenMontage has a revision mechanism, but it is **not this one.**

Upstream's `max_revisions_per_stage` and `max_send_backs` control how many times a
**pipeline stage** can be sent back *internally* before the run escalates. That is
stage-level quality control.

**Client feedback rounds are a different thing**, and upstream has no concept of them.
This is one of the genuine gaps the Sporsho layer fills.

---

## The Rule

**Every client revision becomes a rule or a memory entry.**

A revision that gets fixed and forgotten costs you again on the next project.
A revision that becomes a rule is paid for once.

## Steps

### 1. Capture verbatim

Record what the client actually said, in their words. Do not translate it into
editorial language yet — the wording carries information.

```
"the cuts feel too rushed"
```
is not the same as
```
"increase minimum shot hold"
```
The first tells you their *feeling*. The second is only one possible fix for it.

### 2. Diagnose the root cause

Use the vocabulary in `CLIENTS/_TEMPLATE/PROFILE.md`:

| Root cause | Meaning | Fix goes where |
|---|---|---|
| `taste-mismatch` | The edit was competent; they wanted something else | Client `EDITING-RULES.md` |
| `rule-missing` | No rule existed, so a default was applied | House style **or** client rules |
| `rule-ignored` | A rule existed and was not applied | `MEMORY/` — process failure |
| `asset-quality` | Footage or generated asset was too weak | Flag to client; may need reshoot |
| `spec-error` | Wrong resolution / codec / loudness / naming | Client `DELIVERY.md` |
| `technical-defect` | An actual bug | Check `MEMORY/FAULTS.md`; may be upstream |

### 3. Decide where the fix belongs

This matters for long-term maintainability:

- **This client only?** → `CLIENTS/<client>/EDITING-RULES.md`
- **All clients?** → `SPORSHO/EDITING-RULES/`
- **A repeat process failure?** → `SPORSHO/MEMORY/`
- **An actual bug in OpenMontage?** → note it; consider reporting upstream
  (do **not** patch upstream files in this repo — see `INTEGRATION.md`)

### 4. Apply the fix

Do not just patch the current deliverable and move on. A revision fixed only in the
current file is a revision you will pay for again.

### 5. Re-run and re-QC

Full `SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`. A revision is a new delivery.

### 6. Log it

Add a row to `CLIENTS/<client>/REVISION-LOG.md`:

```
| Round | Date | Deliverable | Feedback | Root cause | Rule added |
```

---

## Revision Patterns To Watch

If the same root cause appears twice for one client, it is now a **rule gap**, not
a revision. Promote it immediately.

If the same root cause appears across **different** clients, it is a **house style
gap**. Promote it to `SPORSHO/EDITING-RULES/`.

| Symptom across multiple clients | Likely house-style gap |
|---|---|
| "too fast" / "too slow" | Register is being guessed, not asked |
| "music too loud" | `AUDIO-RULES.md` defaults need revisiting |
| "captions hard to read" | Contrast or size defaults too aggressive |
| "feels generic" | Hook rule or B-roll relevance not being applied |

## Known Limitations

- Revision tracking is documentation, not automation. Nothing enforces that you log it.
  If this becomes a burden, the fix is a small script — not skipping the log.
- Round counts against a client's included revisions must be tracked manually in
  `CLIENTS/<client>/DELIVERY.md`.
