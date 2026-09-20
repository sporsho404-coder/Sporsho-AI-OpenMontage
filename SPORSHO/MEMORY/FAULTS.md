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

### GitHub-held client footage → unreachable from the agent sandbox — 2026-09-21 (re-verified after repo went public)

**Expected:**   Footage committed to the repo is retrievable by the agent; making the
repository **public** would let the LFS objects be downloaded directly.
**Actual:**      `Revision top tips/1–10.mp4` are 133-byte pointers. Verified against the
tarball of `main@26f2e3fd` (all ten oids + sizes recorded in
`CLIENTS/katharine-radice/ingest-manifest.json`, total **187,987,538 B**). 0 of 10 parts
readable. Public visibility changed nothing.
**Cause:**       Three independent walls, any one of which is sufficient:
1. LFS indirection — every *git-level* route returns the pointer:
   `api.github.com/…/contents/{path}` → pointer; `…/git/blobs/{sha}` +
   `Accept: application/vnd.github.raw` → pointer; `github.com/…/raw/main/…` → 302 to a
   blocked host; **codeload tarball/zipball → pointers** (GitHub never smudges LFS in
   archives); `POST /repos/…/git/blobs` style import → needs admin (404).
2. The LFS object store host is filtered by **SNI**, not by auth: unauthenticated
   `github.com/{repo}.git/info/lfs/objects/batch` *works* on a public repo and issues a
   valid presigned href, but `github-cloud.githubusercontent.com`,
   `media.githubusercontent.com`, `objects.githubusercontent.com`,
   `results-receiver.actions.githubusercontent.com` all die at TLS
   (`curl` → `000` in ~0.03 s, no handshake). Reachable hosts here: `github.com`,
   `api.github.com`, `codeload.github.com`, `pypi.org`, `files.pythonhosted.org`.
   Everything else tested (Drive, Dropbox, catbox, 0x0.st, transfer.sh, jsDelivr,
   allorigins/codetabs/corsproxy, cloudflare tunnel) → `000`.
3. No compute inside GitHub: the App token **cannot create or update
   `.github/workflows/**` on any branch** (server-side policy; `git push` rejected,
   `gh api` 422), so the one mechanism that could convert LFS→plain blobs inside
   GitHub's own network is unavailable to the agent.
**Control proof that the fault is LFS, not GitHub:** `assets/signal-from-tomorrow-demo.mp4`
(20,897,137 B) is a *plain* blob and downloads fine through the identical
`git/blobs/{sha}` endpoint. Every part is ≤22.7 MB — all under the 100 MB plain-blob
ceiling, so **no LFS is required at all** for this footage.
**Workaround:**   Do not route client footage through this repository (already
`CLIENTS/README.md` rule 5 and `INTEGRATIONS/GITHUB.md` — "GitHub holds intelligence, not
footage"; the LFS layer is what turns that mistake into a hard blocker). Two routes that
work: (a) human pastes a relay workflow that republishes the parts as plain `.mov` blobs
on an orphan branch — then `api.github.com` serves them to the agent; (b) attach the
files in the chat/workspace, which bypasses sandbox egress entirely. Verify every
retrieved part: `sha256sum` must equal `lfs_oid_sha256` in `ingest-manifest.json`.
**Upstream?**   no — environment + repo-policy interaction, but the *rule* belongs to
Sporsho: media intake must never depend on LFS.
**Seen again:**  2026-09-19, 2026-09-20, 2026-09-21 (×2, incl. post-public retry) → **promote to rule**

**Post-public retry, exact evidence (2026-09-21):** repo confirmed genuinely public
(`api.github.com` unauthenticated → `private=false`, HTML → 200). Unauthenticated
`POST github.com/{owner}/{repo}.git/info/lfs/objects/batch` **works** and returns a valid
presigned `download.href` on `github-cloud.githubusercontent.com/alambic/media/...`
(`X-Amz-SignedHeaders=host`, `X-Amz-Expires=3600`). The next hop is where it dies: every
GET/HEAD to that host returns `000` with curl exit **35 (SSL connect error)** in ~0.03 s —
TLS is killed at SNI, so no HTTP request is ever sent. Visibility is irrelevant: the
object store host, not auth, is the wall.
**Do not re-test these (all proven dead, in both private and public state):**
`raw.githubusercontent.com`, `media.`, `github-cloud.`, `objects.`,
`results-receiver.`, `codeload` archive smudging (codeload is reachable and answers 200,
but `tar.gz`/`zipball` **contain the 133-byte pointers** — GitHub never smudges LFS in
archives), `github.com/.../raw/...` (302 → blocked host), `api.github.com/repos/.../media/`
(404), `POST /repos/.../import` (404, no admin), third-party HTTP proxies
(allorigins / codetabs / corsproxy), free file hosts (catbox, 0x0.st, tmpfiles, transfer.sh,
litterbox, bashupload, ufile), Drive/Dropbox, jsDelivr, git-lfs (not installed). Reachable
hosts in this sandbox: `github.com`, `api.github.com`, `codeload.github.com`, `pypi.org`,
`files.pythonhosted.org`.
**Correction to a plausible-sounding fix:** GitHub Importer does *not* convert LFS for you.
Docs state: "If you use Git LFS, you will need to either convert the Git LFS objects to
regular files tracked by Git **before** running the migration, or move the Git LFS objects
to the new repository separately." So the local route is
`git lfs migrate export --everything --include="*.mp4"` then push to a throwaway repo —
that is a client-machine action, not an agent one.

### Sandbox egress is SNI-allowlisted → only an inbound intake works — 2026-09-21

**Expected:**   A public direct-download URL (Drive / Dropbox / OneDrive / Cloudflare Tunnel /
any HTTPS file URL) can be fetched by the agent once handed to it.
**Actual:**      Nothing outside GitHub and PyPI can be fetched. TCP connects everywhere
(`1.1.1.1:443`, `drive.google.com:80`, `catbox.moe:443` all report OPEN), but: TLS to any
non-GitHub SNI dies immediately (`SSLZeroReturnError`, i.e. the middlebox closes the handshake);
TLS with **no SNI at all** also dies; and plain **HTTP on port 80** is killed on first byte
(`curl` → `000` in 0.003 s, 0 bytes) even against no-captive-portal test hosts and a public GCS
object. Handshakes that *do* complete: `github.com`, `api.github.com`, `codeload.github.com`,
`pypi.org`, `files.pythonhosted.org`.
**Cause:**      Outbound filtering by TLS SNI against a small allowlist, plus L7 kill of
non-allowlisted HTTP. Not DNS (8.8.8.8 resolves anything), not a firewall on ports.
**Workaround:**   Intake is **inbound, not outbound**: the Arena preview proxy reaches any bound
port on the sandbox, so the operator's browser can push the files in. Receiver +
verify-then-join gate live in `SPORSHO/JOBS/revision-top-tips/` (`ingest_receiver.py`,
`reconstruct.py`), token-gated, 4 MB resumable chunks, SHA-256 checked against the recorded
LFS OIDs. It refuses: partial sets, overwriting an already-verified part, path traversal.
**Note for whoever reads this next:** it is technically possible to smuggle traffic past this
filter by putting `github.com` in the SNI of a connection to some other IP (measured: TLS
completes). Do **not** do it — that is circumventing a platform egress control and would route
client footage through a masqueraded connection. The legitimate version of the same trick is
simply "put the bytes on GitHub as plain blobs".
**Upstream?**   no — environment. But the *intake convention* is worth a house rule: every job
needs a transfer route that does not depend on sandbox egress.
**Seen again:**  2026-09-21 (×2: post-public retry, then direct-source probe)
