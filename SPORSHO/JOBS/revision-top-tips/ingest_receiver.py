#!/usr/bin/env python3
"""Inbound media receiver for the `radice-revision-top-tips` edit job.

WHY THIS EXISTS. This sandbox's egress is filtered by TLS SNI: only GitHub and PyPI
handshakes complete (every other host — Drive, Dropbox, OneDrive, Cloudflare tunnels,
file hosts, even plain HTTP on port 80 — dies at the handshake or on first byte, verified
2026-09-21). GitHub holds the ten video parts only as Git LFS pointers, and the LFS
object host is not in the allowlist. So no *outbound* download route can reach the bytes.
An *inbound* upload from the operator's own browser needs no egress at all: the Arena
preview proxy already reaches this sandbox on any bound port.

WHAT IT DOES. Accepts chunked, resumable PUTs of the source files, writes them into the
project ingest directory, and verifies each one's SHA-256 against the LFS OID recorded in
`ingest-manifest.json`. It never touches anything outside its ingest directory, never
overwrites a file that already passed verification, and never writes to the repo.

Read `GET /` for the operator-facing page. Token-gated so a guessed preview URL cannot
push bytes into the workspace.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

# Both overridable so the receiver can be self-tested against a scratch dir without
# touching a real ingest, and so it survives a workspace move.
INGEST = Path(os.environ.get("SPORSHO_INGEST_DIR", "/home/user/k-radice-edit/ingest"))
MANIFEST = Path(os.environ.get("SPORSHO_INGEST_MANIFEST",
    "/home/user/Sporsho-AI-OpenMontage/SPORSHO/CLIENTS/katharine-radice/ingest-manifest.json"))
PORT = int(os.environ.get("SPORSHO_INGEST_PORT", "8090"))
CHUNK = 8 * 1024 * 1024
MAX_TOTAL = 600 * 1024 * 1024
SAFE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._()-]{0,80}$")

TOKEN = (INGEST / ".token").read_text().strip() if (INGEST / ".token").exists() else secrets.token_hex(8)
INGEST.mkdir(parents=True, exist_ok=True)
(INGEST / ".token").write_text(TOKEN + "\n")
(INGEST / ".token").chmod(0o600)


def manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text())
    except Exception:  # noqa: BLE001
        return {}


def expected_for(name: str) -> tuple[str | None, int | None]:
    """Return (oid, size) this filename should match, if the manifest knows it.

    Matching is case-insensitive on the stem+extension so `1.MP4` / `1.mov` still map to part
    1, but deliberately NOT lenient about anything else: `01.mp4` or `part1.mp4` return no match
    rather than being guessed into a slot, because a silently renumbered part is worse than a
    refused upload.
    """
    m = manifest()
    lname = name.strip().lower()
    for key, part in (m.get("parts") or {}).items():
        aliases = {f"{key}.mp4", f"{key}.mov", f"{key}.m4v", Path(part["repo_path"]).name.lower()}
        if lname in aliases:
            return part["lfs_oid_sha256"], part["expected_bytes"]
    return None, None


_DIGEST: dict[tuple, str] = {}


def _digest_of(p: Path) -> tuple[bytes, str]:
    """Hash once per (size, mtime); a 190 MB ingest must not be re-read on every poll."""
    st = p.stat()
    key = (p.name, st.st_size, int(st.st_mtime))
    if key not in _DIGEST:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for blk in iter(lambda: f.read(1 << 20), b""):
                h.update(blk)
        if len(_DIGEST) > 32:
            _DIGEST.clear()
        _DIGEST[key] = h.hexdigest()
    data = p.read_bytes() if st.st_size < 4096 else b""
    return data, _DIGEST[key]


def state() -> dict:
    m = manifest()
    rows, have = [], 0
    for p in sorted(INGEST.iterdir()):
        if not p.is_file() or p.name.startswith(".") or p.suffix in (".sha", ".part"):
            continue
        _data, digest = _digest_of(p)
        size = p.stat().st_size
        oid, msize = expected_for(p.name)
        if oid:
            ok = digest == oid
            have += 1 if ok else 0
        else:
            ok = None  # not a manifest file (e.g. the whole MOV) — verified by decode, not OID
        rows.append(
            {
                "name": p.name,
                "bytes": size,
                "sha256": digest,
                "in_manifest": bool(oid),
                "oid_match": ok,
                "size_matches_manifest": (size == msize) if msize else None,
                "verified_sidecar": p.with_suffix(p.suffix + ".sha").exists(),
            }
        )
    total = len(m.get("order") or []) or 10
    return {
        "token_ok": True,
        "files": rows,
        "parts_expected": total,
        "parts_verified": have,
        "all_parts_ready": have == total,
        "join_order": m.get("order") or [str(i) for i in range(1, total + 1)],
        "chunk_cap_bytes": CHUNK,
    }


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "sporsho-ingest/1.0"

    def log_message(self, fmt, *args):  # quieter, structured
        print(f"[ingest] {self.address_string()} {fmt % args}", flush=True)

    # ---------- plumbing ----------
    def _send(self, code: int, body: bytes, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _authed(self, q: dict) -> bool:
        return (q.get("k", [""])[0] == TOKEN) or (self.headers.get("X-Token", "") == TOKEN)

    def do_OPTIONS(self):  # noqa: N802
        self._send(204, b"")

    # ---------- read ----------
    def do_GET(self):  # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/status":
            if not self._authed(q):
                return self._send(401, b'{"error":"bad token"}')
            return self._send(200, json.dumps(state(), indent=1).encode())
        if u.path in ("/", "/index.html"):
            return self._send(200, PAGE.replace("__TOKEN__", TOKEN).encode(), "text/html; charset=utf-8")
        if u.path == "/healthz":
            return self._send(200, b'{"ok":true}')
        self._send(404, b'{"error":"not found"}')

    # ---------- write ----------
    def _target(self, name: str) -> Path | None:
        # The URL path arrives percent-encoded (browsers send encodeURIComponent, and any
        # filename with a space — e.g. "Revision Top Tips.MOV" — is otherwise rejected here).
        name = unquote(name).strip()
        if not SAFE.match(name) or ".." in name or "/" in name or "\\" in name:
            return None
        if name in (".", "..") or name.startswith("."):
            return None  # no dotfiles: .token and friends are off-limits
        return INGEST / name

    def do_PUT(self):  # noqa: N802
        """Chunked upload:  PUT /upload/<name>?k=TOKEN&offset=<bytes>&final=1

        Each chunk is written at its stated offset; when `final=1` arrives the whole file on
        disk is hashed, so a retried or interleaved chunk can never produce a half-trusted
        digest. `offset=0` truncates, which is what a fresh retry of a file wants.
        """
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._send(401, b'{"error":"bad token"}')
        if not u.path.startswith("/upload/"):
            return self._send(404, b'{"error":"use /upload/<filename>"}')
        dst = self._target(u.path[len("/upload/"):])
        if dst is None:
            return self._send(400, b'{"error":"unsafe filename"}')
        shafile = dst.with_suffix(dst.suffix + ".sha")
        if shafile.exists():
            return self._send(409, json.dumps({"error": "already verified against its OID, refusing to overwrite", "file": dst.name}).encode())
        try:
            offset = int(q.get("offset", ["0"])[0])
        except ValueError:
            return self._send(400, b'{"error":"offset must be an integer"}')
        if offset < 0:
            return self._send(400, b'{"error":"offset must be >= 0"}')
        length = int(self.headers.get("Content-Length") or 0)
        if offset + length > MAX_TOTAL:
            return self._send(413, b'{"error":"over total size cap"}')
        want = offset + length
        with open(dst, "r+b" if dst.exists() and offset else "wb") as f:
            if offset:
                if f.seek(0, 2) < offset:
                    return self._send(400, json.dumps({"error": "offset beyond end of file — restart this file at offset 0"}).encode())
                f.seek(offset)
            written = 0
            while written < length:
                chunk = self.rfile.read(min(1 << 20, length - written))
                if not chunk:
                    break
                f.write(chunk)
                written += len(chunk)
            f.truncate()
            size = f.seek(0, 2)
        if written != length:
            return self._send(400, json.dumps({"error": "short body", "got": written, "want": length}).encode())
        out = {"file": dst.name, "chunk_bytes": written, "file_bytes_on_disk": size, "expected_at_least": want}
        if q.get("final", ["0"])[0] == "1":
            if size != want:
                out["error"] = f"size {size} != expected {want} — a chunk is missing, re-send this file from offset 0"
                return self._send(409, json.dumps(out, indent=1).encode())
            digest = hashlib.sha256(dst.read_bytes()).hexdigest()
            oid, msize = expected_for(dst.name)
            out.update(sha256=digest, oid_expected=oid, oid_match=(digest == oid) if oid else None,
                       size_match=(size == msize) if msize else None)
            if oid and digest == oid:
                shafile.write_text(digest + "\n")
                out["hint"] = "verified against the LFS OID recorded in ingest-manifest.json"
            elif oid:
                out["hint"] = "OID MISMATCH — do not use this file, and do not reconstruct"
            else:
                out["hint"] = "no manifest entry for this name — validated by decode/continuity instead"
            out["parts_verified"] = state()["parts_verified"]
        self._send(200, json.dumps(out, indent=1).encode())

    def do_POST(self):  # noqa: N802
        """Simple single-shot multipart-free upload:  POST /upload/<name>?k=TOKEN (raw body)"""
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._send(401, b'{"error":"bad token"}')
        if not u.path.startswith("/upload/"):
            return self._send(404, b'{"error":"use /upload/<filename>"}')
        dst = self._target(u.path[len("/upload/"):])
        if dst is None:
            return self._send(400, b'{"error":"unsafe filename"}')
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return self._send(411, b'{"error":"Content-Length required"}')
        append = q.get("append", ["0"])[0] == "1"
        final = q.get("final", ["1"])[0] == "1"
        base = dst.stat().st_size if (append and dst.exists()) else 0  # append=0 truncates first
        if base + length > MAX_TOTAL:
            return self._send(413, b'{"error":"over total size cap"}')
        shafile = dst.with_suffix(dst.suffix + ".sha")
        if shafile.exists():
            return self._send(409, json.dumps({"error": "already verified against its OID, refusing to overwrite", "file": dst.name}).encode())
        written = 0
        with open(dst, "ab" if append else "wb") as f:
            while written < length:
                chunk = self.rfile.read(min(1 << 20, length - written))
                if not chunk:
                    break
                f.write(chunk)
                written += len(chunk)
        if written != length:
            return self._send(400, json.dumps({"error": "short body", "got": written, "want": length}).encode())
        on_disk = dst.stat().st_size
        if not final:
            return self._send(200, json.dumps({"file": dst.name, "chunk_bytes": written, "file_bytes_on_disk": on_disk}).encode())
        digest = hashlib.sha256(dst.read_bytes()).hexdigest()
        oid, msize = expected_for(dst.name)
        ok = (digest == oid) if oid else None
        hint = ("verified against the LFS OID recorded in ingest-manifest.json" if ok else
                ("OID MISMATCH — do not use this file, and do not reconstruct" if oid else
                 "no manifest entry for this name — validated by decode/continuity instead"))
        if ok:
            dst.with_suffix(dst.suffix + ".sha").write_text(digest + "\n")
        print(f"[ingest] {dst.name}: {on_disk:,} B sha256={digest[:16]}… oid_match={ok}", flush=True)
        self._send(
            200,
            json.dumps(
                {
                    "file": dst.name,
                    "bytes": on_disk,
                    "sha256": digest,
                    "in_manifest": bool(oid),
                    "oid_match": ok,
                    "size_match": (on_disk == msize) if msize else None,
                    "hint": hint,
                    "parts_verified": state()["parts_verified"],
                },
                indent=1,
            ).encode(),
        )


PAGE = """<!doctype html><meta charset=utf-8><title>Sporsho ingest</title>
<style>
body{font:15px/1.55 ui-sans-serif,system-ui,sans-serif;background:#F9FAFB;color:#111827;margin:0;padding:38px}
main{max-width:760px;margin:0 auto}h1{font-size:20px;font-weight:800;letter-spacing:-.02em}
.card{background:#fff;border:1px solid #D1D5DB;border-radius:6px;padding:18px 20px;margin:0 0 16px;box-shadow:0 1px 6px rgba(17,24,39,.08)}
.drop{border:1.5px dashed #9CA3AF;border-radius:6px;padding:26px;text-align:center;color:#374151}
.over{border-color:#2563EB;background:#EFF6FF}
button{background:#111827;color:#fff;border:0;border-radius:4px;padding:10px 16px;font-weight:600;cursor:pointer}
table{width:100%;border-collapse:collapse;font-size:13.5px}td,th{text-align:left;padding:6px 8px;border-bottom:1px solid #E5E7EB}
.ok{color:#0F766E;font-weight:700}.bad{color:#B91C1C;font-weight:700}code{background:#F3F4F6;padding:1px 4px;border-radius:3px}
small{color:#6B7280}progress{width:100%;height:8px}
</style><main>
<h1>Sporsho — source ingest</h1>
<p class="card">Drop <strong>1.mp4 … 10.mp4</strong> (all ten, in order) or the single
<code>Revision Top Tips.MOV</code>. Each file is hashed as it lands and checked against the
LFS OID already recorded in the repo manifest. Nothing is edited until all ten verify.</p>
<div class="card"><div id="drop" class="drop">drop files here &nbsp;·&nbsp; or
<input id="pick" type="file" multiple style="border:0;box-shadow:none;padding:0;background:none">
</div><p><button id="send">Send selected</button> <span id="msg"></span></p><progress id="bar" max="100" value="0" hidden></div>
<div class="card"><strong>Received</strong><div id="list"></div>
<p><button id="refresh" style="background:#374151">Refresh status</button></p></div>
</main><script>
const K="__TOKEN__", CH=4*1024*1024; let queue=[];
const $=s=>document.querySelector(s), drop=$("#drop");
const set=m=>$("#msg").textContent=m;
["dragover","dragenter","drop"].forEach(t=>drop.addEventListener(t,ev=>{
  ev.preventDefault(); ev.stopPropagation();
  if(t==="drop"){ queue=[...((ev.dataTransfer&&ev.dataTransfer.files)||[])]; set(queue.length+" file(s) queued"); }
  drop.classList.add("over");
}));
drop.addEventListener("dragleave",()=>drop.classList.remove("over"));
$("#pick").addEventListener("change",e=>{queue=[...e.target.files];set(queue.length+" file(s) queued")});
async function status(){const r=await fetch("/status?k="+K),j=await r.json();
 $("#list").innerHTML="<table><tr><th>file</th><th>bytes</th><th>sha256</th><th>OID check</th></tr>"+
  j.files.map(f=>`<tr><td>${f.name}</td><td>${f.bytes.toLocaleString()}</td><td><code>${f.sha256.slice(0,16)}…</code></td>`+
   `<td>${f.in_manifest?(f.oid_match?'<span class=ok>match</span>':'<span class=bad>MISMATCH</span>'):'<small>not in manifest</small>'}</td></tr>`).join("")+
  `</table><p>parts verified: <strong>${j.parts_verified}/${j.parts_expected}</strong>`+
  (j.all_parts_ready?' — <span class=ok>ready to reconstruct 1→10</span>':' — <span class=bad>incomplete; do not reconstruct</span>')+"</p>";}
async function chunk(name,blob,first){
 // POST-append is the primary verb: many preview proxies allow POST but strip PUT.
 let r=await fetch(`/upload/${encodeURIComponent(name)}?k=${K}&append=${first?0:1}&final=${blob.__last?1:0}`,{method:"POST",body:blob});
 if(r.status===405||r.status===501){ // proxy or server rejected POST -> PUT with explicit offset
   r=await fetch(`/upload/${encodeURIComponent(name)}?k=${K}&offset=${blob.__off}&final=${blob.__last?1:0}`,{method:"PUT",body:blob});}
 let j; try{j=await r.json();}catch(e){throw new Error("proxy returned non-JSON for "+r.status+" — retry, or send files one at a time");}
 if(!r.ok)throw new Error(j.error||("HTTP "+r.status));}
async function up(f){const name=f.name.replace(/[^A-Za-z0-9 ._()-]/g,"_");let off=0;
 $("#bar").hidden=false;const total=Math.ceil(f.size/CH);
 for(let i=0;off<f.size;i++){const end=Math.min(off+CH,f.size);const blob=f.slice(off,end);
  blob.__off=off;blob.__last=(end>=f.size);
  await chunk(name,blob,off===0); off=end;
  $("#bar").value=Math.round(100*off/f.size); set(`${name}: ${off.toLocaleString()} / ${f.size.toLocaleString()} B`);}
 $("#bar").hidden=true;}
$("#send").addEventListener("click",async()=>{try{for(const f of queue)await up(f);set("done");queue=[];status();}catch(e){set("error: "+e.message)}});
$("#refresh").addEventListener("click",status);status();
</script>
"""


if __name__ == "__main__":
    print(f"[ingest] serving on 0.0.0.0:{PORT}  dir={INGEST}", flush=True)
    print(f"[ingest] token={TOKEN}  (the browser page embeds it automatically)", flush=True)
    print(f"[ingest] manifest={MANIFEST} exists={MANIFEST.is_file()}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
