# Source verification — `Revision Top Tips` (radice-revision-top-tips)

Verified 2026-09-21. This is the record of what the source footage actually is, measured from the
bytes — not inferred from a manifest or trusted from a tool's own summary. Everything below was
recomputed from `/home/user/k-radice-edit/ingest/1.mp4 … 10.mp4`.

## 1. Retrieval — 10/10

| # | SHA-256 (first 23 hex) | bytes | == manifest LFS OID |
|---|--------------------------|-------|---------------------|
| 1 | `072ba3362aa42aeeef76279a` | 12,531,687 | ✓ |
| 2 | `4e8cd9081b7bcf5f1fe25975` | 17,010,494 | ✓ |
| 3 | `afe1dd2eaf48d80a7ac41958` | 16,145,549 | ✓ |
| 4 | `35db4f353eb83f5964252683` | 22,338,629 | ✓ |
| 5 | `8ff51c83ebfb26571c6bff53` | 20,929,766 | ✓ |
| 6 | `71e5ec70f4eb0b11a63cf36b` | 21,272,945 | ✓ |
| 7 | `1c22b20df7e74ed3415f58eb` | 14,195,796 | ✓ |
| 8 | `768721ba0141bf375d80874b` | 18,985,241 | ✓ |
| 9 | `404ebfd96ccd3c8b1329e1c1` | 21,918,852 | ✓ |
| 10 | `50652756e62fe89a48117279` | 22,658,579 | ✓ |

Sum **187,987,538 B**, exactly `total_expected_bytes` in `ingest-manifest.json`. Hashes computed
twice, independently (`sha256sum` and Python `hashlib`), not only from the receiver's counter.
Delivered by the operator's browser through the inbound uploader (`SPORSHO/JOBS/revision-top-tips/`).

## 2. What the parts are

Ten sequential chunks of **one** continuous 30 fps take — same room, same framing, same outfit,
audio running unbroken across all nine joins. Never edit them separately; join 1→10.

| part | frames | video s @30 | container s | audio samples | audio−video | coded size |
|------|--------|-------------|-------------|---------------|-------------|------------|
| 1 | 284 | 9.467 | 9.473 | 417,792 | +7.1 ms | 1080×1920 |
| 2 | 392 | 13.067 | 13.073 | 576,512 | +6.2 ms | 1080×1920 |
| 3 | 372 | 12.400 | 12.422 | 547,840 | +22.7 ms | 1080×1920 |
| 4 | 523 | 17.433 | 17.438 | 769,024 | +4.9 ms | 1080×1920 |
| 5 | 489 | 16.300 | 16.300 | 718,848 | +0.4 ms | 1080×1920 |
| 6 | 495 | 16.500 | 16.509 | 728,064 | +9.4 ms | 1080×1920 |
| 7 | 329 | 10.967 | 10.983 | 484,352 | +16.4 ms | 1080×1920 |
| 8 | 444 | 14.800 | 14.814 | 653,312 | +14.3 ms | 1080×1920 |
| 9 | 514 | 17.133 | 17.136 | 755,712 | +3.0 ms | 1080×1920 |
| **10** | **638** | **21.267** | 21.269 | 937,984 | +2.8 ms | **720×1280** |

Totals: 4480 frames = 149.3333 s of video; 6,585,600 audio samples @ 44.1 kHz = 149.3333 s once
each part's tail padding is removed. All parts 30/1 CFR, audio AAC-LC 44.1 kHz stereo.

**Seam forensics (duplicate/dropped frame test).** Mean absolute luma difference across each join,
compared with the motion rate on both sides of it. Ratios 0.97×–1.20× of baseline at all nine joins
→ no duplicated frame (would read ≈0) and no dropped frame or scene jump (would read ≫3×). The
chunking is lossless; nothing is missing from the middle.

## 3. Two defects that a naive reconstruction hides

`ffmpeg -f concat -c copy` of these ten files — which looks healthy, and which `reconstruct.py`
produced as `revision-top-tips_full.mov` — is **not** a safe edit master:

1. **Mixed coded geometry.** Parts 1–9 are 1080×1920, part 10 is 720×1280, so the MP4 changes
   frame size mid-stream at t≈128.1 s. It decodes without error and many players/muxers then
   mishandle the tail (or drop it).
