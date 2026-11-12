# Swami's Vibe Tools

Free browser tools for 3D printing, CNC, and design — by Swami, vibe coded with Claude.

**Open the library:** https://swami-claude-skills.github.io/vibe-tools/

Every tool runs in your web browser. No account, no install.

| Tool | What it does | Link |
|---|---|---|
| Image to Relief Generator | Turns a render, photo, height map, or multi-view sheet into a smooth 3D relief for CNC carving, with a 3D viewer, toolpath preview, and STL/OBJ/height-map/outline/contour exports. | https://swami-claude-skills.github.io/vibe-tools/relief-generator/ |

Tool links never change: a bookmark always opens the newest version. Each tool shows its version date in its header.

**Problems or ideas?** Use the Swami link at the bottom of the library page.

**Build your own with Claude:** see [Swami's Claude Skills](https://claude.ai/artifact/Mg8X9h2EDFMLnsPcG9d2SE).

---

### For maintenance

- `tools.json` lists the public tools; the library page (`index.html`) is built from it.
- Each tool lives in its own folder (`relief-generator/index.html`).
- Rebuild the library: `sh _build/build_all.sh <vibe-dashboard skill folder>`, then the audio overview with `_build/stress_audio.py` (see `_build/build_all.sh`).
- Only public tools ever go in this repo. Private or client tools are never committed here.
- Changes go straight to `main`; GitHub Pages serves `main` within a minute or two.
