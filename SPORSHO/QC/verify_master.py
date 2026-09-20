#!/usr/bin/env python3
"""verify_master.py — ground-truth verification of a joined master.

Usage: verify_master.py FILE [--expect-frames N]

Each measurement opens its own container handle: PyAV yields nothing if you demux and then decode
on the same handle, which is how a healthy file once measured as "0 frames" here. A `-c copy` join
of split footage can report a fine container duration while hiding a mid-stream frame-size change,
drifted audio and non-monotonic PTS, so the only honest check is: count packets, decode every
frame, collect the set of decoded geometries, test PTS monotonicity and compare audio sample count
against video frame count. Exit code 0 means all of that passed.
"""
import sys, json, os
import numpy as np, av

path = sys.argv[1]
want = int(sys.argv[sys.argv.index("--expect-frames") + 1]) if "--expect-frames" in sys.argv else None

def packets(stream_index):
    c = av.open(path); n = 0
    for p in c.demux(c.streams[stream_index]):
        if p.duration: n += 1
    c.close(); return n

def decode_video():
    c = av.open(path); st = c.streams.video[0]
    n = 0; t = []; sz = set(); tb = st.time_base
    for f in c.decode(st):
        n += 1; sz.add((f.width, f.height)); t.append(int(f.pts) if f.pts is not None else None)
    rate = float(st.average_rate or st.base_rate or 0); c.close()
    return n, sorted(f"{w}x{h}" for w, h in sz), t, tb, rate

def decode_audio():
    c = av.open(path)
    if not c.streams.audio:
        c.close(); return None
    st = c.streams.audio[0]; ns = 0
    for f in c.decode(st):
        ns += f.samples
    ar = int(st.rate); c.close(); return ns, ar

n, geo, pts, tb, rate = decode_video()
out = {"file": path, "video_packets": packets(0), "video_frames_decoded": n,
       "geometry": geo, "uniform_geometry": len(geo) == 1, "fps": round(rate, 6)}
d = np.diff(np.asarray(pts, dtype=np.float64)) * float(tb)
if d.size:
    out["pts_monotonic"] = bool((d > 0).all())
    out["frame_spacing_ms"] = [round(float(d.min()) * 1000, 4), round(float(d.max()) * 1000, 4)]
else:
    out["pts_monotonic"] = False; out["frame_spacing_ms"] = None
step = float(np.median(d)) if d.size else (1 / rate if rate else 1 / 30)
vid = (pts[-1] * float(tb) + step) if pts else 0.0
out["video_duration_s"] = round(vid, 4)
a = decode_audio()
if a:
    ns, ar = a
    out.update(audio_packets=packets(1), audio_samples=ns, audio_rate=ar,
               audio_duration_s=round(ns / ar, 4), av_delta_s=round(ns / ar - vid, 5))
c3 = av.open(path)
out["container"] = {"duration_s": round(float(c3.duration / av.time_base), 4) if c3.duration else None,
                    "size_bytes": os.path.getsize(path)}
c3.close()
if want is not None:
    out["frames_expected"] = want; out["frames_match"] = (n == want)
print(json.dumps(out, indent=2))

v = []
v.append("frames exact" if (want is None or out.get("frames_match")) else f"⚠ FRAME COUNT {n} != {want}")
v.append("geometry uniform" if out["uniform_geometry"] else "⚠ MIXED GEOMETRY mid-stream")
v.append("PTS monotonic" if out["pts_monotonic"] else "⚠ NON-MONOTONIC PTS")
sp = out.get("frame_spacing_ms")
v.append("spacing exact CFR" if sp and (sp[1] - sp[0]) < 1e-4 * 1000 else f"⚠ uneven spacing {sp}")
if "av_delta_s" in out:
    v.append(f"A/V locked ({out['av_delta_s']:+.5f}s)" if abs(out["av_delta_s"]) < 0.002 else f"⚠ A/V DRIFT {out['av_delta_s']:+.5f}s")
v.append("packets==decoded" if out["video_packets"] == n else f"⚠ packet/frame mismatch {out['video_packets']} vs {n}")
print("VERDICT: " + " · ".join(v))
json.dump(out, open(path + ".verify.json", "w"), indent=1)
bad = any(x.startswith("⚠") for x in v)
print("RESULT: " + ("FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
