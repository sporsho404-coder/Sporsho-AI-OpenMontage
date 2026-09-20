# Katharine Radice — Editing Rules

Base: `SPORSHO/EDITING-RULES/HOUSE-STYLE.md` + `CUT-RULES.md` + `BROLL-PACING.md` +
`CAPTIONS-TYPOGRAPHY.md` + `AUDIO-RULES.md`.

**Only differences from the house style are listed here.** Precedence
(`SPORSHO/CLIENTS/README.md`): session instruction → client → house → upstream.

---

## Register

`calm`. Every number below is derived from it; where the house table and this file
disagree, this file wins for this client only.

| Parameter | House `calm` | This client |
|---|---|---|
| Shot hold | 3.0–8.0 s | 3.0–8.0 s, **skew long** (aim 4.5–7.0 s on talking head) |
| B-roll coverage | 40–70 % of runtime | **40–55 %** — floor of the band, because "B-roll filling every gap" is a stated dislike |
| Insert length | 3.0–6.0 s | **4.0–6.0 s**, never below 3.0 s |
| Transitions | long holds, few cuts | hard cut or J/L only on speech; **no dissolve on a talking-head seam** |

## Cut Behaviour

- **Runtime follows content, not the other way round.** If a point needs 9 s to land, it
  gets 9 s. Do not compress a sentence to hit a duration target.
- Trim only what carries no information: breath-level dead air, false starts, repeats.
  Keep the pause *before* an emphasis word even when it is long — that pause is the
  premium signal, not a mistake.
- **No cut may land inside a word**, and no cut within 0.12 s of a word boundary —
  verified against transcript words, not by ear. (`CUT-RULES.md`)
- Never dissolve to hide a jump cut. Cover it with B-roll, else punch in 105–115 %.
- Speed stays 1.0. **No speed-ramping, no 1.08× tightening** for this client: the
  2026-09-21 note is specifically that the piece feels rushed.

## Duration

- Target **55–75 s**. This **overrides** `WORKFLOWS/SHORT-FORM-9x16.md` ("20–45 s sweet
  spot, 60 s ceiling"), on the client's explicit instruction of 2026-09-21 that a longer
  video beats a rushed one. Logged as a client difference rather than a silent break.
- ⚠️ **YouTube Shorts hard-caps at 60.0 s.** If Shorts is a target platform, the ceiling
  is a technical limit, not a taste preference: cut the *number of points*, do not speed
  up the delivery. Confirm which platform this ships to before locking the list.

## B-roll & Supporting Visuals

- Every insert must illustrate **the sentence it sits under**, and start **after** the
  claim is made (house rule; the 2026-09-21 note is that this was missed).
- One idea per insert. Never overlay text and B-roll on the same sentence.
- Return to the face before the audience loses the speaker — within the same thought,
  not on a timer.
- B-roll comes from **client-supplied/licensed material only** in this environment:
  `pexels_video` / `pixabay_video` / `clip_search` are unavailable here (no network,
  no keys — see `SPORSHO/INTEGRATIONS/PROVIDERS.md`), and generic stock is exactly the
  "template look" she rejects. No source + licence record → the asset does not ship.
- Where there is no honest visual for a sentence, use a **typographic insert** from the
  playbook (`overlays.key_term` / `stat_card`), not stock. A blank field under a strong
  line reads as confidence.

## Typography & Motion (playbook: `styles/premium-minimalist.yaml`)

The look is the playbook's, not an invented one — see `BRAND.md` for why (client brand
assets have not been supplied).

- Inter throughout: display 700–800, caption weight 500, tracking **−2 % to −4 %** on
  display type; max 2 typefaces.
- Cards: `#FFFFFF` field, `#D1D5DB` 1px border, 6 px radius, `0 1px 6px rgba(17,24,39,.08)`
  shadow; cobalt `#2563EB` only for hierarchy; text `#111827`.
- Contrast validated with `styles/playbook_loader.validate_contrast()` (4.5:1 body,
  3.0:1 large) — **not by eye**. Colour-blind safety via `check_color_blind_safety()` if
  colour ever carries meaning.
  *(House files cite `lib/playbook_loader.py`; the real module is
  `styles/playbook_loader.py` — logged in `MEMORY/FAULTS.md`.)*
- Entrance ≤200 ms, fade-up ~12 px with opacity ramp, **no bounce, no spin, no scale pop**.
  Exit: soft fade with slight y-offset. Transition duration 0.45 s.
- Banned by playbook anti-patterns and therefore by this file: decorative gradients,
  generic corporate-blue template cards, "fast kinetic transitions that reduce
  comprehension".

## Captions

- ≤7 words per card, ≤2 lines, no orphan word on line 2; never split a proper noun.
- Position: lower third **above** the bottom 15 %; clear of right 12 % and top 10 %.
- Follow the speech; **never lead it by more than 3 frames**. Re-check sync after every
  J/L cut (this is failure mode #6 in `CAPTIONS-TYPOGRAPHY.md`, and the likely cause of
  the "narration/visual mismatch" note).
- Word-by-word reveal is the house default; for this client use **phrase-level** reveal
  with a ≤200 ms fade — per-word popping reads as TikTok-native, which she rejects.
- Captions are burned from transcript words. If there is no transcript, **say so**:
  `transcriber` is not runnable here (no `.env`, and huggingface.co is blocked —
  `MEMORY/FAULTS.md`). Never caption from guesswork.

## Audio

- Voice −16 LUFS integrated, −1.0 dBTP ceiling, `audio_enhance` for cleanup only.
  EQ must not thin the voice for "broadcast brightness" — warmth is part of the trust signal.
- **No music bed** unless a licensed track file is delivered. Then: −18…−22 LUFS under
  voice, `audio_mixer` ducking, fade at a musical boundary, ending 1–2 s before the final
  frame, no vocals under speech.
- No SFX by default. The playbook allows "small tactile ticks", but on a single-take
  talking head they read as template ornament. Require an explicit ask.

## Colour

- Neutral-warm grade, skin first: no teal-and-orange, no lifted blacks past ~3 %, no
  added grain on a phone-sourced image.
- Same grade on every insert so the source and the B-roll share one look
  (`PRE-DELIVERY-CHECKLIST.md` → "Grade consistent across all sources and inserts").
