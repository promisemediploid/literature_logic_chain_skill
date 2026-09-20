#!/usr/bin/env python3
"""Generate a self-contained, content-first Literature Logic Chain HTML page."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

VALID_STAGES = {
    "problem", "gap", "hypothesis", "data", "model", "training",
    "downstream", "evidence", "limitation"
}

STAGE_LABELS = {
    "problem": "问题",
    "gap": "为什么原来的方法不够",
    "hypothesis": "关键想法",
    "data": "数据与处理",
    "model": "模型与组件",
    "training": "训练目标",
    "downstream": "最终怎么使用",
    "evidence": "实验与证据",
    "limitation": "局限与未证明事项",
}


def validate(data: dict) -> None:
    required = {"title", "opening_explanation", "prerequisites", "nodes", "edges", "experiments", "limitations"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Missing top-level fields: {sorted(missing)}")

    ids = []
    for node in data["nodes"]:
        for key in ("id", "stage", "title", "explanation", "why", "function", "if_omitted", "evidence"):
            if key not in node:
                raise ValueError(f"Node {node.get('id', '<unknown>')} missing field: {key}")
        if node["stage"] not in VALID_STAGES:
            raise ValueError(f"Invalid stage for {node['id']}: {node['stage']}")
        ids.append(node["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate node ids found")

    idset = set(ids)
    for edge in data["edges"]:
        if edge.get("from") not in idset or edge.get("to") not in idset:
            raise ValueError(f"Edge references missing node: {edge}")


def norm_prereqs(prereqs):
    """Accept either compact dict form or legacy list form."""
    if isinstance(prereqs, dict):
        out = {"required": [], "recommended": [], "nice_to_know": []}
        for key in out:
            vals = prereqs.get(key, []) or []
            out[key] = [str(v) for v in vals]
        return out
    out = {"required": [], "recommended": [], "nice_to_know": []}
    for p in prereqs or []:
        level = p.get("level", "recommended")
        out.setdefault(level, []).append(p.get("title", ""))
    return out


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def generate(data: dict) -> str:
    validate(data)
    prereq = norm_prereqs(data["prerequisites"])
    safe_json = jdump(data).replace("</script", "<\\/script")
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
<title>{html.escape(data['title'])} · Literature Logic Chain</title>
<style>
:root{{--bg:#f5f9ff;--panel:#fff;--ink:#0f172a;--muted:#64748b;--line:#d9e7f7;--blue:#2563eb;--blue2:#0ea5e9;--cyan:#06b6d4;--soft:#eef6ff;--soft2:#ecfeff;--shadow:0 10px 28px rgba(37,99,235,.08)}}
*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(180deg,#eff6ff 0,#f9fcff 56%,#eef9ff 100%);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",\"Microsoft YaHei\",sans-serif;line-height:1.75}}
.header{{position:sticky;top:0;z-index:20;background:rgba(245,249,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding:22px 28px}}
.badge{{display:inline-flex;align-items:center;padding:4px 9px;border-radius:999px;background:#dbeafe;color:#1d4ed8;font-size:11px;font-weight:800;letter-spacing:.05em}}
h1{{margin:10px 0 4px;font-size:28px;line-height:1.2}}.subtitle{{margin:0;color:var(--muted);max-width:1100px;font-size:13px}}
.toolbar{{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}}.toolbar input{{flex:1 1 280px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;outline:none}}.toolbar input:focus{{border-color:#93c5fd;box-shadow:0 0 0 3px #dbeafe}}button{{font:inherit}}
.btn{{border:1px solid var(--line);background:#fff;color:#334155;border-radius:999px;padding:7px 11px;font-size:12px;cursor:pointer}}.btn.active{{background:#dbeafe;border-color:#93c5fd;color:#1d4ed8;font-weight:700}}
.wrap{{max-width:1380px;margin:22px auto;padding:0 20px 46px}}
.panel{{background:rgba(255,255,255,.9);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow)}}
.opening{{padding:24px 26px;margin-bottom:15px;background:linear-gradient(135deg,#eff6ff,#ecfeff)}}.opening h2,.section h2{{margin:0 0 9px;font-size:19px}}.opening p{{margin:0;color:#334155;font-size:15px;line-height:2}}
.prereq{{padding:16px 20px;margin-bottom:18px}}.prereq-head{{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap}}.prereq-note{{font-size:12px;color:var(--muted)}}.prereq-row{{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:10px}}.prereq-group{{display:flex;align-items:center;gap:7px;flex-wrap:wrap}}.prereq-label{{font-size:11px;font-weight:800;color:#1d4ed8}}.term{{display:inline-flex;align-items:center;padding:4px 8px;border-radius:999px;background:#f8fbff;border:1px solid #dbeafe;color:#334155;font-size:11px;cursor:pointer}}.term:hover,.term.active{{background:#dbeafe;border-color:#93c5fd;color:#1d4ed8}}
.grid{{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px;align-items:start}}.content{{padding:24px}}.nav{{position:sticky;top:140px;padding:18px}}.nav h3{{margin:0 0 10px;font-size:15px}}.nav-list{{display:flex;flex-direction:column;gap:7px}}.nav-item{{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 10px;font-size:11px;color:#475569;text-align:left;cursor:pointer}}.nav-item:hover,.nav-item.active{{border-color:#93c5fd;background:#eff6ff;color:#1d4ed8}}
.node{{position:relative;padding:22px 22px 24px 24px;border-left:4px solid #93c5fd;margin-bottom:14px;background:#fff;border-radius:0 14px 14px 0;box-shadow:0 6px 18px rgba(15,23,42,.04);transition:.16s ease}}.node:hover{{box-shadow:0 9px 24px rgba(15,23,42,.07)}}.node.dim{{opacity:.24}}.node.active{{border-left-color:var(--blue);box-shadow:0 0 0 3px #dbeafe}}.node.hidden{{display:none}}
.kicker{{font-size:11px;color:#2563eb;font-weight:800;letter-spacing:.04em}}.node h3{{margin:5px 0 10px;font-size:18px;line-height:1.45}}.explanation{{margin:0 0 14px;color:#334155;font-size:14px;line-height:1.95}}
.explain-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.box{{border:1px solid #e4edf8;border-radius:11px;padding:12px;background:#f8fbff}}.box h4{{margin:0 0 5px;font-size:11px;color:#1d4ed8}}.box p{{margin:0;color:#475569;font-size:12px;line-height:1.75}}
.evidence{{margin-top:12px;padding-top:12px;border-top:1px solid #edf2f7}}.evidence h4{{margin:0 0 5px;font-size:11px;color:#1d4ed8}}.evidence ul{{margin:0;padding-left:18px}}.evidence li{{font-size:12px;color:#475569;margin:2px 0}}
.experiment{{border:1px solid var(--line);border-radius:12px;padding:12px;margin-top:10px;background:#fff}}.experiment strong{{color:#1d4ed8;font-size:12px}}.experiment p{{margin:5px 0 0;font-size:12px;color:#475569;line-height:1.7}}
footer{{margin-top:18px;color:var(--muted);font-size:11px;text-align:center}}
@media(max-width:980px){{.grid{{grid-template-columns:1fr}}.nav{{position:relative;top:auto}}}}@media(max-width:650px){{.wrap{{padding:0 12px 32px}}.header{{padding:18px 15px}}.opening,.content{{padding:18px}}.explain-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class=\"header\">
  <span class=\"badge\">LITERATURE LOGIC CHAIN</span>
  <h1>{html.escape(data['title'])}</h1>
  <p class=\"subtitle\">{html.escape(data.get('subtitle','按人类认知顺序理解整篇论文'))}</p>
  <div class=\"toolbar\">
    <input id=\"search\" placeholder=\"搜索术语、模型、数据、实验……\" />
    <div id=\"stageButtons\"></div>
    <button class=\"btn\" id=\"reset\">重置</button>
  </div>
</header>
<main class=\"wrap\">
  <section class=\"panel opening\">
    <h2>先用一段完整的话把整篇论文讲懂</h2>
    <p id=\"opening\"></p>
  </section>
  <section class=\"panel prereq\">
    <div class=\"prereq-head\"><h2 style=\"margin:0;font-size:16px\">阅读前置知识</h2><span class=\"prereq-note\">这里只列词条；正文会在首次出现时解释必要概念。</span></div>
    <div id=\"prereqs\"></div>
  </section>
  <div class=\"grid\">
    <section class=\"panel content\" id=\"content\">
      <div class=\"section\"><h2>完整逻辑链：按人类理解顺序阅读</h2></div>
      <div id=\"nodes\"></div>
      <section class=\"section\" style=\"margin-top:24px\"><h2>实验：作者到底在验证前面的哪一句话？</h2><div id=\"experiments\"></div></section>
      <section class=\"section\" style=\"margin-top:24px\"><h2>论文真正证明了什么？没有证明什么？</h2><div id=\"limits\"></div></section>
    </section>
    <aside class=\"panel nav\">
      <h3>阅读导航</h3>
      <div class=\"nav-list\" id=\"nav\"></div>
    </aside>
  </div>
  <footer>本页面内容来自输入论文与结构化阅读结果；可视化只服务于阅读，不替代正文解释。</footer>
</main>
<script>
const DATA={safe_json};
const LABELS={json.dumps(STAGE_LABELS,ensure_ascii=False)};
const root=document.getElementById('nodes'), nav=document.getElementById('nav'), search=document.getElementById('search');
const nodeMap=new Map((DATA.nodes||[]).map(n=>[n.id,n]));
function esc(v){{const d=document.createElement('div');d.textContent=v??'';return d.innerHTML}}
function renderOpening(){{document.getElementById('opening').textContent=DATA.opening_explanation||DATA.summary||''}}
function renderPrereqs(){{
  const box=document.getElementById('prereqs'); const groups=[['required','必须知道'],['recommended','建议知道'],['nice_to_know','知道名字即可']]; box.innerHTML='';
  const p=DATA.prerequisites||{{}};
  groups.forEach(([k,label])=>{{const arr=(Array.isArray(p)?p.filter(x=>x.level===k).map(x=>x.title):(p[k]||[])); if(!arr.length)return; const row=document.createElement('div');row.className='prereq-group'; row.innerHTML=`<span class=\"prereq-label\">${{label}}</span>`; arr.forEach((t,i)=>{{const b=document.createElement('button');b.className='term';b.textContent=t;b.dataset.term=t.toLowerCase();b.onclick=()=>highlightTerm(t);row.appendChild(b)}});box.appendChild(row)}})
}}
function highlightTerm(term){{
  const q=term.toLowerCase(); document.querySelectorAll('.term').forEach(x=>x.classList.toggle('active',x.textContent.toLowerCase()===q));
  const hits=(DATA.nodes||[]).filter(n=>[n.title,n.explanation,n.why,n.function,n.if_omitted,(n.evidence||[]).join(' ')].join(' ').toLowerCase().includes(q));
  const ids=new Set(hits.map(n=>n.id));document.querySelectorAll('.node').forEach(x=>{{x.classList.toggle('dim',!ids.has(x.dataset.id));x.classList.toggle('active',ids.has(x.dataset.id))}});
}}
function renderNodes(){{
  root.innerHTML='';nav.innerHTML='';
  (DATA.nodes||[]).forEach((n,i)=>{{
    const el=document.createElement('article');el.className='node';el.id='node-'+n.id;el.dataset.id=n.id;el.dataset.stage=n.stage;
    el.dataset.search=[n.title,n.explanation,n.why,n.function,n.if_omitted,(n.evidence||[]).join(' ')].join(' ').toLowerCase();
    el.innerHTML=`<div class=\"kicker\">第 ${{i+1}} 步 · ${{esc(LABELS[n.stage]||n.stage)}}</div><h3>${{esc(n.title)}}</h3><p class=\"explanation\">${{esc(n.explanation)}}</p><div class=\"explain-grid\"><div class=\"box\"><h4>为什么必须走到这一步？</h4><p>${{esc(n.why)}}</p></div><div class=\"box\"><h4>这一步到底在做什么？</h4><p>${{esc(n.function)}}</p></div><div class=\"box\"><h4>如果不这样做，最容易出现什么问题？</h4><p>${{esc(n.if_omitted)}}</p></div><div class=\"box\"><h4>论文给了什么证据？</h4><p>${{esc((n.evidence||[]).join('；')||'当前节点没有单独记录的证据。')}}</p></div></div>`;
    root.appendChild(el);
    const b=document.createElement('button');b.className='nav-item';b.textContent=`${{i+1}}. ${{n.title}}`;b.dataset.id=n.id;b.onclick=()=>go(n.id);nav.appendChild(b);
  }})
}}
function go(id){{document.querySelectorAll('.node').forEach(x=>x.classList.remove('active','dim'));document.querySelectorAll('.nav-item').forEach(x=>x.classList.toggle('active',x.dataset.id===id));const el=document.getElementById('node-'+id);if(el){{el.classList.add('active');el.scrollIntoView({{behavior:'smooth',block:'center'}})}}}}
function renderExperiments(){{const box=document.getElementById('experiments');box.innerHTML='';(DATA.experiments||[]).forEach(e=>{{const d=document.createElement('div');d.className='experiment';d.innerHTML=`<strong>${{esc(e.claim||'实验要验证的说法')}}</strong><p><b>实验：</b>${{esc(e.method||'')}}</p><p><b>作用：</b>这个实验要检查前面的哪一个假设，以及结果能够支持到什么程度。</p>`;d.onclick=()=>((e.supports||[])[0]&&go((e.supports||[])[0]));box.appendChild(d)}})}}
function renderLimits(){{const box=document.getElementById('limits');box.innerHTML=(DATA.limitations||[]).map(x=>`<div class=\"experiment\"><p style=\"margin:0\">${{esc(x)}}</p></div>`).join('')||'<p style="color:#64748b">当前没有单独提供 limitation 数据。</p>'}}
function renderStageButtons(){{const box=document.getElementById('stageButtons');box.innerHTML='';Object.entries(LABELS).forEach(([k,v])=>{{const b=document.createElement('button');b.className='btn';b.textContent=v;b.dataset.stage=k;b.onclick=()=>{{const on=b.classList.toggle('active');document.querySelectorAll('[data-stage]').forEach(x=>{{if(x.classList.contains('node'))x.classList.toggle('hidden',on&&x.dataset.stage!==k)}})}};box.appendChild(b)}})}}
search.addEventListener('input',()=>{{const q=search.value.trim().toLowerCase();document.querySelectorAll('.node').forEach(n=>n.classList.toggle('hidden',!!q&&!n.dataset.search.includes(q)))}});
document.getElementById('reset').onclick=()=>{{search.value='';document.querySelectorAll('.btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.node').forEach(n=>n.classList.remove('hidden','active','dim'));document.querySelectorAll('.term').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));}};
renderOpening();renderPrereqs();renderNodes();renderExperiments();renderLimits();renderStageButtons();
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_json")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(generate(data), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
