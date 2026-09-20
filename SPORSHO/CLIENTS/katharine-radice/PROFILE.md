# Katharine Radice

- **Slug:** `katharine-radice`
- **Since:** 2026-09-19 (first working session on `Revision Top Tips`)
- **Contact:** not recorded — Katharine is the approver on every note seen so far. **Ask before the next round.**
- **Primary pipeline:** `talking-head` (**beta** upstream — see `../../WORKFLOWS/TALKING-HEAD-TO-SHORT.md`)
- **Content types:** 9:16 short-form from a single self-shot talking-head source

> **Provenance of this profile.** Everything below is either (a) stated by the client in
> the session brief, or (b) marked `UNKNOWN — ask`. Nothing here is inferred from her
> practice, credentials, or audience. `K Radice bio & headshot.docx` was named as the
> positioning source of truth but **has not been delivered**, so no biography,
> qualification, service description, statistic or testimonial may be used on screen.

## What They Want

> "Professional talking-head edit with strong opening, useful key points, accurate
> captions, colour and audio polish, appropriate CTA — premium, not template."

Read against the revision note of 2026-09-21, "premium" here means **unhurried and
deliberate**, not more effects. The client said explicitly that a longer video is
preferable to a rushed one that misses information. See
`MEMORY/CLIENT-TASTE.md` → *Stated vs Observed*.

## Audience

`UNKNOWN — ask.` Assumed working basis (state, do not sell on it): people who already
know what the topic is and want a practitioner's view, watching on a phone, often muted
first. Replace this line when the bio document lands.

## Non-Negotiables

- **Nothing invented.** No claim, qualification, statistic, testimonial, or medical/
  health framing that is not present in the source footage or the client document.
- **Meaning is preserved.** Cuts may remove dead space and mistakes; they may not
  re-order an argument or tighten it into a different claim.
- **No Premiere Pro for the edit.** Deliver via FFmpeg/Python tooling (their
  `tools/` pipeline). Premiere may be opened only to inspect.
- **Source footage is never modified.** `Revision Top Tips` parts are read-only inputs.
- **Music only if a licensed track is actually supplied.** None has been → no bed.
- **CTA must come from the source content**, and must stay fully readable ≥1.5s.

## Known Dislikes

- Template / TikTok-native look: preset transitions, emoji, bouncy text, sticker UI.
- Rushed pacing — the 2026-09-21 note calls the previous pass out by name.
- Visuals that don't match the sentence being spoken at that moment.
- B-roll used to fill every gap (equally disliked: B-roll that appears for 1s and vanishes).

## Reference Material

| Reference | Status |
|---|---|
| `HUTCHAIN 3` (client drive) | **Style reference only, never copied.** Bytes are on `D:\SPORSHO AI\`, unreachable from this environment — not yet analysed. See `references/hutchain-3.md` |
| `Revision Top Tips` 10 source parts | LFS pointers on `main`; **not readable** here. See `SPORSHO/INTEGRATIONS/GITHUB.md` rule: *GitHub holds intelligence, not footage* |
| `K Radice bio & headshot.docx` | **Not delivered.** Blocks on-screen positioning copy and the key-point list |

## Register

**`calm`** — declared, with evidence, per `../../EDITING-RULES/HOUSE-STYLE.md`
("If the client's tone is unclear, ask. Do not guess the register."):

- tone asked for: trustworthy, warm, expert-led → not `urgent`
- revision note: "pacing too aggressive… extending duration is acceptable" → not `steady`
- playbook in play: `styles/premium-minimalist.yaml` → `pace: deliberate`, min scene hold 2.75s

**To confirm in one line:** `calm`, or `steady` if she wants it to keep moving faster.
