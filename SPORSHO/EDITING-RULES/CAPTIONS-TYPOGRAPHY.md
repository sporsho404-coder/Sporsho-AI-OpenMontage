# Captions & Typography

**Tools:** `tools/subtitle/subtitle_gen.py`, `tools/video/remotion_caption_burn.py`
**Skills:** `skills/core/subtitle-sync.md`, `skills/creative/typography.md`,
`.agents/skills/remotion*`, `.agents/skills/gsap*`
**Playbook:** custom looks go in `styles/custom/*.yaml` (see INTEGRATION.md)

---

## The Split Of Responsibility

| Concern | Owner |
|---|---|
| Caption timing, word alignment | OpenMontage (`transcriber` + `subtitle_gen`) |
| Caption rendering | OpenMontage (`remotion_caption_burn`) |
| **Caption style: font, size, position, animation** | **Sporsho** |
| **Accessibility (contrast, safe areas)** | **Sporsho** (with upstream validators) |

Do not rebuild caption timing. Wire into the existing tools and control the *look*.

---

## Caption Rules

- **Max 7 words per caption card** (house default)
- **Max 2 lines** on screen at once
- **Position:** lower third, clear of platform UI (see safe zones below)
- **Timing:** captions follow speech closely; never lead it by more than ~3 frames
- **Never** caption a word before it is spoken — viewers notice and it reads as broken
- **Never** split a proper noun across two cards
- Punctuation: omit terminal periods on short cards; keep question and exclamation marks

## Mobile Safe Zones (9:16)

| Zone | Keep clear |
|---|---|
| Bottom ~15% | Platform UI, progress bar, CTA buttons |
| Right edge ~12% | Like/comment/share stack |
| Top ~10% | Platform header |

Place captions in the lower third but **above** the bottom 15%.

---

## Typography Rules

- **Max 2 typefaces** in a single video (one display, one body)
- Type scale: use a modular ratio via the playbook `scale_system`
  (`minor_third` is the Sporsho default)
- **Weight:** 700+ for on-screen display type at mobile size; 400–500 for body
- **Tracking:** slightly negative for large display type (−2% to −4%)
- **Never** put body text over busy footage without a scrim or solid backing

## Contrast (Non-Negotiable)

OpenMontage ships the validator. Use it — do not eyeball contrast.

```python
from lib.playbook_loader import validate_contrast, check_color_blind_safety
validate_contrast("#FFFFFF", "#1F2937")     # → ratio + AA/AAA pass/fail
check_color_blind_safety(["#E11D48", "#16A34A"])  # → flagged confusion pairs
```

Requirements:

- Normal text: WCAG AA = 4.5:1 minimum
- Large text (≥24px bold or ≥32px): AA = 3.0:1 minimum
- Never rely on red/green distinction alone — that is the most common colour-blind pair

---

## Motion For Captions

Source of truth for animation technique: `.agents/skills/gsap-*`,
`.agents/skills/framer-motion`, `.agents/skills/remotion-best-practices`.

Sporsho rules on top:

- Entrance animation ≤ 200ms. Slow text feels laggy on short-form.
- **No bouncing or spinning text.** It reads as gimmicky and hurts comprehension.
- Word-by-word reveal is the house default; full-card is acceptable for `calm` register.
- Exit animations are optional — often a clean cut is better.
- Animations must not change the text's position between cards (causes reading friction).

---

## Common Failure Modes (check these)

1. Caption covers the speaker's mouth — violates house overlay discipline
2. Caption drifts out of sync after a J/L-cut shifted the audio
3. Two lines wrap badly, orphaning a single word
4. Low-contrast caption over light footage
5. Caption extends into the platform UI zone
6. Emoji renders as a missing-glyph box in the chosen font

Validate with `visual_qa` — it includes a caption occlusion check that compares
brightness in the face zone vs the caption zone.
