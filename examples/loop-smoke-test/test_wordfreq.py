import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("wordfreq.py")


def run(*args, stdin=b""):
    if isinstance(stdin, str):
        stdin = stdin.encode()
    r = subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True)
    return r.returncode, r.stdout.decode(), r.stderr.decode()


def words(stdout):
    return [line.split() for line in stdout.splitlines()]


class WordFreqCLI(unittest.TestCase):
    def test_counts_case_insensitively_and_ranks(self):
        _, out, _ = run("-n", "2", stdin="The cat. the CAT! the dog")
        self.assertEqual(words(out), [["3", "the"], ["2", "cat"]])

    def test_ties_break_alphabetically(self):
        _, out, _ = run(stdin="b a c")
        self.assertEqual(words(out), [["1", "a"], ["1", "b"], ["1", "c"]])

    def test_contractions_stay_whole(self):
        _, out, _ = run(stdin="Don't don’t rock'n'roll 'tis")
        self.assertEqual(words(out), [["1", "don't"], ["1", "don’t"],
                                      ["1", "rock'n'roll"], ["1", "tis"]])

    def test_unicode_words_are_not_split(self):
        _, out, _ = run(stdin="café Café naïve Straße")
        self.assertEqual(words(out), [["2", "café"], ["1", "naïve"], ["1", "strasse"]])

    def test_invalid_utf8_on_stdin_does_not_crash(self):
        code, out, err = run(stdin=b"ok \xff bad")
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(w for _, w in words(out)), ["bad", "ok"])

    def test_reads_multiple_files_and_dash_for_stdin(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("apple apple banana\n")
        try:
            _, out, _ = run(f.name, "-", f.name, stdin="banana")
            self.assertEqual(words(out), [["4", "apple"], ["3", "banana"]])
        finally:
            Path(f.name).unlink()

    def test_empty_input_prints_nothing(self):
        self.assertEqual(run(stdin="")[:2], (0, ""))

    def test_missing_file_fails_cleanly(self):
        code, _, err = run("nope.txt")
        self.assertEqual(code, 1)
        self.assertIn("nope.txt", err)
        self.assertNotIn("Traceback", err)

    def test_rejects_non_positive_n(self):
        for n in ("0", "-3"):
            code, _, err = run("-n", n)
            self.assertEqual(code, 2)
            self.assertIn("-n must be >= 1", err)

    def test_closed_pipe_exits_quietly(self):
        text = " ".join(f"w{i}" for i in range(50000))
        p = subprocess.run(
            f'"{sys.executable}" "{SCRIPT}" -n 50000 | head -1',
            shell=True, input=text.encode(), capture_output=True)
        self.assertEqual(len(p.stdout.splitlines()), 1)
        self.assertEqual(p.stderr.decode(), "")


if __name__ == "__main__":
    unittest.main()
