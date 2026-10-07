# Review — `wordfreq` (adversarial, fresh subagent)

| # | Sev | Issue | Failure | Status |
|---|---|---|---|---|
| 1 | High | ASCII-only regex splits non-English words | `café` → `caf`, `e`; `don’t` → `don`, `t` | Fixed: Unicode `[^\W_]+`, curly apostrophes, `casefold()` |
| 2 | Med | Stdin decoded strictly (files used `errors="replace"`) | `\xff` on stdin → `UnicodeDecodeError` traceback | Fixed: lenient UTF-8 wrapper on `stdin.buffer` |
| 3 | Med | `BrokenPipeError` caught as a file error | `… \| head -1` → `wordfreq: None: Broken pipe`, rc=120 | Fixed: separate output handling, exits quietly |
| 4 | Low | `-` not accepted as stdin | `wordfreq -` → "No such file" | Fixed |
| 5 | Low | Repeated apostrophes split unevenly | `rock'n'roll` → `rock'n`, `roll` | Fixed |
| 6 | Low | Binary files counted silently | `wordfreq /bin/ls` → counts garbage | Won't fix (smoke test). Documented |

Test gaps flagged (ASCII-only inputs, no multi-file or stdin-mix cases, a loose `assertIn`) are closed. The suite went from 6 to 10 tests.
