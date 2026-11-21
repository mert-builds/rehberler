"""Download chat and video sections for Twitch VODs and YouTube live replays."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

TWITCH_GQL = "https://gql.twitch.tv/gql"
TWITCH_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"   # public web client id (same as TwitchDownloader)


def platform_of(url: str) -> str:
    if re.search(r"twitch\.tv/videos/\d+", url):
        return "twitch"
    if re.search(r"(youtube\.com/(watch|live/)|youtu\.be/)", url):
        return "youtube"
    raise ValueError(f"Unsupported URL (need twitch.tv/videos/<id> or a YouTube video): {url}")


def video_info(url: str) -> dict:
    out = subprocess.run(["yt-dlp", "-J", "--no-warnings", url], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata failed:\n{out.stderr[-2000:]}")
    return json.loads(out.stdout)


# ---------------- Twitch chat ----------------

_COMMENTS_QUERY = (
    'query{video(id:"%s"){comments(contentOffsetSeconds:%d){edges{node{id contentOffsetSeconds '
    'commenter{id login displayName} message{fragments{text emote{emoteID}}}}} '
    'pageInfo{hasNextPage}}}}'
)


def _gql(query: str) -> dict:
    req = urllib.request.Request(
        TWITCH_GQL, data=json.dumps({"query": query}).encode(),
        headers={"Client-ID": TWITCH_CLIENT_ID, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    return {}


def download_twitch_chat(video_id: str, duration: float, dst: Path) -> Path:
    """Page through the VOD chat by time offset; writes TwitchDownloader-compatible JSON."""
    seen, comments = set(), []
    offset, last_print = 0, 0
    while offset <= duration:
        data = _gql(_COMMENTS_QUERY % (video_id, offset))
        video = (data.get("data") or {}).get("video")
        if video is None:
            raise RuntimeError(f"Twitch GQL returned no video for {video_id}: {str(data)[:500]}")
        edges = ((video.get("comments") or {}).get("edges")) or []
        max_off = offset
        for e in edges:
            n = e["node"]
            if n["id"] in seen:
                continue
            seen.add(n["id"])
            frags = [{"text": f.get("text") or "", "emoticon": f.get("emote")}
                     for f in (n.get("message") or {}).get("fragments", [])]
            who = n.get("commenter") or {}
            comments.append({
                "content_offset_seconds": n["contentOffsetSeconds"],
                "commenter": {"_id": who.get("id") or who.get("login") or "?",
                              "display_name": who.get("displayName")},
                "message": {"body": "".join(f["text"] for f in frags), "fragments": frags},
            })
            max_off = max(max_off, n["contentOffsetSeconds"])
        # Each page covers a time slice; step past it (at least 1 s) to make progress.
        offset = max(offset + 1, int(max_off) + (0 if max_off > offset else 1))
        if not edges:
            offset += 30
        if offset - last_print >= 600:
            print(f"  chat {offset / 60:.0f}/{duration / 60:.0f} min, {len(comments)} msgs", file=sys.stderr)
            last_print = offset
    comments.sort(key=lambda c: c["content_offset_seconds"])
    dst.write_text(json.dumps({"video": {"id": video_id}, "comments": comments}), encoding="utf-8")
    return dst


# ---------------- YouTube chat ----------------

def download_youtube_chat(url: str, workdir: Path) -> Path:
    out_tmpl = str(workdir / "chat.%(ext)s")
    subprocess.run(["yt-dlp", "--skip-download", "--write-subs", "--sub-langs", "live_chat",
                    "--no-warnings", "-o", out_tmpl, url], check=True)
    hits = list(workdir.glob("chat*.live_chat.json"))
    if not hits:
        raise RuntimeError("No live_chat replay found. Is this a past livestream with chat replay?")
    return hits[0]


# ---------------- video sections ----------------

def download_section(url: str, start: float, end: float, dst_stem: Path) -> Path:
    """Download only [start, end] of the remote video (exact cuts)."""
    tmpl = str(dst_stem) + ".%(ext)s"
    dst_stem.parent.mkdir(parents=True, exist_ok=True)
    # YouTube often 403s section downloads on the default client; fall back to others.
    clients = [None, "mweb", "web_safari"] if platform_of(url) == "youtube" else [None]
    last_err = ""
    for client in clients:
        for p in dst_stem.parent.glob(dst_stem.name + ".*"):
            p.unlink()
        cmd = ["yt-dlp", "--no-warnings", "-q",
               "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
               "--download-sections", f"*{start:.2f}-{end:.2f}", "--force-keyframes-at-cuts",
               "--merge-output-format", "mp4", "-o", tmpl]
        if client:
            cmd += ["--extractor-args", f"youtube:player_client={client}"]
        r = subprocess.run(cmd + [url], capture_output=True, text=True)
        hits = [p for p in dst_stem.parent.glob(dst_stem.name + ".*") if p.suffix in (".mp4", ".mkv", ".webm")]
        if r.returncode == 0 and hits:
            return hits[0]
        last_err = r.stderr[-800:]
        print(f"  section download failed (client={client or 'default'}), retrying", file=sys.stderr)
    raise RuntimeError(f"Section download failed for {start}-{end}:\n{last_err}")
