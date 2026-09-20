# JOB: radice-revision-top-tips — runbook

```
Route:      footage + revision  (source = material to cut; the 2026-09-21 note = revision round 1)
Pipeline:   talking-head (beta upstream)  +  SHORT-FORM-9x16 layer
Client:     katharine-radice  → SPORSHO/CLIENTS/katharine-radice/
Register:   calm             (declared in EDITING-RULES.md; confirm with client)
Playbook:   styles/premium-minimalist.yaml   (provisional — client brand not supplied)
Rules:      EDITING-RULES/{HOUSE-STYLE,CUT-RULES,BROLL-PACING,CAPTIONS-TYPOGRAPHY,AUDIO-RULES}.md
            + CLIENTS/katharine-radice/EDITING-RULES.md (differences win)
Tools:      silence_cutter → video_trimmer → auto_reframe → subtitle_gen → video_compose
            (+ audio_mixer only if a licensed bed exists; visual_qa, audio_probe, frame_sampler,
             color_grade)  — all AVAILABLE in this sandbox as of 2026-09-21
Gates:      QC/PRE-DELIVERY-CHECKLIST.md (layers 1–5) + QC/SHORT-FORM-QC.md
Media root: D:\SPORSHO AI\clients\katharine-radice\footage\revision-top-tips\   (not in git)
Est. cost:  $0 — every paid provider is unreachable here (no .env, no keys)
```

---

## Why a runbook instead of a new engine

`SPORSHO/WORKFLOWS/TALKING-HEAD-TO-SHORT.md` already prescribes the stage order and the tool
names. Re-implementing that (as an earlier session did) is how house rules get silently
dropped. This directory therefore holds only **glue that upstream genuinely lacks**:
an inbound media receiver, and a verify-then-join gate.

## Blocker status (2026-09-21)

Source bytes: **0/10 parts available.** They sit on `main` as Git LFS pointers; this sandbox's
egress is SNI-filtered so the LFS object host cannot be reached at all — see
`SPORSHO/MEMORY/FAULTS.md` (entry "GitHub-held client footage") for the full route matrix.
Two working intake routes, both implemented here:

1. **`ingest_receiver.py`** — the operator's browser pushes the files in through the preview
   proxy (no egress needed). Runs on `0.0.0.0:8090`, token-gated, 4 MB resumable chunks,
   hashes each file and compares against `CLIENTS/katharine-radice/ingest-manifest.json`.
2. **GitHub republished as plain blobs** (relay workflow, or `git lfs migrate export` into a
   throwaway repo) → fetched with `gh api .../git/blobs/<sha>` + `Accept:
   application/vnd.github.raw`.

```bash
# intake (already running; the operator just opens the preview URL and drops the files)
SPORSHO_INGEST_DIR=/home/user/k-radice-edit/ingest \
  /home/user/.venv-edit/bin/python SPORSHO/JOBS/revision-top-tips/ingest_receiver.py

# verify + join, strictly 1 → 10. Refuses on any mismatch or subset.
/home/user/.venv-edit/bin/python SPORSHO/JOBS/revision-top-tips/reconstruct.py \
  /home/user/k-radice-edit/ingest /home/user/k-radice-edit/work
```

## Order of work once `reconstruct.py` passes

1. `frame_sampler` + `audio_probe` on the joined master → **look at the frames**, do not assume.
2. Transcript. `transcriber` cannot run here (needs a model from huggingface.co; no key either)
   → ask the client for word-level timings, or accept a plain transcript and align.
   **Captions are never guessed.**
3. `silence_cutter` in `mark` mode first; compare its silence map with breath/emphasis pauses
   (house floor 0.5 s; emphasis pauses above 1.5 s are kept on purpose).
4. Cut plan as an `edit_decisions` artifact (validated against
   `schemas/artifacts/edit_decisions.schema.json`), **one reason per cut**, register `calm`:
   holds 4.5–7.0 s, no speed tightening, jump cuts covered by B-roll else punch-in 105–115 %.
5. B-roll + key-point inserts planned *with* the cuts, not after: coverage 40–55 %,
   inserts 4.0–6.0 s placed *after* the claim, never over the hook, never overlay+B-roll on one
   sentence. Only assets with a recorded source+licence (client-supplied; stock search is
   unreachable here).
6. `auto_reframe` to 1080×1920 (never centre-crop), verify headroom by eye.
7. Captions: ≤7 words, above bottom 15 %, clear right 12 %/top 10 %, phrase-level reveal,
   entrance ≤200 ms, Inter 700 with −2…−4 % tracking, contrast via
   `styles.playbook_loader.validate_contrast()`; **re-check sync after every J/L**.
8. Audio: `audio_enhance` then loudness to −16 LUFS / −1.0 dBTP. No music unless a licensed
   file exists.
9. Grade with `color_grade` (neutral-warm, skin first), consistent across inserts.
10. `visual_qa` + `lib/slideshow_risk.py` + `lib/verify_scene_pacing.py` + the two QC files;
    then Layers 3–5 of the checklist, including `MEMORY/` writes.

## Do not

- Do not edit before `reconstruct.py` reports 10/10 verified.
- Do not use `assets/logo.png`, `assets/monty-*.svg`, `assets/sponsors/*`,
  `assets/signal-from-tomorrow-demo.mp4` or the `.agents/skills/**` example clips — those are
  OpenMontage's and upstream's, not the client's.
- Do not commit footage, renders, or frames to this repo.
