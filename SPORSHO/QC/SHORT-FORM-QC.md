# Short-Form QC (9:16)

Additional gate for vertical deliverables. Runs **in addition to**
[`PRE-DELIVERY-CHECKLIST.md`](PRE-DELIVERY-CHECKLIST.md).

---

## The Three-Second Test

Watch only the first 3 seconds.

- [ ] Does the content start immediately, with no logo/title card?
- [ ] Is the opening line the strongest available line?
- [ ] If the source's first line was weak, was the video re-opened on a stronger one?
      (and was that decision stated?)
- [ ] Would **you** keep watching? If not, the hook is wrong regardless of what the rules say.

## Framing

- [ ] Reframed with `auto_reframe`, not centre-cropped
- [ ] Subject's head fully in frame, with sensible headroom
- [ ] Subject's hands in frame if they're gesturing meaningfully
- [ ] Subject in the upper-middle third
- [ ] Head does not drift out of frame across the clip
- [ ] Frames actually inspected via `frame_sampler` — not assumed

## Safe Zones

- [ ] All text clear of bottom ~15%
- [ ] All text clear of right edge ~12%
- [ ] No key action behind platform UI areas

## Captions

- [ ] Present (mandatory for short-form — most viewing starts muted)
- [ ] ≤ 7 words per card
- [ ] Legible at actual phone size, not at editor zoom
- [ ] Contrast passes AA
- [ ] In sync after all cuts

## Audio

- [ ] Passes the phone-speaker test
- [ ] Music does not compete with voice
- [ ] No clipping

## Pacing

- [ ] Shot holds within the register's range (`EDITING-RULES/HOUSE-STYLE.md`)
- [ ] No stretch longer than ~3s without a visual change in `urgent` register
- [ ] `lib/slideshow_risk.py` shows no slideshow risk
- [ ] B-roll coverage within the register's range

## Ending

- [ ] Lands a payoff — does not just stop
- [ ] No dangling sentence or unfinished thought
- [ ] If there's a CTA, it appears long enough to read (≥1.5s)
- [ ] Last frame is intentional, not a random mid-motion frame

## Originality (for reference-driven work)

- [ ] Inspired by the reference format, not a copy of its content
- [ ] Would the original creator recognise this as derivative, or as a rip-off?

---

## Failure Modes Ranked By How Often They Actually Happen

1. **Weak hook** — the most common and most costly failure
2. **Caption out of safe zone** — clipped by platform UI on real devices
3. **Centre-crop decapitation** — head cut off by naive reframing
4. **Audio mixed for headphones** — unintelligible on a phone
5. **Ending that just stops** — no payoff, no landing
6. **Caption sync drift** — usually caused by a J/L-cut applied after captioning
