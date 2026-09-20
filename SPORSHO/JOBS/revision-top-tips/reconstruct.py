#!/usr/bin/env python3
"""Verify-then-join for the `Revision top tips` parts. Refuses to guess.

Usage:  python reconstruct.py <ingest_dir> <out_dir>
Refuses unless every part in the manifest's `order` is present AND its SHA-256 equals the
recorded LFS OID (or a `.sha` sidecar written by ingest_receiver says so). Never writes to
the source files, never joins a subset, never re-orders.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

MANIFEST = Path(os.environ.get("SPORSHO_INGEST_MANIFEST",
    "/home/user/Sporsho-AI-OpenMontage/SPORSHO/CLIENTS/katharine-radice/ingest-manifest.json"))


def die(msg: str) -> "NoReturn":  # noqa: ANN401
    print(f"REFUSING: {msg}")
    raise SystemExit(1)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    if out.returncode:
        die(f"ffprobe failed on {path.name}: {out.stderr[:200]}")
    return json.loads(out.stdout)


def main(ingest: Path, outdir: Path) -> None:
    man = json.loads(MANIFEST.read_text())
    order = man["order"]
    files: list[tuple[str, Path]] = []
    for key in order:
        cand = [ingest / f"{key}.mp4", ingest / f"{key}.mov", ingest / f"{key}.MOV"]
        found = next((c for c in cand if c.is_file()), None)
        if found is None:
            die(f"part {key} missing from {ingest} — do not reconstruct a subset")
        exp = man["parts"][key]["lfs_oid_sha256"]
        got = sha(found)
        if got != exp:
            die(f"part {key} sha256 {got[:16]}… != LFS OID {exp[:16]}… — this is not the original file")
        if found.stat().st_size != man["parts"][key]["expected_bytes"]:
            die(f"part {key} size {found.stat().st_size} != manifest {man['parts'][key]['expected_bytes']}")
        files.append((key, found))
        print(f"  part {key}: verified {found.stat().st_size:,} B")

    outdir.mkdir(parents=True, exist_ok=True)
    lst = outdir / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for _, p in files))
    joined = outdir / "revision-top-tips_full.mov"
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", "-movflags", "+faststart", "-y", str(joined)],
        capture_output=True, text=True,
    )
    if r.returncode:
        die(f"concat failed: {r.stderr[-400:]}")

    parts_meta = [probe(p) for _, p in files]
    full = probe(joined)
    v = next((s for s in full.get("streams", []) if s.get("codec_type") == "video"), None)
    if v is None:
        die("joined file has no video stream")
    sum_dur = sum(float(m["format"].get("duration", 0)) for m in parts_meta)
    dur = float(full["format"]["duration"])
    print(f"  joined: {dur:.3f} s  {v['width']}x{v['height']} @{v.get('avg_frame_rate')}  {full['format'].get('size')} B")
    print(f"  sum of part durations: {sum_dur:.3f} s  (delta {abs(sum_dur - dur):.3f} s)")
    if abs(sum_dur - dur) > 0.6:
        die(f"duration mismatch of {abs(sum_dur - dur):.3f} s — parts are not contiguous or timestamps were rewritten")
    dec = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(joined), "-f", "null", "-"], capture_output=True, text=True
    )
    if dec.stderr.strip():
        print("  decode warnings:\n" + dec.stderr.strip()[:600])
        die("decode errors present — not deliverable")
    print(f"  decode clean, {len(files)}/{len(order)} contiguous → reconstruction verified. Do NOT edit until a transcript exists.")
    (outdir / "reconstruction.json").write_text(json.dumps({
        "parts": [{"key": k, "path": str(p), "sha256": sha(p), "bytes": p.stat().st_size} for k, p in files],
        "joined": str(joined), "duration_seconds": dur, "sum_part_seconds": sum_dur,
        "width": v["width"], "height": v["height"], "fps": v.get("avg_frame_rate"),
        "decode_errors": 0, "verified_against_lfs_oid": True,
    }, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        die("usage: reconstruct.py <ingest_dir> <out_dir>")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
