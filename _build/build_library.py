"""Build the Vibe Tools library page (index.html) from tools.json, in the vibe-dashboard design system.

Usage (from the repo root):
  python3 _build/build_library.py SKILL_DIR
    SKILL_DIR = the vibe-dashboard skill folder (holds assets/template.html and scripts/)
Then run, in order: fit_patch.py, scripts/search_patch.py, mindmap_patch.py, and the audio overview build
(see the vibe-dashboard skill). _build/ is not served by GitHub Pages.
Only PUBLIC tools ever go in tools.json or this repo.
"""
import json, os, re, sys, html
SKILL = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(SKILL, 'assets', 'template.html'), encoding='utf-8').read()
DATA = json.load(open(os.path.join(ROOT, 'tools.json'), encoding='utf-8'))
LIB, TOOLS, GROUPS = DATA['library'], DATA['tools'], DATA['groups']
GCOLOR = {g['name']: g['color'] for g in GROUPS}
SKILL_LIB = 'https://claude.ai/artifact/Mg8X9h2EDFMLnsPcG9d2SE'
REPO = 'https://github.com/swami-claude-skills/vibe-tools'
E = html.escape
D = lambda s: f'<b class="dt">{E(s)}</b>'

CATS = [('overview', '#38dafa', 'OVERVIEW'), ('library', '#38fa79', 'LIBRARY'),
        ('using', '#dafa38', 'USING'), ('updates', '#fa9938', 'UPDATES'), ('reference', '#3879fa', 'REFERENCE')]
def rgb(h): return ','.join(str(int(h[i:i+2], 16)) for i in (1, 3, 5))
BADGE = {c[0]: c[2] for c in CATS}

def rep(old, new):
    global T
    assert T.count(old) >= 1, old[:70]
    T = T.replace(old, new, 1)

rep("""    --cat-overview:#38dafa;   /* palette 1 (cyan)  */
    --cat-source:#38fa79;     /* palette 2 (green) */""", '\n'.join(f'    --cat-{n}:{h};' for n, h, _ in CATS))
rep("""  .toc-tip.tc-overview .tip-badge{color:var(--cat-overview);background:rgba(56,218,250,.10)}
  .toc-tip.tc-source .tip-badge{color:var(--cat-source);background:rgba(56,250,121,.10)}""",
    '\n'.join(f'  .toc-tip.tc-{n} .tip-badge{{color:var(--cat-{n});background:rgba({rgb(h)},.10)}}' for n, h, _ in CATS))
rep("""  .cat-overview .cat-badge{color:var(--cat-overview);background:rgba(56,218,250,.10)}
  .cat-overview{border-left:3px solid var(--cat-overview)}
  .toc-chip.tc-overview{border-left-color:var(--cat-overview)}
  .toc-chip.tc-overview:hover{color:var(--cat-overview)}
  .cat-source .cat-badge{color:var(--cat-source);background:rgba(56,250,121,.10)}
  .cat-source{border-left:3px solid var(--cat-source)}
  .toc-chip.tc-source{border-left-color:var(--cat-source)}
  .toc-chip.tc-source:hover{color:var(--cat-source)}""", '\n'.join(
    f'  .cat-{n} .cat-badge{{color:var(--cat-{n});background:rgba({rgb(h)},.10)}}\n  .cat-{n}{{border-left:3px solid var(--cat-{n})}}\n'
    f'  .toc-chip.tc-{n}{{border-left-color:var(--cat-{n})}}\n  .toc-chip.tc-{n}:hover{{color:var(--cat-{n})}}' for n, h, _ in CATS))
rep('  .cite:hover{color:var(--cyan)}\n', '''  .cite:hover{color:var(--cyan)}
  .dt{color:#fff;font-weight:700}
  .open-tool{display:inline-block;font-family:var(--mono);font-size:12px;font-weight:700;color:#0d0d0f;background:var(--cyan);border-radius:6px;padding:3px 10px;text-decoration:none;white-space:nowrap}
  .open-tool:hover{filter:brightness(1.15)}
  .status-grid{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;font-size:14px;margin:4px 0}
  .status-grid .k{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-mute);align-self:center}
''')

