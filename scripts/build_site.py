#!/usr/bin/env python3
"""Build the ifURI brand/logo gallery for logo.ifuri.com."""
import os, sys, html, shutil, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"_site"
ASSET_DIRS=["svg","png","ico","color","pdf","webp"]
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for d in ASSET_DIRS:
    if (ROOT/d).is_dir(): shutil.copytree(ROOT/d, OUT/d)
for f in ROOT.glob("*.svg"): shutil.copy2(f, OUT/f.name)
for f in ["COLORS.md","README.md"]:
    if (ROOT/f).exists(): shutil.copy2(ROOT/f, OUT/f)

def card(img, label, links):
    ls=" · ".join(f'<a href="{u}">{t}</a>' for t,u in links)
    return f'<figure class="logo-card"><div class="show"><img src="{img}" alt="{html.escape(label)}" loading="lazy"></div><figcaption>{html.escape(label)}<span>{ls}</span></figcaption></figure>'

cards=[]
cards.append(card("svg/lockup/ifuri-lockup-horizontal-dark.svg","Lockup — horizontal",[("SVG","svg/lockup/ifuri-lockup-horizontal-dark.svg"),("light","svg/lockup/ifuri-lockup-horizontal.svg"),("PNG","png/lockup/1200/")]))
cards.append(card("svg/lockup/ifuri-lockup-tagline-dark.svg","Lockup — with tagline",[("SVG","svg/lockup/ifuri-lockup-tagline-dark.svg")]))
cards.append(card("svg/lockup/ifuri-lockup-stacked-dark.svg","Lockup — stacked",[("SVG","svg/lockup/ifuri-lockup-stacked-dark.svg")]))
cards.append(card("svg/mark/ifuri-mark.svg","Mark",[("SVG","svg/mark/ifuri-mark.svg"),("mono","svg/mark/ifuri-mark-mono.svg")]))
cards.append(card("svg/icon/ifuri-icon.svg","Icon",[("SVG","svg/icon/ifuri-icon.svg"),("PNG 512","png/icon/512x512/"),("ICO","ico/favicon.ico")]))
cards.append(card("color/palette.svg","Colour palette",[("SVG","color/palette.svg"),("tokens.css","color/tokens.css"),("tokens.json","color/tokens.json")]))

grid="".join(cards)
page=f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ifURI — logo & brand kit</title><meta name="theme-color" content="#1E1B4B">
<link rel="icon" href="svg/icon/ifuri-favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css">
</head><body>
<header><a class="brand" href="index.html">ifURI <span>brand</span></a>
<nav><a href="https://ifuri.com/">ifuri.com</a><a href="https://docs.ifuri.com/">Docs</a><a href="https://github.com/if-uri/logo">GitHub</a></nav></header>
<main>
<h1>ifURI — logo &amp; brand kit</h1>
<p class="lead">The mark is a conditional fork on a URI path: a branch meeting a slash at a right angle (the <code>if</code>) flowing into a parallel <code>//</code> (the URI). Palette: indigo + emerald + slate.</p>
<div class="grid">{grid}</div>
<h2>Files</h2>
<p>Vectors in <a href="svg/">svg/</a>, raster in <a href="png/">png/</a>, favicon <a href="ico/favicon.ico">ico/favicon.ico</a>, print <a href="pdf/">pdf/</a>, tokens in <a href="color/">color/</a>. Full guide: <a href="COLORS.md">COLORS.md</a>.</p>
</main>
<footer>ifURI brand kit · <a href="https://ifuri.com/">ifuri.com</a></footer>
</body></html>"""
(OUT/"index.html").write_text(page,encoding="utf-8")
(OUT/"style.css").write_text(""":root{--bg:#1E1B4B;--card:rgba(255,255,255,.06);--text:#EEF2FF;--muted:#A5B4FC;--line:rgba(255,255,255,.14);--green:#34D399}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 520px at 88% -8%,rgba(79,70,229,.2),transparent 60%),linear-gradient(180deg,#1E1B4B,#191640);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;line-height:1.6;min-height:100vh}
a{color:var(--green);text-decoration:none}a:hover{text-decoration:underline}
header{position:sticky;top:0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 24px;border-bottom:1px solid var(--line);background:rgba(30,27,75,.82);backdrop-filter:blur(12px)}
.brand{font-weight:800;font-size:18px;color:var(--text)}.brand span{color:var(--green)}
header nav a{color:var(--muted);font-weight:700;font-size:14px;margin-left:16px}
main{max-width:1040px;margin:0 auto;padding:36px 24px 72px}
h1{font-size:clamp(28px,4vw,42px);letter-spacing:-.02em;margin:0 0 6px}h2{font-size:23px;margin:34px 0 0}
.lead{font-size:18px;color:#cdd6ee;max-width:680px}p{color:#cdd6ee}
code{background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);color:#6EE7B7;border-radius:6px;padding:.06rem .35rem;font-family:ui-monospace,Menlo,monospace;font-size:.9em}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}
.logo-card{margin:0;border:1px solid var(--line);background:var(--card);border-radius:14px;overflow:hidden}
.logo-card .show{display:grid;place-items:center;min-height:150px;padding:24px;background:repeating-linear-gradient(45deg,rgba(255,255,255,.02) 0 10px,transparent 10px 20px)}
.logo-card img{max-width:100%;max-height:90px}
.logo-card figcaption{padding:12px 16px;border-top:1px solid var(--line);font-weight:700;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.logo-card figcaption span{font-weight:600;font-size:13px;color:var(--muted)}
footer{max-width:1040px;margin:0 auto;padding:24px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media(max-width:820px){.grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.grid{grid-template-columns:1fr}}""",encoding="utf-8")
print(f"built logo gallery -> {OUT} ({len(cards)} cards)")