2. **Duration-driven drift.** The concat demuxer offsets each part by its *container* duration,
   which overstates its frame count by 0.4–22.7 ms. Result: two 66.7 ms timeline gaps (non-existent
   "missing frames") at the joins after parts 3 and 7, non-monotonic DTS at part 10, and audio
   149.6526 s against video 149.4402 s → **+0.2196 s of A/V drift by the end**. That is ~6 frames of
   lip-sync error growing through the piece: exactly the "narration and visuals don't line up"
   complaint, produced by the join and not by any cut.

**How the master was rebuilt instead** (`work/` scripts, verified by full decode):
concat the ten sources through a filter graph, `scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p`
per input so the concat inputs match, then `setpts=N/(30*TB)` over the **whole** stream so every
frame is numbered by index at exactly 1/30 s; audio rebuilt from each part's decoded PCM trimmed to
exactly `frames/30` seconds, concatenated, then muxed with `-c copy` and no `-shortest`.

`master_norm.mov` — 4480 frames, uniform 1080×1920, monotonic PTS, spacing 33.333–33.334 ms,
video 149.3333 s, audio 6,585,600 samples @ 44.1 kHz = 149.3333 s, **A/V delta 0.00000 s**,
H.264 High CRF14 yuv420p bt709, 24-bit PCM audio, 282,698,600 B. `SPORSHO/QC/verify_master.py`
reports PASS on it and FAIL on the copy-join. That is the file the edit works from; the ten parts
and `revision-top-tips_full.mov` are untouched as evidence.

## 4. Picture and sound properties that change the edit plan

* **Loudness −26.0 LUFS integrated, peak −5.3 dBTP, LRA 5.6 LU.** The voice is ~10 LU below the
  house target (−16 LUFS / −1.0 dBTP). Headroom is available, so gain + gentle limiting gets there
  without clipping. Do **not** run `silence_cutter` at its default absolute threshold first: on a
  recording sitting 10 dB low, an absolute −35 dB cut point clips quiet speech. Either normalise
  before cutting, or use a relative threshold and re-check every cut against the transcript.
* **No black frames** (`blackdetect=d=0.06:pix_th=0.10` found none) and **no silent passage ≥0.35 s**
  below −55 dB — there is continuous room tone, so dead air here is *content* pauses, not digital
  silence, and must be judged against speech, not against a dB floor.
* **Framing (75 frames sampled, face detected in 75/75).** Forehead top median y=451 (23.5% from
  top; range 18.8–26.5%), face centre x=502 of 1080 (38 px left of centre; range 408–647 as she
  gestures), face width median 477 px (44.2% of frame). Chin never below y=988, caption band starts
  at y=1632 → **lower thirds never cover her face**. Native 9:16 vertical, no rotate metadata, so
  no reframe is needed; a 105–115% punch-in stays inside frame and leaves the headroom intact.
* **The tail matches the rest in framing** (part 10 vs parts 1–9: forehead +12 px, face width
  −16 px) — same camera position and shot size, so only resolution differs, no visual jump in
  composition at t=128.1 s.
* **Caveat to report, not to fix by re-splitting:** the closing 21.267 s was exported at 720×1280
  and therefore carries fewer pixels than the rest; after upscaling it will read slightly softer in
  the last act. A 1080×1920 re-export of just that segment would recover it if the client still has
  the original export.

## 5. Still open before a render (none of these are byte-related)

1. **Transcript / caption text** — no `faster-whisper` weights are reachable (model host is blocked
   by the sandbox egress filter, see `SPORSHO/MEMORY/FAULTS.md`). Captions must come from the client's
   source text or a transcript she supplies; nothing is to be invented.
2. `K Radice bio & headshot.docx` text — positioning source, still only on her machine.
3. `HUTCHAIN 3` reference — never analysed; style reference only, no fabricated findings.
4. Register confirmation (`calm`, per `PROFILE.md`) and the platform list for duration caps.
5. No provider keys in this sandbox → no stock B-roll or licensed music pulls. If she has a licensed
   track she must supply it; otherwise the render ships voice-only (allowed by `AUDIO-RULES.md`).
