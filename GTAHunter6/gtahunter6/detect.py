"""Find chat bursts and turn them into clip windows."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from .chat import Message


@dataclass
class Peak:
    window_start: int     # start second of the densest 15 s window
    onset: float          # second where the burst starts rising
    messages: int         # messages in the 15 s window
    authors: int          # unique authors in the 15 s window
    baseline: float       # typical unique authors per 15 s around this point
    score: float
    clip_start: float = 0.0
    clip_end: float = 0.0


def per_second(msgs: list[Message], duration: int):
    counts = np.zeros(duration, dtype=np.int32)
    authors_at = defaultdict(list)
    for m in msgs:
        s = int(m.t)
        if 0 <= s < duration:
            counts[s] += 1
            authors_at[s].append(m.author)
    return counts, authors_at


def unique_authors_rolling(authors_at, duration: int, window: int) -> np.ndarray:
    """U[t] = distinct authors in [t, t+window). Incremental sliding multiset."""
    live: dict[str, int] = defaultdict(int)
    out = np.zeros(duration, dtype=np.int32)
    for s in range(min(window, duration)):
        for a in authors_at.get(s, ()):
            live[a] += 1
    for t in range(duration):
        out[t] = len(live)
        for a in authors_at.get(t, ()):           # drop second t
            live[a] -= 1
            if live[a] == 0:
                del live[a]
        nxt = t + window                           # add second t+window
        for a in authors_at.get(nxt, ()):
            live[a] += 1
    return out


def rolling_sum(x: np.ndarray, window: int) -> np.ndarray:
    c = np.concatenate([[0], np.cumsum(x)])
    end = np.minimum(np.arange(len(x)) + window, len(x))
    return c[end] - c[np.arange(len(x))]


def local_baseline(x: np.ndarray, half: int = 300, step: int = 10) -> np.ndarray:
    """Rolling median over +-half seconds, sampled every `step` s and interpolated."""
    n = len(x)
    idx = np.arange(0, n, step)
    med = np.array([np.median(x[max(0, i - half): i + half + 1]) for i in idx], dtype=float)
    return np.interp(np.arange(n), idx, med)


def find_peaks(msgs: list[Message], duration: float, top: int = 10, window: int = 15,
               min_gap: int = 60, onset_k: float = 2.0) -> tuple[list[Peak], dict]:
    dur = int(np.ceil(duration)) + 1
    counts, authors_at = per_second(msgs, dur)
    S = rolling_sum(counts, window)
    U = unique_authors_rolling(authors_at, dur, window)
    B = local_baseline(U)
    # Poisson-style surprise: how far above the local norm, in noise units.
    score = (U - B) / np.sqrt(B + 1.0)

    order = np.argsort(-score, kind="stable")
    chosen: list[int] = []
    for t in order:
        if score[t] <= 0 or len(chosen) >= top:
            break
        if all(abs(int(t) - c) >= min_gap for c in chosen):
            chosen.append(int(t))

    # Onset: first second (looking back up to 10 s) where the 5 s message rate
    # clearly exceeds the local per-5s norm.
    R5 = rolling_sum(counts, 5)
    msg_base = local_baseline(S)
    peaks = []
    for t in chosen:
        thr = onset_k * msg_base[t] / window * 5 + 1
        onset = float(t)
        for s in range(max(0, t - 10), min(dur, t + window)):
            if R5[s] >= thr:
                onset = float(s)
                break
        peaks.append(Peak(t, onset, int(S[t]), int(U[t]), float(B[t]), float(score[t])))
    series = {"counts": counts, "S": S, "U": U, "B": B, "score": score}
    return peaks, series


def assign_clips(peaks: list[Peak], duration: float, lead: float = 25.0, length: float = 15.0) -> None:
    for p in peaks:
        start = max(0.0, p.onset - lead)
        start = min(start, max(0.0, duration - length))
        p.clip_start = round(start, 2)
        p.clip_end = round(min(duration, start + length), 2)
