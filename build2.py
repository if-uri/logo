#!/usr/bin/env python3
# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

import os, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

import pathlib as _pathlib
ROOT=str(_pathlib.Path.home() / "ifuri-logo/pkg")

# ============================================================
#  STANDARDIZED COLOR TOKENS
# ============================================================
RAMPS = {
 "primary": {  # Indigo
   "50":"#EEF2FF","100":"#E0E7FF","200":"#C7D2FE","300":"#A5B4FC","400":"#818CF8",
   "500":"#6366F1","600":"#4F46E5","700":"#4338CA","800":"#3730A3","900":"#312E81","950":"#1E1B4B"},
 "accent": {   # Emerald
   "50":"#ECFDF5","100":"#D1FAE5","200":"#A7F3D0","300":"#6EE7B7","400":"#34D399",
   "500":"#10B981","600":"#059669","700":"#047857","800":"#065F46","900":"#064E3B"},
 "neutral": {  # Slate
   "50":"#F8FAFC","100":"#F1F5F9","200":"#E2E8F0","300":"#CBD5E1","400":"#94A3B8",
   "500":"#64748B","600":"#475569","700":"#334155","800":"#1E293B","900":"#0F172A"},
}
WHITE="#FFFFFF"; BLACK="#000000"
SEM = {
 "brand-primary":      ("primary","600"),
 "brand-primary-dark": ("primary","950"),
 "brand-accent":       ("accent","500"),
 "brand-accent-bright":("accent","400"),
 "surface-dark":       ("primary","950"),
 "surface-light":      ("primary","50"),
 "text-ink":           ("primary","950"),
 "text-muted":         ("neutral","500"),
 "text-muted-dark":    ("primary","300"),
}
def C(ramp,step): return RAMPS[ramp][step]
def S(name):
    r,s=SEM[name]; return C(r,s)

# convenient brand colours
PRIMARY=S("brand-primary"); INK=S("brand-primary-dark")
ACCENT=S("brand-accent"); ACCENT_BRIGHT=S("brand-accent-bright")
PAPER=S("surface-light"); MUTED=S("text-muted"); MUTED_D=S("text-muted-dark")
MOTTO="name it run it"

# ============================================================
#  FONTS / TEXT -> PATHS
# ============================================================
med=TTFont(str(_pathlib.Path.home() / "ifuri-logo/Poppins-Medium.ttf"))
reg=TTFont(str(_pathlib.Path.home() / "ifuri-logo/Poppins-Regular.ttf"))
def layout(font, segments):
    gs=font.getGlyphSet(); cmap=font.getBestCmap(); upm=font["head"].unitsPerEm
    out=[]; bp=BoundsPen(gs); x=0.0
    for text,color in segments:
        pen=SVGPathPen(gs)
        for ch in text:
            g=cmap.get(ord(ch))
            if g is None: x+=upm*0.30; continue
            gs[g].draw(TransformPen(pen,(1,0,0,1,x,0)))
            gs[g].draw(TransformPen(bp,(1,0,0,1,x,0)))
            x+=gs[g].width
        out.append((pen.getCommands(),color))
    xmin,ymin,xmax,ymax = bp.bounds if bp.bounds else (0,0,x,0)
    return {"paths":out,"upm":upm,"xmin":xmin,"ymin":ymin,"xmax":xmax,"ymax":ymax}
def render_text(lay,size,ink_x,baseline_y):
    s=size/lay["upm"]; ox=ink_x-lay["xmin"]*s
    parts="".join(f'<path d="{d}" fill="{c}"/>' for d,c in lay["paths"])
    return f'<g transform="translate({ox:.2f},{baseline_y:.2f}) scale({s:.5f},{-s:.5f})">{parts}</g>'
def tw(l,sz): return (l["xmax"]-l["xmin"])*sz/l["upm"]
def ttop(l,sz): return l["ymax"]*sz/l["upm"]
def tbot(l,sz): return l["ymin"]*sz/l["upm"]

