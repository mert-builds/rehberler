"""Name a clip after the phrase chat repeated most during the burst."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict

from .chat import Message

STOPWORDS = set("""
a an the and or but is are was were be been to of in on at for with it this that i you he she we they
me my your so no yes not just like lol what why how who im its dont do does did can will
ve ile de da ki bu şu o ben sen biz siz onlar mi mı mu mü ne niye neden nasıl çok daha en bir
için gibi ama ya ki da de var yok olan oldu olur şey abi kanka aga ya ha he hee
""".split())

# Reaction filler: real chat noise, never a good clip name on its own.
FILLER = set("""
bro bruh lol lmao lmfao omg wtf gg yo yoo ok okay oh ah no yes yeah nah w l ww ll dude man guys chat
hahaha haha ahah xd mk aynen of off ya yaa vay oha lan amk
""".split())

# Common third-party emote names that arrive as plain text (BTTV/7TV/FFZ).
COMMON_EMOTES = {e.lower() for e in """
KEKW LUL LULW OMEGALUL Pog PogChamp POGGERS PogU Kappa monkaS monkaW Sadge PepeHands PepeLaugh
pepeLaugh catJAM Clap EZ xdd xd WICKED Aware Copium COPIUM Stare ICANT Kreygasm 4Head LMAO LMFAO
""".split()}

WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


TR_CHARS = set("ğüşöçıİĞÜŞÖÇ")
ELONGATION_RE = re.compile(r"(.)\1{2,}")


def tr_lower(s: str) -> str:
    """Lowercase; dotless-I mapping only when the text looks Turkish (keeps 'BRICKED' -> 'bricked')."""
    if TR_CHARS & set(s):
        s = s.replace("I", "ı").replace("İ", "i")
    return s.lower()


def tokens(text: str) -> list[str]:
    out = []
    for w in WORD_RE.findall(tr_lower(text)):
        w = ELONGATION_RE.sub(r"\1", w)            # "noooo" -> "no", "meee" -> "me"
        if len(w) > 2 and not w.isdigit() and w not in COMMON_EMOTES:
            out.append(w)
    return out


def ngrams(toks: list[str], n: int):
    for i in range(len(toks) - n + 1):
        g = toks[i:i + n]
        if g[0] in STOPWORDS or g[-1] in STOPWORDS:
            continue
        if all(w in FILLER for w in g):
            continue
        if len(set(g)) < n:           # "gol gol gol"
            continue
        yield " ".join(g)


def best_phrase(msgs: list[Message], min_authors: int = 3) -> str:
    authors_by_gram: dict[str, set] = defaultdict(set)
    emote_counter: Counter = Counter()
    for m in msgs:
        toks = tokens(m.text)
        for n in (1, 2, 3):
            for g in set(ngrams(toks, n)):
                authors_by_gram[g].add(m.author)
        for e in set(m.emotes) | {w for w in WORD_RE.findall(m.text) if w.lower() in COMMON_EMOTES}:
            emote_counter[e] += 1
    best, best_score = None, 0.0
    for g, authors in authors_by_gram.items():
        if len(authors) < min_authors:
            continue
        n = g.count(" ") + 1
        s = len(authors) * (1 + 0.35 * (n - 1))
        if s > best_score:
            best, best_score = g, s
    if best:
        return best[:1].upper() + best[1:]
    if emote_counter:
        return emote_counter.most_common(1)[0][0]
    return "Clip"


def slugify(s: str, maxlen: int = 40) -> str:
    s = unicodedata.normalize("NFKD", tr_lower(s).replace("ı", "i"))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:maxlen].rstrip("-")) or "clip"
