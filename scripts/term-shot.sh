#!/usr/bin/env bash
# Render a command and its output as a PNG, for PR proof (conventions/pull-requests.md).
# The command line is shown in bold yellow; output lines matching the optional regex are highlighted green.
# Usage: term-shot.sh <output.png> '<command>' ['<highlight regex>']
# Requires freeze (github.com/charmbracelet/freeze); set FREEZE to override its path.
set -euo pipefail

if [[ ${1:-} == --inner ]]; then
  printf '\033[1;33m$ %s\033[0m\n' "$CMD"
  if [[ -n $HIGHLIGHT ]]; then
    eval "$CMD" 2>&1 | GREP_COLOR='1;32' GREP_COLORS='mt=1;32' grep --color=always -E "$HIGHLIGHT|$" || true
  else
    eval "$CMD" 2>&1 || true
  fi
  exit 0
fi

out=$1
export CMD=$2 HIGHLIGHT=${3:-}
"${FREEZE:-$HOME/.local/bin/freeze}" --execute "bash $0 --inner" --window --padding 20 --margin 0 \
  --output "$out" </dev/null >/dev/null
echo "$out"
