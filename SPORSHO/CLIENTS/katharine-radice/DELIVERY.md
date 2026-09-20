# Katharine Radice — Delivery

Specs below are **stated or derived-and-flagged**, never assumed silently. Anything
marked `CONFIRM` was not given in the brief.

---

## Export Spec

| Field | Value | Basis |
|---|---|---|
| Container / codec | MP4, H.264 High profile, yuv420p | social standard |
| Resolution | 1080 × 1920 | 9:16 deliverable |
| Frame rate | **match the source exactly** — read with `audio_probe`, do not convert | `PRE-DELIVERY-CHECKLIST.md`: "Resolution, codec, and frame rate match the client's spec exactly" |
| Bitrate | CRF 18, 2-pass equivalent quality; no VBR starvation on text | legibility of burned captions |
| Audio | AAC-LC 192 k, mono→stereo only if source is stereo | phone speakers |
| Loudness | −16 LUFS integrated, −1.0 dBTP ceiling | `EDITING-RULES/AUDIO-RULES.md` |
| Captions | burned in (no sidecar SRT unless asked) | most vertical playback starts muted |
| Duration | 55–75 s target; **60.0 s hard cap if YouTube Shorts is in scope** | client override, see `EDITING-RULES.md` |

## Naming

Proposed, pending client convention:

```
radice-revision-top-tips_9x16_v01.mp4
radice-revision-top-tips_9x16_qc/            ← contact sheet, loudness report, QC log
```

Client folder convention is not recorded → **ask once, then freeze it here.**

## Where Files Go

- Working project workspace: `D:\SPORSHO AI\projects\radice-revision-top-tips\`
  (`OPENMONTAGE_PROJECTS_DIR`, per `INTEGRATIONS/LOCAL-DRIVE.md`)
- Source footage: `D:\SPORSHO AI\clients\katharine-radice\footage\revision-top-tips\`
  — **never in this repository** (`CLIENTS/README.md` rule 5)
- Final render: to the client by the route she names. **Not via a GitHub commit.** The
  10 LFS-pointer parts of 2026-09-19 could not be read back from this environment at all,
  which is the direct consequence of that rule being broken.

## Delivery Payload (what she actually receives)

1. The 9:16 master mp4.
2. A QC one-pager: loudness numbers, duration, cut count, caption word count, safe-zone
   check result, contact-sheet frames.
3. A short note listing **what was cut and why** (dead air / false start / repeat) and
   **what was deliberately left alone** (emphasis pauses, the hook).
4. Anything the client still owes before a second round can be trusted: the bio
   document, a licensed track if music is wanted, brand files if a logo is wanted.

## Revision Rounds

`UNKNOWN — ask.` No round allowance has been recorded in any brief. Do not promise
unlimited rounds; do not bill-log rounds that were never agreed.

## Do Not Deliver Until

- [ ] `SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md` layers 1–5 all ticked with evidence
- [ ] `SPORSHO/QC/SHORT-FORM-QC.md` run against the render, frames inspected by eye
- [ ] Every on-screen claim traced to the footage or the client document
- [ ] No OpenMontage repo asset used as if it were the client's brand (`BRAND.md`)
