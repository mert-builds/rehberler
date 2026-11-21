# GTAHunter6

Find the moments where a stream's chat explodes and cut vertical 9:16 clips that start
just **before** the explosion (chat always reacts late).

Works with **Twitch VODs** and **YouTube live replays** (chat replay must be enabled).

## How it works

1. **Chat** — downloads the full chat (Twitch: public GQL API, no login; YouTube: `yt-dlp` live_chat).
2. **Detect** — counts *unique chatters* per 15 s window and compares each window to the
   local norm (rolling median over ±5 min). Unique chatters, not raw messages, so one spammer
   can't fake a burst and a busy stream's constant chatter doesn't drown out real spikes.
   Picks the top N bursts at least 60 s apart.
3. **Onset** — finds the second the burst starts rising (5 s rate > 2× local norm).
4. **Clip window** — `start = onset − lead` (default 25 s), length 15 s.
5. **Title** — the phrase most distinct chatters typed during the burst (1–3 words,
   Turkish/English stopwords and emotes filtered), e.g. "Polis uçtu".
6. **Render** — downloads only the needed 15 s section (no full VOD download), renders
   1080×1920 blur-fit: full 16:9 frame centered over a blurred, darkened copy.

## Setup

```bash
git clone https://github.com/mert-builds/rehberler.git && cd rehberler/GTAHunter6
/opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
# needs ffmpeg + yt-dlp on PATH (brew install ffmpeg yt-dlp)
```

## Usage

```bash
# Twitch VOD
.venv/bin/python -m gtahunter6.cli https://www.twitch.tv/videos/2933861646

# YouTube live replay
.venv/bin/python -m gtahunter6.cli "https://www.youtube.com/watch?v=VIDEO_ID"

# Only find moments (fast, no video), check the chart first
.venv/bin/python -m gtahunter6.cli <url> --detect-only

# Local files (TwitchDownloader chat JSON or yt-dlp live_chat.json)
.venv/bin/python -m gtahunter6.cli --video stream.mp4 --chat chat.json
```

Options: `--top 10` clips, `--lead 25` seconds before burst, `--dur 15` clip length,
`--window 15` chat window, `--min-gap 60` seconds between bursts, `--out out`.

## Output

```
out/<platform>-<id>/
  clips/01-polis-uctu.mp4 ...   9:16 clips, ranked by burst strength
  clips.csv                     rank, title, times, chatter counts
  manifest.json                 same data; input for a future publish step
  chat-density.png              chatter curve, baseline, picked bursts (red)
  chat.json / *.live_chat.json  cached chat (re-runs skip the download)
```

## Notes

- Twitch chat paging uses time offsets (cursor paging is blocked by Twitch integrity checks).
  In extreme bursts the API may return a capped page per second; peaks still rank on top.
- Re-run with a different `--lead` (25–30) if events land too early/late in the clips.
- Publishing to YouTube Shorts / Instagram Reels is not built yet.

## Tests

```bash
.venv/bin/python -m pytest -q tests
```
