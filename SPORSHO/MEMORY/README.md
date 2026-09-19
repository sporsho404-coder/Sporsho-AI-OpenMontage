# MEMORY — The Learning Loop

This folder is what turns a tool into a brain.

---

## Is This The Biggest Gap?

**Yes.** Verified by searching the OpenMontage source at commit `08e2151`:
there is **no retrospective artifact, no lessons-learned store, and no mechanism for
learning from past edits.** The only "feedback loop" references upstream are about
narration duration vs video duration during a single run — not cross-project learning.

Upstream has excellent *within-run* quality control (the reviewer protocol, the
checkpoint protocol, `visual_qa`). It has no *across-run* memory.

That is Sporsho's job, and it is the single highest-value thing this layer does.

---

## The Rule

**Every completed project writes to memory. No exceptions.**

A project that produces a video and no memory is a project you will repeat.

---

## Files

| File | Records | Update when |
|---|---|---|
| [`INDEX.md`](INDEX.md) | One row per completed project | Every delivery |
| [`LESSONS.md`](LESSONS.md) | Patterns that worked and didn't | Every delivery |
| [`FAULTS.md`](FAULTS.md) | Tool/behaviour surprises | When something behaves unexpectedly |
| [`CLIENT-TASTE.md`](CLIENT-TASTE.md) | What each client actually likes | When you learn something new |

---

## The Entry Contract

Every project writes **exactly three things**:

```markdown
### {{project-id}} — {{date}}

**What we did:**   {{pipeline, register, client, duration}}
**What worked:**   {{specific, verifiable}}
**What didn't:**   {{specific, verifiable}}
**Surprise:**      {{anything that behaved differently than documented}}
**Next time:**     {{one concrete change}}
```

The **"Next time"** line is the load-bearing one. If it's vague ("do better"), it's useless.
It must be concrete enough to act on: *"Use `silence_cutter` before `video_trimmer` on
interview footage — manual trimming missed 40% of the dead air."*

---

## Reading Order

At session start, read `INDEX.md` and `LESSONS.md`.

Before starting work for a specific client, read `CLIENT-TASTE.md` for that client.

Before using a tool you haven't used recently, check `FAULTS.md` for it.

---

## Promoting To Rules

Memory **describes**; rules **prescribe**.

When the same lesson appears **three times**, it stops being a lesson and becomes a rule.
Promote it:

| Lesson is about… | Promote to |
|---|---|
| Cut/pacing/caption/audio behaviour | `SPORSHO/EDITING-RULES/` |
| One client's preference | `SPORSHO/CLIENTS/<client>/EDITING-RULES.md` |
| OpenMontage behaving unexpectedly | Report upstream (see `INTEGRATION.md`) |

Then mark the lesson in `LESSONS.md` as `→ promoted to <file>` so it isn't re-promoted.

---

## What Memory Is Not

- Not a log of every render. Only what you *learned*.
- Not a place for client footage or screenshots.
- Not a replacement for `REVISION-LOG.md` — that's per-client, this is cross-project.

---

## Honest Limitation

Nothing in this folder is enforced by code. It is a **contract**, and it only works
if it is followed. The mitigation is keeping entries short — a memory entry that takes
30 seconds to write gets written; one that takes 10 minutes does not.
