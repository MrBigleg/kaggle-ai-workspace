#!/usr/bin/env python3
"""
viz_okf.py — Render an OKF bundle as a single self-contained interactive HTML file.

A zero-dependency (Python stdlib + PyYAML) consumer of OKF, modelled on the
okf-viz / knowledge-catalog visualizers: a force-directed concept graph plus a
reader panel, embedded as one portable index.html (Cytoscape + marked via CDN).

Usage:
  python3 viz_okf.py --bundle okf/local-seo-gbp
  python3 viz_okf.py --bundle okf/local-seo-gbp --out okf/local-seo-gbp/viz.html --title "Local SEO & GBP"
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml --break-system-packages")

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)]+\.md)\)")

RESERVED = {"index.md", "log.md"}


def split_fm(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return (fm if isinstance(fm, dict) else {}), text[m.end():]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    bundle = Path(args.bundle).resolve()
    out = Path(args.out) if args.out else bundle / "viz.html"
    title = args.title or bundle.name

    nodes, edges = [], []
    ids = set()
    for p in sorted(bundle.rglob("*.md")):
        if p.name in RESERVED:
            continue
        cid = str(p.relative_to(bundle).with_suffix("")).replace("\\", "/")
        ids.add(cid)

    for p in sorted(bundle.rglob("*.md")):
        if p.name in RESERVED:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm, body = split_fm(text)
        cid = str(p.relative_to(bundle).with_suffix("")).replace("\\", "/")
        nodes.append({
            "id": cid,
            "title": fm.get("title", p.stem),
            "type": str(fm.get("type", "concept")),
            "description": fm.get("description", ""),
            "tags": fm.get("tags", []) or [],
            "group": cid.split("/")[0] if "/" in cid else "(root)",
            "body": body.strip(),
            "resource": fm.get("resource", ""),
        })
        for m in LINK_RE.finditer(body):
            tgt = m.group(1).lstrip("/")[:-3]  # drop leading / and .md
            if tgt in ids and tgt != cid:
                edges.append({"source": cid, "target": tgt})

    data = {"title": title, "nodes": nodes, "edges": edges}
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data))
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out}  ({len(nodes)} nodes, {len(edges)} edges)")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OKF Viewer</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root{--bg:#0f1115;--panel:#171a21;--ink:#e6e9ef;--muted:#9aa4b2;--accent:#4f8cff;--line:#2a2f3a;}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
#app{display:grid;grid-template-columns:280px 1fr 420px;height:100vh}
.col{height:100vh;overflow:auto;border-right:1px solid var(--line)}
header{padding:14px 16px;border-bottom:1px solid var(--line)}
header h1{font-size:15px;margin:0 0 8px}
input,select{width:100%;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px;margin-bottom:8px}
.nav a{display:block;padding:6px 16px;color:var(--ink);text-decoration:none;border-left:3px solid transparent;font-size:13px}
.nav a:hover{background:var(--panel)}.nav a.active{border-left-color:var(--accent);background:var(--panel)}
.grp{padding:10px 16px 4px;color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:.06em}
#cy{height:100vh;background:radial-gradient(circle at 50% 40%,#141821,#0f1115)}
#reader{padding:18px 22px}
#reader h2{margin:0 0 4px}.meta{color:var(--muted);font-size:12px;margin-bottom:12px}
.tag{display:inline-block;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:1px 8px;margin:2px 4px 2px 0;font-size:11px;color:var(--muted)}
#reader a{color:var(--accent)}#reader table{border-collapse:collapse;width:100%}#reader td,#reader th{border:1px solid var(--line);padding:6px}
#reader pre{background:#0b0d11;padding:12px;border-radius:8px;overflow:auto}
.backlinks{margin-top:18px;border-top:1px solid var(--line);padding-top:12px}
.count{color:var(--muted);font-size:12px}
</style></head>
<body><div id="app">
<div class="col"><header><h1 id="bt"></h1>
<input id="q" placeholder="Search title / id / tag">
<select id="tf"></select><div class="count" id="cnt"></div></header>
<div class="nav" id="nav"></div></div>
<div class="col" style="padding:0"><div id="cy"></div></div>
<div class="col"><div id="reader"><p class="count">Select a concept from the list or graph.</p></div></div>
</div>
<script>
const DATA=__DATA__;
document.getElementById('bt').textContent=DATA.title;
document.title=DATA.title+" — OKF";
const byId={};DATA.nodes.forEach(n=>byId[n.id]=n);
const backlinks={};DATA.edges.forEach(e=>{(backlinks[e.target]=backlinks[e.target]||[]).push(e.source)});
const types=[...new Set(DATA.nodes.map(n=>n.type))].sort();
const palette=['#4f8cff','#48c78e','#ffb020','#f06595','#a78bfa','#22d3ee','#fb923c','#94a3b8'];
const colorOf={};types.forEach((t,i)=>colorOf[t]=palette[i%palette.length]);
const tf=document.getElementById('tf');tf.innerHTML='<option value="">All types ('+DATA.nodes.length+')</option>'+types.map(t=>`<option value="${t}">${t}</option>`).join('');

const cy=cytoscape({container:document.getElementById('cy'),
 elements:[...DATA.nodes.map(n=>({data:{id:n.id,label:n.title,type:n.type}})),
           ...DATA.edges.map(e=>({data:{source:e.source,target:e.target}}))],
 style:[{selector:'node',style:{'background-color':e=>colorOf[e.data('type')]||'#94a3b8','label':'data(label)','color':'#cfd6e2','font-size':7,'text-wrap':'wrap','text-max-width':80,'width':12,'height':12}},
        {selector:'edge',style:{'width':0.6,'line-color':'#39414f','target-arrow-color':'#39414f','target-arrow-shape':'triangle','arrow-scale':0.5,'curve-style':'bezier','opacity':0.5}},
        {selector:'.sel',style:{'background-color':'#fff','width':18,'height':18,'font-size':9,'color':'#fff','z-index':99}},
        {selector:'.dim',style:{'opacity':0.12}}],
 layout:{name:'cose',animate:false,nodeRepulsion:9000,idealEdgeLength:60}});

function render(id){const n=byId[id];if(!n)return;
 const r=document.getElementById('reader');
 const tags=(n.tags||[]).map(t=>`<span class="tag">${t}</span>`).join('');
 const bl=(backlinks[id]||[]);
 const blhtml=bl.length?`<div class="backlinks"><div class="grp">Cited by (${bl.length})</div>`+bl.map(s=>`<a href="#" data-id="${s}">${(byId[s]||{}).title||s}</a>`).join('')+`</div>`:'';
 let body=marked.parse(n.body||'');
 r.innerHTML=`<h2>${n.title}</h2><div class="meta">${n.type} · <code>${id}</code></div>${tags?('<div>'+tags+'</div>'):''}${n.resource?`<p><a href="${n.resource}" target="_blank">↗ resource</a></p>`:''}<hr style="border-color:var(--line)">${body}${blhtml}`;
 r.querySelectorAll('a[data-id]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id)}));
 r.querySelectorAll('a[href^="/"]').forEach(a=>{const t=a.getAttribute('href').replace(/^\//,'').replace(/\.md$/,'');if(byId[t]){a.addEventListener('click',ev=>{ev.preventDefault();select(t)})}});
}
function select(id){cy.elements().removeClass('sel dim');const node=cy.$id(id);if(node){node.addClass('sel');const nb=node.closedNeighborhood();cy.elements().not(nb).addClass('dim');cy.animate({center:{eles:node},zoom:1.2},{duration:300});}
 document.querySelectorAll('.nav a').forEach(a=>a.classList.toggle('active',a.dataset.id===id));render(id);}
cy.on('tap','node',e=>select(e.target.id()));

const nav=document.getElementById('nav');
function buildNav(){const q=document.getElementById('q').value.toLowerCase();const tfv=tf.value;
 const groups={};DATA.nodes.forEach(n=>{
   if(tfv&&n.type!==tfv)return;
   const hay=(n.title+' '+n.id+' '+(n.tags||[]).join(' ')).toLowerCase();
   if(q&&!hay.includes(q))return;
   (groups[n.group]=groups[n.group]||[]).push(n);});
 let html='';let shown=0;Object.keys(groups).sort().forEach(g=>{html+=`<div class="grp">${g}</div>`;groups[g].sort((a,b)=>a.title.localeCompare(b.title)).forEach(n=>{shown++;html+=`<a href="#" data-id="${n.id}">${n.title}</a>`})});
 nav.innerHTML=html;document.getElementById('cnt').textContent=shown+' of '+DATA.nodes.length+' concepts';
 nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id)}));}
document.getElementById('q').addEventListener('input',buildNav);tf.addEventListener('change',buildNav);buildNav();
</script></body></html>"""

if __name__ == "__main__":
    main()
