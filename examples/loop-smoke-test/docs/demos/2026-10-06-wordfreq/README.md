# Demo — `wordfreq`

**Result: pass.** Captured in [`transcript.txt`](transcript.txt) (run from `examples/loop-smoke-test/`).

| # | Scenario | Expected | Observed |
|---|---|---|---|
| 1 | Real file (`AGENTS.md`), `-n 8` | Top 8, count desc, ties alphabetical | ✅ `the 18 … knowledge 5` |
| 2 | Unicode + curly/straight apostrophes | `café`, `naïve`, `don’t`, `rock'n'roll` intact | ✅ |
| 3 | Invalid UTF-8 on stdin | No crash; counts valid words | ✅ `bad`, `ok`, exit 0 |
| 4 | File + `-` (stdin) mixed | Counts combined | ✅ `notes 3` (1 from file + 2 from stdin) |
| 5 | Output piped to `head` | No `BrokenPipeError` noise | ✅ clean, exit 0 |
| 6 | Missing file | Clean error, exit 1 | ✅ |
| 7 | `-n 0` | Usage error, exit 2 | ✅ |
| 8 | Test suite | 10/10 pass | ✅ |

Reproduce: `cd examples/loop-smoke-test && python3 -m unittest -v test_wordfreq`, then run the
commands in `transcript.txt`.
