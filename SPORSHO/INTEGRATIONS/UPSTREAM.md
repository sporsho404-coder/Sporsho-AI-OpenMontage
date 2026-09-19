# Integration — UPSTREAM (OpenMontage)

Staying current with OpenMontage without losing Sporsho knowledge.

---

## Why This Works

`SPORSHO/` sits at the repository root. Upstream's tree has no `SPORSHO/` directory.
Therefore **a merge can never conflict inside `SPORSHO/`.** That is the entire reason
this folder is named the way it is and placed where it is.

Keep that property. If a conflict ever appears in `SPORSHO/`, something has gone wrong
with how the layer is being maintained.

---

## The Update Ritual

```bash
git fetch upstream
git diff upstream/main --stat            # what changed?
git diff upstream/main -- lib/paths.py lib/pipeline_loader.py styles/playbook_loader.py
git merge upstream/main
```

### Why check those three files specifically

They are the Sporsho layer's load-bearing assumptions:

| File | Sporsho depends on |
|---|---|
| `lib/paths.py` | `OPENMONTAGE_PROJECTS_DIR` override |
| `lib/pipeline_loader.py` | `load_pipeline(..., defs_dir=)` |
| `styles/playbook_loader.py` | `styles/custom/` lookup |

If any changed, revisit `docs/sporsho/INTEGRATION.md` and update the relevant section.

---

## After Merging

```bash
# 1. Confirm the layer survived
ls SPORSHO/BRAIN SPORSHO/CLIENTS SPORSHO/MEMORY SPORSHO/QC

# 2. Confirm licence untouched
git diff upstream/main -- LICENSE        # must be empty

# 3. Check for playbook name collisions
python -c "
from styles.playbook_loader import list_playbooks
from collections import Counter
n = [p for p in list_playbooks()]
print('playbooks:', n)
"

# 4. Record the new base
git log -1 --format='%H %ad %s'
# → update OPENMONTAGE_VERSION in PROVENANCE.md
```

---

## When Upstream Breaks Something

Upstream moves fast (449 commits, many contributors). Occasionally a merge changes
behaviour your layer relies on.

1. **Record it** in `SPORSHO/MEMORY/FAULTS.md`
2. **Do not patch upstream files** in this repo — the next merge conflicts
3. **Work around it** in your calling code or in `SPORSHO/`
4. **Consider upstreaming a fix** as a pull request to `calesthio/OpenMontage`

Rule 3 is the important one. A local patch to an upstream file is a merge conflict
you have scheduled for later.

### If you must patch upstream

Sometimes there is no alternative. If so:

1. Do it on a **separate branch** (`sporsho-patches`), never on `main`
2. Record it in `PROVENANCE.md` under "Local modifications"
3. Re-check it after every merge
4. Open an upstream PR so you can eventually drop the patch

The goal is always zero local patches to upstream files.

---

## Version Pinning

`PROVENANCE.md` records the exact upstream commit this repository is based on.
After every merge, update it.

That gives you a clean answer to "which OpenMontage is this?" — and a rollback point
if an upstream change breaks your workflow.
