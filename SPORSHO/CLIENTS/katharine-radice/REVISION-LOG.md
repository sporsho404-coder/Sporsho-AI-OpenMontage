# Revision Log — Katharine Radice

| Round | Date | Deliverable | Feedback | Root cause | Rule added |
|---|---|---|---|---|---|
| 0 | 2026-09-19 | `revision-top-tips` v01 — **never rendered** | (no client review: source bytes never reached the edit environment) | `technical-defect` — footage was committed to GitHub as LFS pointers; `SPORSHO/INTEGRATIONS/GITHUB.md` says *GitHub holds intelligence, not footage*, and `CLIENTS/README.md` rule 5 forbids client footage in the repo. Both routes to the bytes (raw URL, LFS batch + media host, Actions relay) are blocked from this sandbox | Footage transfer must be non-GitHub (drive mount / direct upload), recorded in `DELIVERY.md` |
| 1 | 2026-09-21 | review of the pacing and polish in the working cut | "Pacing too aggressive, narration/visual mismatch, B-roll and supporting visuals skipped too fast. Fix typography, motion design, transitions. Premium, high-end fintech/trading standard. **Do not shorten for speed — extending duration is acceptable.**" | `rule-missing` — no client profile existed, so pacing was tuned against thresholds invented in-session instead of `HOUSE-STYLE.md`'s register table; register was never declared ("ask the register, don't guess"). Plus `rule-ignored` — B-roll was planned after the cut instead of with it, and captions were not re-checked after J/L shifts | `EDITING-RULES.md` written: register `calm`, holds 4.5–7.0 s, no speed-up tightening, inserts 4.0–6.0 s placed after the claim, runtime follows content, duration override logged, playbook typography mandatory |
| 1b | 2026-09-21 | same review | "Review ALL provided folders, scripts, brand guidelines, references — identify what was overlooked" | `rule-ignored` — `SPORSHO/` (37 files: `EDITING-RULES/*`, `WORKFLOWS/*`, `QC/*`, `styles/*.yaml`, `references` protocol) existed in the repo and was not read before the first pass; `REFERENCES/INDEX.md` was empty because HUTCHAIN 3 was never run through the reference workflow | Route block + `PRE-DELIVERY-CHECKLIST.md` layers are now executed as gates, not consulted optionally; job recorded in `SPORSHO/JOBS/revision-top-tips/RUNBOOK.md` |

---

## Open Questions (blocking, cheap to answer)

1. **Register** — `calm` as recorded, or `steady`? One word decides the whole pace model.
2. **Platform** — if YouTube Shorts is a target, 60.0 s is a hard technical cap; the
   point list must shrink instead of the pacing. Which platforms?
3. **`K Radice bio & headshot.docx`** — needed before any positioning line, key-point
   title, or CTA copy goes on screen. Nothing has been invented in its absence.
4. **Music** — no licensed track supplied. Confirm "no bed" is what she wants (house
   default for this client is silence under voice).
5. **Approval chain / rounds included** — not recorded anywhere in the brief.
