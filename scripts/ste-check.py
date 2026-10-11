"""Check prose against about 80% of ASD-STE100: short sentences and active voice.

A file passes when at least 80% of its sentences have 20 words or fewer and no sentence has more than 30.
Passive voice is listed but doesn't fail the check, because the pattern match is rough.
Skips front matter, headings, code and Mermaid blocks, images, and HTML scripts, styles and SVG.
Use - to read stdin, e.g. `gh pr view 9 --json body -q .body | python3 ste-check.py -`.
Usage: python3 ste-check.py <file.md | file.html | -> [...]
"""
from __future__ import annotations

import html
import re
import sys

MAX_WORDS, MIN_SHARE, HARD_CAP = 20, 0.8, 30
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+(?:ed|en))\b", re.I)
NOT_PARTICIPLES = {"open", "often", "even", "seven", "eleven", "when", "then", "ten", "token", "between",
                   "listen", "women", "children"}
WORD = re.compile(r"[A-Za-z0-9](?:[\w'’%-]|\.(?=\w))*")


def prose(text: str, is_html: bool) -> str:
    if is_html:
        text = re.sub(r"<(script|style|pre|code|svg)\b[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<br\s*/?>|</(?:p|li|h\d|div|td|th|tr|caption|figcaption|summary|button|label)>",
                      "\n\n", text, flags=re.I)
        return html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```|<!--.*?-->", "\n\n", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", "code", text)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            lines.append("")
        elif stripped.startswith("|"):
            lines.extend(cell for c in stripped.strip("|").split("|") for cell in ("", c, ""))
        else:
            lines.append(line)
    return "\n".join(lines)


def sentences(text: str) -> list[tuple[int, str]]:
    text = re.sub(r"\b(e\.g|i\.e|vs|etc|cf)\.", lambda m: m.group(1).replace(".", ""), text, flags=re.I)
    out = []
    for block in re.split(r"\n\s*\n|\n\s*(?:[-*+]|\d+\.)\s+", text):
        for sentence in re.split(r"(?<=[.!?])\s+", " ".join(block.split())):
            words = WORD.findall(sentence)
            if len(words) >= 3:
                out.append((len(words), sentence))
    return out


def passive(sentence: str) -> str | None:
    for m in PASSIVE.finditer(sentence):
        if m.group(1).lower() not in NOT_PARTICIPLES:
            return m.group(0)
    return None


def check(name: str, text: str) -> bool:
    found = sentences(prose(text, name.lower().endswith((".html", ".htm"))))
    if not found:
        print(f"PASS {name}: no prose found")
        return True
    share = sum(n <= MAX_WORDS for n, _ in found) / len(found)
    longest = max(n for n, _ in found)
    flagged = [(p, s) for _, s in found if (p := passive(s))]
    ok = share >= MIN_SHARE and longest <= HARD_CAP
    print(f"{'PASS' if ok else 'FAIL'} {name}: {len(found)} sentences, {share:.0%} at {MAX_WORDS} words or "
          f"fewer (need {MIN_SHARE:.0%}), longest {longest} (max {HARD_CAP}), {len(flagged)} possibly passive")
    for n, s in found:
        if n > MAX_WORDS:
            print(f"  long [{n}] {s[:200]}")
    for p, s in flagged:
        print(f"  passive? [{p}] {s[:200]}")
    return ok


if len(sys.argv) < 2:
    sys.exit(__doc__.strip().splitlines()[-1])
results = [check("stdin", sys.stdin.read()) if path == "-" else check(path, open(path, encoding="utf-8").read())
           for path in sys.argv[1:]]
sys.exit(0 if all(results) else 1)
