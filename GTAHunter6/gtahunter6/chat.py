"""Chat parsing: normalize Twitch / YouTube chat formats to a common message list."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Message:
    t: float                      # seconds from video start
    author: str
    text: str                     # message text with emotes removed
    emotes: list[str] = field(default_factory=list)


def _twitch_fragments(fragments, body: str) -> tuple[str, list[str]]:
    if not fragments:
        return body, []
    text_parts, emotes = [], []
    for f in fragments:
        is_emote = bool(f.get("emoticon") or f.get("emote"))
        txt = f.get("text") or ""
        (emotes if is_emote else text_parts).append(txt.strip() if is_emote else txt)
    return "".join(text_parts).strip(), [e for e in emotes if e]


def parse_twitchdownloader(data: dict) -> list[Message]:
    """TwitchDownloader chat JSON ({"comments": [...]}) or our own Twitch GQL dump."""
    out = []
    for c in data.get("comments", []):
        msg = c.get("message") or {}
        commenter = c.get("commenter") or {}
        author = commenter.get("_id") or commenter.get("display_name") or commenter.get("name") or "?"
        text, emotes = _twitch_fragments(msg.get("fragments"), msg.get("body") or "")
        out.append(Message(float(c["content_offset_seconds"]), str(author), text, emotes))
    return out


def parse_youtube_live_chat(lines) -> list[Message]:
    """yt-dlp live_chat.json: one JSON object per line."""
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        replay = obj.get("replayChatItemAction") or {}
        offset_ms = replay.get("videoOffsetTimeMsec")
        for action in replay.get("actions", []):
            item = (action.get("addChatItemAction") or {}).get("item") or {}
            r = item.get("liveChatTextMessageRenderer") or item.get("liveChatPaidMessageRenderer")
            if not r or offset_ms is None:
                continue
            text_parts, emotes = [], []
            for run in (r.get("message") or {}).get("runs", []):
                if "text" in run:
                    text_parts.append(run["text"])
                elif "emoji" in run:
                    sc = run["emoji"].get("shortcuts") or [run["emoji"].get("emojiId", "")]
                    emotes.append(sc[0].strip(":"))
            author = r.get("authorExternalChannelId") or (r.get("authorName") or {}).get("simpleText", "?")
            out.append(Message(int(offset_ms) / 1000.0, author, "".join(text_parts).strip(), emotes))
    return out


def load_chat(path: str | Path) -> list[Message]:
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    stripped = raw.lstrip()
    if stripped.startswith("{") and '"comments"' in raw[:5000]:
        msgs = parse_twitchdownloader(json.loads(raw))
    else:
        msgs = parse_youtube_live_chat(raw.splitlines())
    msgs = [m for m in msgs if m.t >= 0]
    msgs.sort(key=lambda m: m.t)
    if not msgs:
        raise ValueError(f"No chat messages parsed from {path}")
    return msgs
