#!/bin/sh
# Rebuild index.html from tools.json. Usage: sh _build/build_all.sh SKILL_DIR   (vibe-dashboard skill folder)
# Then rebuild the audio overview: python3 _build/stress_audio.py SKILL_DIR build index.html _build/narration.txt index.html
set -e
SK="$1"; cd "$(dirname "$0")/.."
python3 _build/build_library.py "$SK"
python3 _build/fit_patch.py index.html
python3 "$SK/scripts/search_patch.py" index.html
python3 _build/mindmap_patch.py index.html
