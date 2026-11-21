"""ffmpeg rendering: 16:9 source -> 1080x1920 blur-fit vertical clip."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

BLUR_FIT = (
    "[0:v]split[a][b];"
    "[a]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,"
    "gblur=sigma=8,eq=brightness=-0.12,scale=1080:1920[bg];"
    "[b]scale=1080:-2[fg];"
    "[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]"
)


def probe_duration(path: str | Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def render_vertical(src: str | Path, dst: str | Path, start: float, length: float) -> None:
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{length:.3f}",
        "-filter_complex", BLUR_FIT, "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-movflags", "+faststart", str(dst),
    ]
    subprocess.run(cmd, check=True)