n_tools, n_groups = len(TOOLS), len({t['group'] for t in TOOLS})
plural = lambda n, w: f'{n} {w}' + ('' if n == 1 else 's')
newest = max(TOOLS, key=lambda t: t['updated'])  # dates share one format; fine while few tools

rep('{{PAGE_TITLE}}', E(LIB['title']))
rep('{{KICKER}}', 'TOOL LIBRARY')
rep('{{H1_TITLE}}', E(LIB['title']))
rep('{{H1_SUBTITLE}}', 'free browser tools for 3D printing, CNC, and design')
rep("""    <span>{{BYLINE_A}}</span>
    <span>{{BYLINE_B}}</span>""", f"""    <span>Swami</span>
    <span>{plural(n_tools, 'tool')} · {plural(n_groups, 'group')}</span>
    <span>list built {D(LIB['built'])}</span>""")
rep('{{MAIL_SUBJECT}}', 'Vibe Tools')

def li(tid, body): return f'<li><span class="tid">{tid}</span>{body}</li>'
def ul(items): return '<ul>' + ''.join(li(t, b) for t, b in items) + '</ul>'
def callout(lbl, txt): return f'<div class="callout"><span class="lbl">{lbl}</span>{txt}</div>'
def gtag(g): return f'<span class="tid" style="--tc:{GCOLOR.get(g, "#38dafa")}">{E(g)}</span>'

rows = ''.join(
    f'<tr><td><strong>{E(t["name"])}</strong></td><td>{gtag(t["group"])}</td><td>{E(t["summary"])}</td>'
    f'<td>{E(t["whats_new"])}</td><td>{D(t["updated"])}</td>'
    f'<td><a class="open-tool" href="{E(t["path"])}" target="_blank" rel="noopener">Open tool ↗</a></td></tr>' for t in TOOLS)

SECS = [
 ('Tool Library (open from here)', 'library', 'Every tool with what it does, what changed, and its link', 'Finding a tool and opening it',
  f'''<p>Open any tool with the <strong>Open tool</strong> link in its row. These links work for anyone, no Claude account needed: each tool runs right in your web browser.</p>
''' + callout('Status', f'''<div class="status-grid"><span class="k">Contents</span><span>{plural(n_tools, 'tool')} in {plural(n_groups, 'group')}</span>
<span class="k">Newest change</span><span>{D(newest['updated'])} · {E(newest['name'])}</span>
<span class="k">List built</span><span>{D(LIB['built'])}</span></div>''') + f'''
<div class="table-wrap" data-desc="All tools">
  <table><thead><tr><th>Tool</th><th>Group</th><th>What it does</th><th>What's new</th><th>Updated</th><th>Open</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>'''),
 ('Using the Tools', 'using', 'How the tools run, which browsers work, and saving files', 'Opening a tool for the first time, or something does not work',
  ul([
   ('No account', 'Open the link and use the tool. There is nothing to install and no sign-in.'),
   ('In your browser', 'Each tool is a single web page that does its work on your own computer.'),
   ('Browsers', 'Use a current Chrome, Edge, Safari, or Firefox on a desktop or laptop. The 3D views need a computer with graphics support, which almost every recent one has.'),
   ('Saving files', 'Exports save straight to your browser&#39;s Downloads folder. Large meshes come zipped.'),
   ('Blank viewer', 'If a 3D view stays blank, close other heavy tabs and reload, or try another browser.'),
  ]) + callout('Bookmark it', 'Each tool keeps the same link forever, so a bookmark always opens the newest version.')),
 ('Updates & Versions (explained)', 'updates', 'How the list stays current, version dates, and reporting a problem', 'Checking how current a tool is, or reporting a problem',
  ul([
   ('Same links', 'Tool links never change. When a tool is updated, the same link opens the new version; reload the page if it still looks old.'),
   ('Version date', 'Each tool shows its version date in its header, matching the Updated column in Tool Library (open from here).'),
   ('Where they live', f'The tools are kept on GitHub, which records every version: <a href="{REPO}" target="_blank" rel="noopener">vibe-tools on GitHub ↗</a>'),
   ('Skills', f'Want Claude to build pages like these? See <a href="{SKILL_LIB}" target="_blank" rel="noopener">Swami&#39;s Claude Skills ↗</a>.'),
   ('Problems', 'Use the Swami link at the bottom of this page to email what happened, which tool, and which browser.'),
  ])),
]

