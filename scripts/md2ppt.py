#!/usr/bin/env python3
import argparse
import html
import re
from pathlib import Path

DARK_CSS = """
:root{--w:1280px;--h:720px;--bg:#0b1020;--fg:#eaf0ff;--muted:#9fb0d6;--accent:#66d9ef;--card:#121a31}
*{box-sizing:border-box}
body{margin:0;background:#070b16;color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Noto Sans CJK SC',sans-serif}
.deck{display:flex;flex-direction:column;gap:18px;padding:24px;align-items:center}
.slide{width:var(--w);height:var(--h);background:linear-gradient(160deg,#0d1326,#0a1022);border:1px solid #253458;border-radius:16px;padding:44px;position:relative;overflow:hidden}
.slide h1{margin:.1em 0 .35em;font-size:46px;line-height:1.15}
.slide h2{margin:.1em 0 .35em;font-size:36px;color:#d7e4ff}
.slide h3{margin:.1em 0 .35em;font-size:28px;color:#cae2ff}
.slide p,.slide li{font-size:24px;line-height:1.45}
.slide ul{margin:.3em 0 .3em 1.1em}
.slide code{background:#1e2b4a;padding:.1em .3em;border-radius:6px}
pre{background:#0b1530;padding:14px;border-radius:10px;overflow:auto;border:1px solid #2d3f67}
.table{width:100%;border-collapse:collapse;font-size:20px}
.table th,.table td{border:1px solid #355087;padding:8px 10px}
.table th{background:#13203f}
.tip{border-left:5px solid var(--accent);padding:10px 14px;background:#0d1a36;border-radius:8px;margin:8px 0}
.card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.card{background:var(--card);border:1px solid #2c3f68;border-radius:10px;padding:12px}
.muted{color:var(--muted)}
.footer{position:absolute;right:28px;bottom:18px;font-size:16px;color:#94a3c8}
"""

LIGHT_CSS = """
:root{--w:1280px;--h:720px;--bg:#f6f8fc;--fg:#0f172a;--muted:#64748b;--accent:#2563eb;--card:#ffffff}
*{box-sizing:border-box}
body{margin:0;background:#f3f5f9;color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Noto Sans CJK SC',sans-serif}
.deck{display:flex;flex-direction:column;gap:18px;padding:24px;align-items:center}
.slide{width:var(--w);height:var(--h);background:linear-gradient(160deg,#ffffff,#f8fbff);border:1px solid #dbe4f0;border-radius:16px;padding:44px;position:relative;overflow:hidden;box-shadow:0 6px 24px rgba(15,23,42,.06)}
.slide h1{margin:.1em 0 .35em;font-size:46px;line-height:1.15;color:#0b1220}
.slide h2{margin:.1em 0 .35em;font-size:36px;color:#1e3a8a}
.slide h3{margin:.1em 0 .35em;font-size:28px;color:#1d4ed8}
.slide p,.slide li{font-size:24px;line-height:1.45}
.slide ul{margin:.3em 0 .3em 1.1em}
.slide code{background:#e8eef9;padding:.1em .3em;border-radius:6px;color:#0f172a}
pre{background:#f2f6fc;padding:14px;border-radius:10px;overflow:auto;border:1px solid #d5e0f0}
.table{width:100%;border-collapse:collapse;font-size:20px}
.table th,.table td{border:1px solid #cdd9eb;padding:8px 10px}
.table th{background:#eaf1fb}
.tip{border-left:5px solid var(--accent);padding:10px 14px;background:#eef4ff;border-radius:8px;margin:8px 0}
.card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.card{background:var(--card);border:1px solid #d7e1f0;border-radius:10px;padding:12px}
.muted{color:var(--muted)}
.footer{position:absolute;right:28px;bottom:18px;font-size:16px;color:#64748b}
"""

def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text

def render_table(lines):
    rows = [ln.strip().strip('|').split('|') for ln in lines]
    if len(rows) < 2:
        return ''
    head = ''.join(f'<th>{inline_md(c.strip())}</th>' for c in rows[0])
    body_rows = []
    for r in rows[2:]:
        body_rows.append('<tr>' + ''.join(f'<td>{inline_md(c.strip())}</td>' for c in r) + '</tr>')
    return f"<table class='table'><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"

def render_slide(md: str, idx: int, total: int) -> str:
    lines = md.strip().splitlines()
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
        elif ln.startswith('# '): out.append(f'<h1>{inline_md(ln[2:].strip())}</h1>')
        elif ln.startswith('## '): out.append(f'<h2>{inline_md(ln[3:].strip())}</h2>')
        elif ln.startswith('### '): out.append(f'<h3>{inline_md(ln[4:].strip())}</h3>')
        elif ln.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(f"<li>{inline_md(lines[i][2:].strip())}</li>")
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>')
            continue
        elif ln.startswith('> '): out.append(f"<div class='tip'>{inline_md(ln[2:].strip())}</div>")
        elif re.match(r"^\|.*\|$", ln):
            t = []
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i]):
                t.append(lines[i]); i += 1
            out.append(render_table(t)); continue
        else: out.append(f'<p>{inline_md(ln)}</p>')
        i += 1
    out.append(f"<div class='footer'>{idx}/{total}</div>")
    return '<section class="slide">' + ''.join(out) + '</section>'

def main():
    ap = argparse.ArgumentParser(description='Markdown to simple HTML presentation (1280x720).')
    ap.add_argument('input')
    ap.add_argument('-o','--output',required=True)
    ap.add_argument('--theme', choices=['dark', 'light'], default='light')
    args = ap.parse_args()

    md = Path(args.input).read_text(encoding='utf-8')
    chunks = [c for c in re.split(r'\n---\n', md) if c.strip()]
    slides = [render_slide(c, i+1, len(chunks)) for i, c in enumerate(chunks)]
    css = LIGHT_CSS if args.theme == 'light' else DARK_CSS
    html_doc = f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Presentation</title><style>{css}</style></head><body><main class='deck'>{''.join(slides)}</main></body></html>"
    Path(args.output).write_text(html_doc, encoding='utf-8')
    print(f'Wrote {args.output} ({len(chunks)} slides, theme={args.theme})')

if __name__ == '__main__':
    main()
