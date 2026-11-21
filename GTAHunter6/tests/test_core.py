import json
import random

from gtahunter6.chat import Message, load_chat
from gtahunter6.detect import assign_clips, find_peaks
from gtahunter6.title import best_phrase, slugify


def synth_chat(duration=3600, bursts=(600, 1800, 3000), spam_at=2400, seed=1):
    rnd = random.Random(seed)
    msgs = []
    for t in range(duration):                       # background: ~1 msg/s from 200 users
        for _ in range(rnd.choice([0, 1, 1, 2])):
            msgs.append(Message(t + rnd.random(), f"u{rnd.randrange(200)}", "hello chat"))
    for b in bursts:                                # burst: 150 distinct users in ~10 s
        for i in range(150):
            msgs.append(Message(b + 4 + rnd.random() * 10, f"fan{b}_{i}", "polis uçtu KEKW"))
    for i in range(300):                            # one spammer, 300 msgs, should NOT win
        msgs.append(Message(spam_at + rnd.random() * 15, "spammer", "buy followers"))
    msgs.sort(key=lambda m: m.t)
    return msgs


def test_finds_bursts_and_ignores_spammer():
    msgs = synth_chat()
    peaks, _ = find_peaks(msgs, 3600, top=3)
    onsets = sorted(p.onset for p in peaks)
    for b, o in zip((600, 1800, 3000), onsets):
        assert b <= o <= b + 6, (b, o)
    assert all(abs(p.onset - 2400) > 60 for p in peaks)


def test_clip_window_lead_and_clamp():
    msgs = synth_chat()
    peaks, _ = find_peaks(msgs, 3600, top=3)
    assign_clips(peaks, 3600, lead=25, length=15)
    for p in peaks:
        assert abs(p.clip_start - (p.onset - 25)) < 1e-6
        assert abs(p.clip_end - p.clip_start - 15) < 1e-6
    p = peaks[0]
    p.onset = 10
    assign_clips([p], 3600, lead=25, length=15)
    assert p.clip_start == 0 and p.clip_end == 15


def test_title_picks_repeated_phrase():
    msgs = [Message(0, f"a{i}", "POLİS UÇTU KEKW") for i in range(20)]
    msgs += [Message(0, f"b{i}", "nasıl ya") for i in range(4)]
    assert best_phrase(msgs) == "Polis uçtu"
    assert slugify("Polis uçtu") == "polis-uctu"


def test_parsers(tmp_path):
    td = {"comments": [{"content_offset_seconds": 5.5, "commenter": {"_id": "1"},
                        "message": {"body": "gg Kappa", "fragments": [{"text": "gg ", "emoticon": None},
                                                                       {"text": "Kappa", "emoticon": {"emoticon_id": "25"}}]}}]}
    p = tmp_path / "td.json"
    p.write_text(json.dumps(td))
    m = load_chat(p)[0]
    assert (m.t, m.author, m.text, m.emotes) == (5.5, "1", "gg", ["Kappa"])

    yt = {"replayChatItemAction": {"videoOffsetTimeMsec": "12000", "actions": [{"addChatItemAction": {"item": {
        "liveChatTextMessageRenderer": {"message": {"runs": [{"text": "bu nasıl kaza "},
                                                             {"emoji": {"shortcuts": [":fire:"]}}]},
                                        "authorExternalChannelId": "UC1"}}}}]}}
    p2 = tmp_path / "x.live_chat.json"
    p2.write_text(json.dumps(yt) + "\n")
    m = load_chat(p2)[0]
    assert (m.t, m.author, m.text, m.emotes) == (12.0, "UC1", "bu nasıl kaza", ["fire"])


def test_title_filters_noise_and_keeps_english_i():
    msgs = [Message(0, f"a{i}", "BRICKED KEKW") for i in range(6)]
    msgs += [Message(0, f"b{i}", "bro 10 noooo") for i in range(12)]
    assert best_phrase(msgs) == "Bricked"