GL = [
 ('github', r'GitHub', 'GitHub', 'Library', '#38dafa', 'Website that hosts the tools and keeps a record of every version.'),
 ('version-date', r'version dates?', 'Version date', 'Library', '#38dafa', 'The date a tool was last changed, shown in its header and in the Updated column.'),
 ('browser', r'browsers?', 'Browser', 'Using', '#38fa79', 'The program you view web pages with, such as Chrome, Edge, Safari, or Firefox.'),
 ('export', r'exports?', 'Export', 'Using', '#38fa79', 'Saving a file a tool made, such as a mesh or an image, to your computer.'),
 ('mesh', r'mesh(?:es)?', 'Mesh', '3D', '#dafa38', 'A 3D shape made of many small flat faces, saved as STL or OBJ.'),
 ('relief', r'reliefs?', 'Relief', '3D', '#dafa38', 'A carving that rises from a flat background, like a sign or a coin.'),
 ('height-map', r'height[ -]?maps?', 'Height map', '3D', '#dafa38', 'A grayscale image where brighter means higher and darker means lower.'),
 ('stl', r'STL', 'STL', '3D', '#dafa38', 'The most common 3D mesh file type, read by slicers and CAM software.'),
 ('obj', r'OBJ', 'OBJ', '3D', '#dafa38', 'A 3D mesh file type that can keep four-sided faces and textures.'),
 ('cnc', r'CNC', 'CNC', 'Making', '#fa9938', 'Computer-controlled cutting machines, such as a wood router.'),
 ('toolpath', r'toolpaths?', 'Toolpath', 'Making', '#fa9938', 'The path a CNC cutter follows to carve a shape.'),
 ('zip', r'zipped|zips?', 'Zip', 'Using', '#38fa79', 'A compressed file that holds one or more files; open it to get them out.'),
 ('claude', r'Claude', 'Claude', 'Library', '#38dafa', 'Anthropic&#39;s AI assistant, which Swami vibe codes these tools with.'),
]
grows = ''.join(f'<tr data-gterm="{i}" data-match="{m}" data-code=""><td><strong>{t}</strong></td><td><span class="tid" style="--tc:{c}">{tp}</span></td><td>{d}</td><td class="gloss-uses"></td><td class="gloss-count"></td></tr>' for i, m, t, tp, c, d in GL)

