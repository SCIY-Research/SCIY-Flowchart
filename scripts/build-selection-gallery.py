#!/usr/bin/env python3
"""Build self-contained (except reference image URLs) dual chooser for layout + color."""
import html
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT/'references/structure-reference-manifest.json').read_text(encoding='utf-8'))
colors = json.loads((ROOT/'references/color-palettes.json').read_text(encoding='utf-8'))
es = lambda x: html.escape(str(x), quote=True)
blocks = []
for family in range(1, 9):
    subset = [a for a in items if int(a['family']) == family]
    if len(subset) != 4:
        raise ValueError(f'Family {family} has {len(subset)} references, expected 4')
    cards = []
    slug = ['academic-classic','academic-modular','technical-architecture','timeline-stage','swimlane','cycle-feedback','network-concept','illustrated-workflow'][family-1]
    fallback = f'examples/style-gallery/sciy-ai/{family:02d}-{slug}.png'
    for a in subset:
        aid = a['id']
        cards.append(f'''<article class="ref"><img loading="lazy" src="{es(a['image_url'])}" data-fallback="{es(fallback)}" alt="{es(a['title'])}" onerror="this.onerror=null;this.src=this.dataset.fallback;this.title='原参考图加载失败，显示SCIY备用示意图';this.closest('article').querySelector('.offline').hidden=false;"><small class="offline" hidden>网络图片未加载，已切换 SCIY 备用示意图（非原论文图）</small><b>{es(aid)} · {es(a['title'])}</b><small>{es(a['structure_note'])}</small><div class="actions"><button type="button" onclick="chooseStructure('{es(aid)}',this)">选这个结构参考</button> <a href="{es(a['source_url'])}" target="_blank" rel="noreferrer">来源/许可</a></div></article>''')
    blocks.append(f'''<details><summary>{family:02d}｜{es(subset[0]['family_zh'])}<small>{es(subset[0]['family_en'])}</small></summary><div class="refs">{''.join(cards)}</div></details>''')
pals=[]
for p in colors:
    swatches=''.join(f'<div style="background:{es(c)}" title="{es(c)}"></div>' for c in p['colors'])
    pals.append(f'''<div class="palette" data-key="{es(p['id'])}"><button type="button" onclick="chooseColor('{es(p['id'])}',this)"><b>{es(p['id'])} · {es(p['name'])}</b><span class="swatches">{swatches}</span></button></div>''')
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SCIY | 结构与配色联合选择</title><style>
*{{box-sizing:border-box}}body{{font:15px/1.5 Arial,"Microsoft YaHei","Noto Sans CJK SC",sans-serif;margin:0;background:#f3f6fa;color:#263646}}a{{color:#346393}}.top{{padding:20px 24px;background:white;border-bottom:1px solid #dce5ee;position:sticky;top:0;z-index:2;box-shadow:0 3px 10px #20354b10}}h1{{font-size:22px;margin:0 0 7px}}.intro{{margin:4px 0;color:#5b6674}}.selected{{display:flex;align-items:center;gap:12px;flex-wrap:wrap}}#selected{{font-size:15px;font-weight:bold;max-width:100%;min-width:260px;background:#eff4fa;border:1px solid #cad7e8;padding:9px;border-radius:6px;flex:1}}button{{cursor:pointer;border:1px solid #b7c7d9;background:white;color:#20354b;border-radius:8px;padding:8px 11px;font:inherit}}button:hover{{background:#e9f1fa}}button.active{{background:#315d87;color:white}}.body{{display:grid;grid-template-columns: minmax(0,2fr) minmax(300px,1fr);gap:18px;max-width:1600px;margin:auto;padding:18px}}section{{min-width:0}}.panel{{background:white;border:1px solid #dce5ee;border-radius:14px;padding:16px}}h2{{margin:0 0 8px;font-size:19px}}details{{border:1px solid #d9e1eb;margin:12px 0;border-radius:9px;overflow:hidden}}summary{{background:#f7f9fc;padding:12px;cursor:pointer;font-weight:bold}}summary small{{display:block;font-weight:normal;color:#707e8c}}.refs{{padding:12px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}.ref{{border:1px solid #e2e7ed;padding:10px;border-radius:10px}}.ref img{{width:100%;height:215px;object-fit:contain;background:white;border:1px solid #eef2f6}}.ref b,.ref small{{display:block;margin-top:7px}}.ref small{{color:#647181}}.actions{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:8px}}.palette{{margin:9px 0}}.palette button{{width:100%;text-align:left;padding:9px}}.palette b{{font-size:13px}}.swatches{{display:flex;overflow:hidden;border-radius:6px;height:27px;margin-top:5px}}.swatches div{{flex:1}}.rights{{font-size:12px;color:#697788;line-height:1.7}}@media(max-width:1000px){{.body{{display:block}}.panel{{margin-bottom:20px}}.refs{{grid-template-columns:1fr}}.top{{position:static}}}}</style></head><body>
<div class="top"><h1>SCIY Flowchart · 同时选择结构和配色</h1><p class="intro">结构只参考信息组织与布局逻辑；配色独立决定。二者选一次即可，不需要分两轮问。</p><div class="selected"><input id="selected" value="结构：AI自动选择；配色：默认学术配色" readonly aria-label="本次选择结果"><button onclick="copySelection()">复制选择结果</button></div></div>
<div class="body"><section class="panel"><h2>① 结构参考 · 8 类 × 4 张</h2><button onclick="chooseStructure('AI自动选择',this)">由 AI 推荐结构（默认）</button><p class="intro">展开任一分类选 01-A 至 08-D，也可以仅回复 01～08，AI 从该类的 4 张中选择构图思路。</p>{''.join(blocks)}</section><section class="panel"><h2>② 科研配色 · 同时选择</h2><button onclick="chooseColor('默认学术配色',this)">默认学术配色（推荐）</button>{''.join(pals)}<p class="intro">也可以直接回复：<b>自定义 #176B87 + 灰色</b>、<b>低饱和蓝绿</b>、<b>参考我上传的配色图</b>。</p><p class="rights">色板名称含 inspired 的仅表示取自公开科学绘图风格的启发，不意味着期刊官方指定。图片均为远程结构参考，可能需要联网；加载失败时备用图来自 SCIY，不冒称原图。查看原文、作者及具体 Figure 信用说明，请点击每张图下方来源。署名不是全部使用权限，商业分发仍以原许可及第三方授权为准。最终作品须独立绘制，不复制原图文本、图标和具体版式。</p><p class="intro"><a href="STYLE-GALLERY.html">查看独立结构图库</a>　<a href="COLOR-GALLERY.html">查看独立配色图库</a></p></section></div>
<script>
let structure='AI自动选择', color='默认学术配色';
function chooseStructure(v,btn){{structure=v;document.querySelectorAll('.ref .active').forEach(x=>x.classList.remove('active'));if(btn)btn.classList.add('active');update()}}
function chooseColor(v,btn){{color=v;document.querySelectorAll('.palette .active').forEach(x=>x.classList.remove('active'));if(btn)btn.classList.add('active');update()}}
function update(){{document.getElementById('selected').value='结构：'+structure+'；配色：'+color}}
function copySelection(){{const el=document.getElementById('selected');el.select();if(navigator.clipboard && window.isSecureContext){{navigator.clipboard.writeText(el.value).catch(()=>document.execCommand('copy'))}}else{{document.execCommand('copy')}}}}
</script></body></html>'''
out=ROOT/'SELECTION-GALLERY.html'
out.write_text(page,encoding='utf-8')
print(out, len(blocks), len(pals), len(page))