# ============================================================
#  MARK  (content bbox-driven)
# ============================================================
CX0,CY0,CW,CH=3,2,19,12
TX0,TY0,TW,TH=3,2,11,12
def _l(x1,y1,x2,y2,c,sw): return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
    f'stroke="{c}" stroke-width="{sw:.2f}" stroke-linecap="round"/>')
def mark_art(x,y,h,struct,acc):
    s=h/CH; sw=2.2*s; ox=x-CX0*s; oy=y-CY0*s
    L=lambda a,b,c,d,col:_l(ox+a*s,oy+b*s,ox+c*s,oy+d*s,col,sw)
    return L(3,3,9,8,struct)+L(4,14,14,2,struct)+L(12,14,22,2,acc), h*CW/CH
def fork_art(x,y,h,col):
    s=h/TH; sw=2.2*s; ox=x-TX0*s; oy=y-TY0*s
    L=lambda a,b,c,d:_l(ox+a*s,oy+b*s,ox+c*s,oy+d*s,col,sw)
    return L(3,3,9,8)+L(4,14,14,2), h*TW/TH

def svg(w,h,body,extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.2f} {h:.2f}" role="img"{extra}>{body}</svg>\n')
def write(rel,content):
    p=os.path.join(ROOT,rel); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"w").write(content)

# ---- icons ----
def icon(rel,title,struct,acc,tile,box=CW,boxh=CH,fork=False,fill_h=0.46,Sz=256,rad=0.22,extra=""):
    h=Sz*fill_h; aw=h*box/boxh; x=(Sz-aw)/2; y=(Sz-h)/2
    art,_=(fork_art(x,y,h,struct) if fork else mark_art(x,y,h,struct,acc))
    t=f'<rect width="{Sz}" height="{Sz}" rx="{Sz*rad:.1f}" fill="{tile}"/>' if tile else ""
    write(rel, svg(Sz,Sz,f"<title>{title}</title>"+t+art,extra))

icon("svg/icon/ifuri-icon.svg","ifuri icon",WHITE,ACCENT_BRIGHT,INK if False else PRIMARY)
icon("svg/icon/ifuri-icon-light.svg","ifuri icon light",PRIMARY,ACCENT,PAPER)
icon("svg/icon/ifuri-icon-mono.svg","ifuri icon mono","currentColor","currentColor",None,extra=' fill="none" color="#1E1B4B"')
icon("svg/icon/ifuri-favicon.svg","ifuri favicon",WHITE,ACCENT_BRIGHT,PRIMARY,fill_h=0.50,Sz=64)
icon("svg/icon/ifuri-favicon-tiny.svg","ifuri favicon tiny",WHITE,WHITE,PRIMARY,box=TW,boxh=TH,fork=True,fill_h=0.58,Sz=64)
# bare mark tight
h=180; pad=h*0.12; art,aw=mark_art(pad,pad,h,PRIMARY,ACCENT)
write("svg/mark/ifuri-mark.svg", svg(aw+2*pad,h+2*pad,"<title>ifuri mark</title>"+art))
write("svg/mark/ifuri-mark-mono.svg", svg(aw+2*pad,h+2*pad,"<title>ifuri mark mono</title>"+mark_art(pad,pad,h,"currentColor","currentColor")[0], extra=' fill="none" color="#1E1B4B"'))

# ---- wordmark ----
WM=160
for nm,uri in [("svg/wordmark/ifuri-wordmark.svg",INK),("svg/wordmark/ifuri-wordmark-dark.svg",WHITE)]:
    l=layout(med,[("if",PRIMARY),("uri",uri)]); pad=10
    W=tw(l,WM)+2*pad; H=(ttop(l,WM)-tbot(l,WM))+2*pad
    write(nm, svg(W,H,"<title>ifuri</title>"+render_text(l,WM,pad,pad+ttop(l,WM))))