summary_rows = ''.join(f'<tr><td><span class="secnum">{n+2:02d}</span></td><td><strong>{t}</strong></td><td class="sec-cat"></td><td>{f}</td><td>{w}</td></tr>' for n, (t, c, f, w, b) in enumerate(SECS))
content = ''.join(f'''
  <div class="section cat-{c}" data-title="{t}" data-cat="{c}">
    <div class="sec-head"><span class="sec-num">{n+2:02d}</span><span class="sec-title">{t}</span><span class="cat-badge">{BADGE[c]}</span><span class="chevron">▶</span></div>
    <div class="sec-body">
      {b}
    </div>
  </div>
''' for n, (t, c, f, w, b) in enumerate(SECS))
N = len(SECS) + 2
i0 = T.index('  <!-- REQUIRED FIRST SECTION'); i1 = T.index('</main>')
main = f'''  <div class="section cat-overview" data-title="Dashboard Summary" data-cat="overview">
    <div class="sec-head"><span class="sec-num">01</span><span class="sec-title">Dashboard Summary</span><span class="cat-badge">OVERVIEW</span><span class="chevron">▶</span></div>
    <div class="sec-body">
      <p>This page lists Swami&#39;s free browser tools for 3D printing, CNC, and design. Tool Library (open from here) has every tool with what it does, what changed, and its link. Using the Tools covers browsers and saving files, and Updates &amp; Versions (explained) shows how the tools stay current. Terms with a dotted underline jump to the Glossary.</p>
      {callout('Quick start', 'Open Tool Library (open from here) and click a tool&#39;s <strong>Open tool</strong> link. No account or install needed.')}
      <div class="table-wrap" data-desc="What each section covers">
        <table>
          <thead><tr><th>#</th><th>Section</th><th>Category</th><th>Focus</th><th>Use When</th></tr></thead>
          <tbody>
            <tr><td><span class="secnum">01</span></td><td><strong>Dashboard Summary</strong></td><td class="sec-cat"></td><td>This overview and the section index</td><td>Getting oriented</td></tr>
            {summary_rows}
            <tr><td><span class="secnum" data-target-title="Glossary"></span></td><td><strong>Glossary</strong></td><td class="sec-cat"></td><td>Term definitions with jump links both ways</td><td>A term is unfamiliar, or you want every place it&#39;s used</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
{content}
  <div class="section cat-reference" data-title="Glossary" data-cat="reference">
    <div class="sec-head"><span class="sec-num">{N:02d}</span><span class="sec-title">Glossary</span><span class="cat-badge">REFERENCE</span><span class="chevron">▶</span></div>
    <div class="sec-body">
      <p>Every term with a <span class="gterm-demo">dotted underline</span> in the dashboard links here — hover it for a quick definition, click it to land on its row. In the <strong>Appears in</strong> column, each number is a jump link to where that term is used in that section; the term flashes green when you arrive. <strong>Qty</strong> counts every mention across the content sections. Each term&#39;s <strong>Topic</strong> tag names what it is about, one color per topic.</p>
      <div class="table-wrap" data-desc="Glossary of terms">
        <table>
          <thead><tr><th>Term</th><th>Topic</th><th>Definition</th><th>Appears in</th><th>Qty</th></tr></thead>
          <tbody>{grows}</tbody>
        </table>
      </div>
    </div>
  </div>

'''
T = T[:i0] + main + T[i1:]
# no verbatim section on this page
T = re.sub(r"/\* ---- verbatim content.*?\n}\n", '', T, count=1, flags=re.S)
T = T.replace("const VERBATIM = `{{VERBATIM_TEXT}}`;", "")
rep("def = row.cells[1].textContent.trim();",
    "def = ([...row.cells].slice(1).find(c => !c.querySelector('.tid') && !c.matches('.gloss-uses,.gloss-count')) || {textContent:''}).textContent.trim();")
rep("buildFloatingHeaders();\n", """buildFloatingHeaders();

/* ---- glossary: start sorted by Topic column (asc) ---- */
(function(){
  const gsec = document.querySelector('.section[data-title="Glossary"]');
  if(!gsec) return;
  const table = gsec.querySelector('.table-wrap table');
  if(!table || !table.tHead) return;
  const ths = [...table.tHead.rows[0].cells];
  const ti = ths.findIndex(th => { const t = th.childNodes[0]; return t && t.nodeType === 3 && t.nodeValue.trim().toUpperCase() === 'TOPIC'; });
  if(ti < 0) return;
  ths[ti].click();
})();
""")
left = re.findall(r'\{\{\w+\}\}', T)
assert not left, left
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(T)
print('index.html built:', len(T), 'bytes,', n_tools, 'tools')
