# Loop smoke test — `wordfreq`

A small CLI built to exercise the Build → Explainer → Reviewer → Demo loop once, end to end.

1. **Build:** [`wordfreq.py`](wordfreq.py) plus behavior tests in [`test_wordfreq.py`](test_wordfreq.py).
2. **Explainer:** [`docs/explainers/2026-10-06-wordfreq.md`](docs/explainers/2026-10-06-wordfreq.md).
3. **Reviewer:** [`docs/review.md`](docs/review.md). A fresh subagent found 6 issues; 5 are fixed with regression tests.
4. **Demo:** [`docs/demos/2026-10-06-wordfreq/`](docs/demos/2026-10-06-wordfreq/). All scenarios pass.

What the loop caught that the first round of tests missed: ASCII-only tokenizing, a crash on invalid UTF-8 on stdin,
noisy broken-pipe errors, no support for `-` as stdin, and inconsistent apostrophe handling.
