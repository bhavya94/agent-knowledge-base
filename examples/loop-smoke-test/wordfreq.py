"""Print the N most frequent words in text from files or stdin ("-" means stdin)."""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from collections import Counter
from typing import Iterable, Iterator

# Unicode letters/digits, joined by internal straight or curly apostrophes (don't, rock'n'roll).
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*")


def top_words(lines: Iterable[str], n: int) -> list[tuple[str, int]]:
    """Return the n most common words, ties broken alphabetically."""
    counts = Counter(w for line in lines for w in WORD_RE.findall(line.casefold()))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def read_lines(paths: list[str]) -> Iterator[str]:
    """Yield lines from each path (stdin for "-" or no paths), decoding as UTF-8 leniently."""
    for path in paths or ["-"]:
        if path == "-":
            yield from io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
        else:
            with open(path, encoding="utf-8", errors="replace") as f:
                yield from f


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help='input files (default: stdin; "-" for stdin)')
    parser.add_argument("-n", type=int, default=10, help="number of words (default: 10)")
    args = parser.parse_args(argv)
    if args.n < 1:
        parser.error("-n must be >= 1")

    try:
        result = top_words(read_lines(args.files), args.n)
    except OSError as e:
        print(f"wordfreq: {e.filename}: {e.strerror}", file=sys.stderr)
        return 1

    try:
        for word, count in result:
            print(f"{count:>6}  {word}")
        sys.stdout.flush()
    except BrokenPipeError:
        # Reader closed early (e.g. `| head`); exit quietly like standard Unix tools.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 0


if __name__ == "__main__":
    sys.exit(main())
