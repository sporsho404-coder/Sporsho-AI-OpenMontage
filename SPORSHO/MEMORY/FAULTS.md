# Faults — Tool Behaviour Surprises

When a tool behaves differently than its skill file claims, record it here.

---

## Why This File Is High-Value

OpenMontage's own `AGENT_GUIDE.md` says this directly, in its section on reading source:

> *"When a skill and a tool disagree, or when something behaves differently than the
> skill claims, reading the tool source is fair game — that's often the only way to
> catch a silent-availability bug or a stale doc string."*

And it adds:

> *"If you do read source to debug, consider whether the finding belongs in a skill
> update afterward so the next agent doesn't need to repeat the dive."*

This file is the Sporsho version of that. Upstream can't hold it, because it's
specific to your environment, your providers, and your configured API keys.

---

## Entry Format

```markdown
### {{tool_name}} — {{YYYY-MM-DD}}

**Expected:**   {{what the skill/doc says}}
**Actual:**     {{what happened}}
**Cause:**      {{root cause, if found}}
**Workaround:** {{what to do instead}}
**Upstream?**   {{is this a genuine OpenMontage bug worth reporting? yes/no/investigate}}
**Seen again:** {{dates — after 3 occurrences, escalate}}
```

---

## Entries

_None recorded yet._

---

## Categories To Watch

These are the failure modes most likely to bite, based on how the system is built:

### 1. Silent provider unavailability
A tool exists in the registry but its API key is not configured. The tool appears
available but fails at call time. **Always check configuration before promising a
provider.** This is the most common false promise in generated plans.

### 2. Stale doc strings
A skill file describes parameters that have since changed in the tool. Compare the
skill against the tool's actual signature when something behaves oddly.

### 3. Beta pipeline rough edges
`talking-head`, `clip-factory`, `podcast-repurpose`, `character-animation`, and
`localization-dub` are marked **beta** upstream. Expect (and record) rough edges.

### 4. Cost estimate drift
`lib/delivery_promise.py` and the cost tracker exist to catch this. If actual spend
diverges from the estimate, record by how much and on which tool.

### 5. Render-time surprises
Remotion/HyperFrames renders can fail on specific composition constructs. Record the
construct, not just the error.

---

## Escalation

After a fault is seen **three times**, do one of:

- **If it's environmental** (your keys, your paths) → fix your setup, close the entry
- **If it's genuinely upstream** → consider a pull request to
  `calesthio/OpenMontage`. **Never** patch upstream files directly in this repo —
  see `SPORSHO/INTEGRATIONS/GITHUB.md` for why.
