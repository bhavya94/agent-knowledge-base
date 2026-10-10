"""Turn `path:lines` and `:lines` code references in a Markdown explainer into commit-pinned GitHub links.

A bare `:lines` refers to the last file path mentioned. Run once the PR's commit is pushed; src may equal dst.
Usage: python3 explainer-permalinks.py <src.md> <dst.md> <repo-dir> <commit-sha> <owner/repo>
"""
import re
import subprocess
import sys

src, dst, repo_dir, sha, slug = sys.argv[1:6]
files = set(subprocess.run(["git", "-C", repo_dir, "ls-tree", "-r", "--name-only", sha],
                           capture_output=True, text=True, check=True).stdout.split())
ref = re.compile(r"^(?P<path>[\w./-]*):(?P<a>\d+)(?:-(?P<b>\d+))?$")
last = None
converted = 0


def link(match: re.Match) -> str:
    global last, converted
    token = match.group(1)
    m = ref.match(token)
    if m and (m["path"] in files or (not m["path"] and last)):
        path = m["path"] or last
        last = path
        anchor = f"#L{m['a']}" + (f"-L{m['b']}" if m["b"] else "")
        shown = token if m["path"] else f"{path.rsplit('/', 1)[-1]}{token}"
        converted += 1
        return f"[`{shown}`](https://github.com/{slug}/blob/{sha}/{path}{anchor})"
    if token in files:
        last = token
    return match.group(0)


text = re.sub(r"`([^`\n]+)`", link, open(src).read())
open(dst, "w").write(text)
leftovers = re.findall(r"(?<!\[)`[^`]*:[0-9][0-9-]*`", text)
print(dst.rsplit("/", 1)[-1] + ":", converted, "references linked; unlinked leftovers:", leftovers)
