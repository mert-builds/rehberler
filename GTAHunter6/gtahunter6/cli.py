"""GTAHunter6: find chat explosions in a stream and cut 9:16 clips from just before them."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from . import fetch
from .chat import load_chat
from .detect import assign_clips, find_peaks
from .render import probe_duration, render_vertical
from .title import best_phrase, slugify


def fmt(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"


def plot_density(series, peaks, duration, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    U, B = series["U"], series["B"]
    x = np.arange(len(U)) / 60
    fig, ax = plt.subplots(figsize=(14, 4), dpi=110)
    ax.plot(x, U, lw=0.6, color="#4a6fa5", label="unique chatters / 15 s")
    ax.plot(x, B, lw=1, color="#999", label="local baseline")
    for i, p in enumerate(peaks, 1):
        ax.axvline(p.onset / 60, color="#e4572e", lw=0.8)
        ax.axvspan(p.clip_start / 60, p.clip_end / 60, color="#e4572e", alpha=0.25)
        ax.text(p.onset / 60, U.max() * 0.97, str(i), color="#e4572e", fontsize=8, ha="center")
    ax.set_xlabel("minutes")
    ax.set_xlim(0, duration / 60)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="GTAHunter6", description=__doc__)
    ap.add_argument("url", nargs="?", help="Twitch VOD or YouTube live replay URL")
    ap.add_argument("--video", help="local video file (instead of downloading)")
    ap.add_argument("--chat", help="local chat file: TwitchDownloader JSON or yt-dlp live_chat.json")
    ap.add_argument("--top", type=int, default=10, help="number of clips (default 10)")
    ap.add_argument("--lead", type=float, default=25.0, help="seconds before the chat burst to start (default 25)")
    ap.add_argument("--dur", type=float, default=15.0, help="clip length in seconds (default 15)")
    ap.add_argument("--window", type=int, default=15, help="chat window in seconds (default 15)")
    ap.add_argument("--min-gap", type=int, default=60, help="min seconds between bursts (default 60)")
    ap.add_argument("--out", default="out", help="output root (default ./out)")
    ap.add_argument("--detect-only", action="store_true", help="find moments, do not cut video")
    a = ap.parse_args(argv)

    if not a.url and not (a.chat and (a.video or a.detect_only)):
        ap.error("give a URL, or --chat plus --video (or --detect-only)")

    platform, info = None, {}
    if a.url:
        platform = fetch.platform_of(a.url)
        print(f"[1/4] metadata ({platform})", file=sys.stderr)
        info = fetch.video_info(a.url)
        stream_id = f"{platform}-{info['id']}"
    else:
        stream_id = Path(a.video or a.chat).stem
    workdir = Path(a.out) / slugify(stream_id, 80)
    workdir.mkdir(parents=True, exist_ok=True)

    duration = probe_duration(a.video) if a.video else float(info.get("duration") or 0)

    if a.chat:
        chat_path = Path(a.chat)
    elif platform == "twitch":
        print("[2/4] downloading Twitch chat", file=sys.stderr)
        chat_path = workdir / "chat.json"
        if not chat_path.exists():
            fetch.download_twitch_chat(str(info["id"]).lstrip("v"), duration, chat_path)
    else:
        print("[2/4] downloading YouTube chat replay", file=sys.stderr)
        existing = list(workdir.glob("chat*.live_chat.json"))
        chat_path = existing[0] if existing else fetch.download_youtube_chat(a.url, workdir)

    msgs = load_chat(chat_path)
    if not duration:
        duration = msgs[-1].t + a.dur
    print(f"[3/4] {len(msgs)} chat messages over {fmt(duration)}; detecting bursts", file=sys.stderr)

    peaks, series = find_peaks(msgs, duration, top=a.top, window=a.window, min_gap=a.min_gap)
    assign_clips(peaks, duration, lead=a.lead, length=a.dur)
    peaks.sort(key=lambda p: -p.score)

    rows = []
    for rank, p in enumerate(peaks, 1):
        burst = [m for m in msgs if p.onset <= m.t < p.onset + a.window]
        title = best_phrase(burst)
        fname = f"{rank:02d}-{slugify(title)}.mp4"
        rows.append({
            "rank": rank, "title": title, "file": fname,
            "clip_start": p.clip_start, "clip_end": p.clip_end,
            "clip_start_hms": fmt(p.clip_start), "burst_onset_hms": fmt(p.onset),
            "burst_onset": p.onset, "messages_15s": p.messages, "unique_chatters_15s": p.authors,
            "baseline_chatters_15s": round(p.baseline, 1), "score": round(p.score, 2),
            "source_url": a.url or str(a.video),
        })
        print(f"  #{rank:<2} {fmt(p.onset)}  {p.authors:>4} chatters (base {p.baseline:.0f})  "
              f"clip {fmt(p.clip_start)}  \"{title}\"", file=sys.stderr)

    plot_density(series, peaks, duration, workdir / "chat-density.png")
    with open(workdir / "clips.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["rank"])
        w.writeheader()
        w.writerows(rows)

    if not a.detect_only:
        print(f"[4/4] rendering {len(rows)} clips -> {workdir}", file=sys.stderr)
        clips_dir = workdir / "clips"
        clips_dir.mkdir(exist_ok=True)
        for r in rows:
            dst = clips_dir / r["file"]
            if a.video:
                render_vertical(a.video, dst, r["clip_start"], a.dur)
            else:
                part = fetch.download_section(a.url, r["clip_start"], r["clip_end"],
                                              workdir / "parts" / f"{r['rank']:02d}")
                render_vertical(part, dst, 0.0, a.dur)
            print(f"  wrote {dst}", file=sys.stderr)

    manifest = {"source": a.url or str(a.video), "platform": platform, "duration": duration,
                "settings": {"top": a.top, "lead": a.lead, "dur": a.dur, "window": a.window},
                "clips": rows}
    (workdir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"done: {workdir}/manifest.json", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