# ---- horizontal lockups ----
def horizontal(rel,uri,struct,acc,motto=False,mcol=None,bg=None):
    pad=34; l=layout(med,[("if",PRIMARY),("uri",uri)]); s=WM/1000; cap=697*s
    nw=tw(l,WM); ntop=ttop(l,WM); nbot=tbot(l,WM)
    mh=cap*1.16; maw=mh*CW/CH; gap=mh*0.46
    Yb=pad+ntop; mcy=Yb-cap/2; mtop=mcy-mh/2; mbot=mcy+mh/2
    sh=pad-min(pad,mtop); Yb+=sh; mtop+=sh; mbot+=sh
    tx=pad+maw+gap; art,_=mark_art(pad,mtop,mh,struct,acc)
    el=[art, render_text(l,WM,tx,Yb)]; bottom=max(Yb-nbot,mbot); W=tx+nw+pad
    if motto:
        ml=layout(reg,[(MOTTO,mcol)]); ms=WM*0.30; mb=Yb+ms*1.05
        el.append(render_text(ml,ms,tx+2,mb)); bottom=max(bottom,mb-tbot(ml,ms)); W=max(W,tx+tw(ml,ms)+pad)
    H=bottom+pad; pre=f'<rect width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>' if bg else ""
    write(rel, svg(W,H,"<title>ifuri</title>"+pre+"".join(el)))
horizontal("svg/lockup/ifuri-lockup-horizontal.svg",INK,PRIMARY,ACCENT)
horizontal("svg/lockup/ifuri-lockup-horizontal-dark.svg",WHITE,WHITE,ACCENT_BRIGHT,bg=INK)
horizontal("svg/lockup/ifuri-lockup-tagline.svg",INK,PRIMARY,ACCENT,motto=True,mcol=MUTED)
horizontal("svg/lockup/ifuri-lockup-tagline-dark.svg",WHITE,WHITE,ACCENT_BRIGHT,motto=True,mcol=MUTED_D,bg=INK)

# ---- stacked lockups ----
def stacked(rel,uri,struct,acc,mcol,bg=None,mono=False):
    pad=44; WMs=150; ifc=uri if mono else PRIMARY
    nl=layout(med,[("if",ifc),("uri",uri)]); cap=697*WMs/1000; nw=tw(nl,WMs)
    ml=layout(reg,[(MOTTO,mcol)]); ms=WMs*0.32; mw=tw(ml,ms)
    mh=cap*1.30; maw=mh*CW/CH; cw=max(maw,nw,mw); W=cw+2*pad; cx=W/2
    y=pad; art,_=mark_art(cx-maw/2,y,mh,struct,acc); y+=mh+mh*0.42
    nb=y+ttop(nl,WMs); ng=render_text(nl,WMs,cx-nw/2,nb); y=nb+ms*1.15
    mb=y+ttop(ml,ms); mg=render_text(ml,ms,cx-mw/2,mb); H=mb-tbot(ml,ms)+pad
    pre=f'<rect width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>' if bg else ""
    write(rel, svg(W,H,f"<title>ifuri — {MOTTO}</title>"+pre+art+ng+mg))
stacked("svg/lockup/ifuri-lockup-stacked.svg",INK,PRIMARY,ACCENT,MUTED)
stacked("svg/lockup/ifuri-lockup-stacked-dark.svg",WHITE,WHITE,ACCENT_BRIGHT,MUTED_D,bg=INK)
stacked("svg/lockup/ifuri-lockup-stacked-mono.svg",INK,INK,INK,MUTED,mono=True)

# ============================================================
#  COLOR TOKEN FILES
# ============================================================
def hex2rgb(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))
tokens={"ramps":RAMPS,"semantic":{k:C(r,s) for k,(r,s) in SEM.items()},
        "base":{"white":WHITE,"black":BLACK},"motto":MOTTO}
write("color/tokens.json", json.dumps(tokens,indent=2)+"\n")
# CSS
css=[":root {"]
for ramp,steps in RAMPS.items():
    for st,hx in steps.items(): css.append(f"  --ifuri-{ramp}-{st}: {hx};")
css.append("  --ifuri-white: #FFFFFF;")
for k,(r,s) in SEM.items(): css.append(f"  --ifuri-{k}: var(--ifuri-{r}-{s});")
css.append("}")
write("color/tokens.css","\n".join(css)+"\n")
# SCSS
scss=[]
for ramp,steps in RAMPS.items():
    for st,hx in steps.items(): scss.append(f"$ifuri-{ramp}-{st}: {hx};")
for k,(r,s) in SEM.items(): scss.append(f"$ifuri-{k}: ${'ifuri'}-{r}-{s};")
write("color/tokens.scss","\n".join(scss)+"\n")
# Tailwind
tw_obj={r:{st:hx for st,hx in steps.items()} for r,steps in RAMPS.items()}
write("color/tailwind.colors.js",
      "// Tailwind v3+: theme.extend.colors.ifuri\nmodule.exports = "+
      json.dumps({"ifuri":tw_obj},indent=2)+";\n")

# ---- palette swatch sheet (SVG + later PNG) ----
def swatch_sheet():
    cell_w, cell_h, gap, lab = 96, 64, 8, 34
    x0,y0 = 40, 56
    rows=list(RAMPS.items())
    width = x0 + 11*(cell_w+gap) + 40
    height = y0 + len(rows)*(cell_h+lab+24) + 120
    body=[f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>']
    body.append(f'<text x="40" y="34" font-family="ui-sans-serif,Arial" font-size="22" font-weight="600" fill="#1E1B4B">ifuri — colour system</text>')
    yy=y0
    for name,steps in rows:
        body.append(f'<text x="40" y="{yy-10}" font-family="ui-sans-serif,Arial" font-size="14" font-weight="600" fill="#1E1B4B">{name}</text>')
        xx=x0
        for st,hx in steps.items():
            r,g,b=hex2rgb(hx); lum=(0.299*r+0.587*g+0.114*b)
            tcol="#FFFFFF" if lum<150 else "#1E1B4B"
            body.append(f'<rect x="{xx}" y="{yy}" width="{cell_w}" height="{cell_h}" rx="8" fill="{hx}"/>')
            body.append(f'<text x="{xx+8}" y="{yy+22}" font-family="ui-monospace,monospace" font-size="12" fill="{tcol}">{st}</text>')
            body.append(f'<text x="{xx+8}" y="{yy+cell_h-10}" font-family="ui-monospace,monospace" font-size="11" fill="{tcol}">{hx}</text>')
            xx+=cell_w+gap
        yy+=cell_h+lab+24
    # semantic row
    body.append(f'<text x="40" y="{yy-10}" font-family="ui-sans-serif,Arial" font-size="14" font-weight="600" fill="#1E1B4B">semantic</text>')
    xx=x0
    for k,(r,s) in SEM.items():
        hx=C(r,s); rr,gg,bb=hex2rgb(hx); lum=(0.299*rr+0.587*gg+0.114*bb); tcol="#FFFFFF" if lum<150 else "#1E1B4B"
        body.append(f'<rect x="{xx}" y="{yy}" width="{cell_w+gap}" height="{cell_h}" rx="8" fill="{hx}"/>')
        short=k.replace("brand-","").replace("text-","")
        body.append(f'<text x="{xx+8}" y="{yy+20}" font-family="ui-monospace,monospace" font-size="10.5" fill="{tcol}">{short}</text>')
        body.append(f'<text x="{xx+8}" y="{yy+cell_h-10}" font-family="ui-monospace,monospace" font-size="11" fill="{tcol}">{hx}</text>')
        xx+=cell_w+gap+6
    write("color/palette.svg", svg(width,height,"<title>ifuri colour system</title>"+"".join(body)))
swatch_sheet()

print("svg+tokens generated")
