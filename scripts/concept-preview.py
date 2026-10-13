#!/usr/bin/env python3
"""Deterministic, offline preview fallback for failed/unavailable image generation.

Usage:
 python scripts/concept-preview.py examples/sample-diagram.json /tmp/sc-concepts --count 4
Creates actual SVG previews, candidate JSONs and an offline click-open HTML index.
Do not misrepresent these as AI-generated bitmap images.
"""
import argparse
import copy
import json
import math
import sys
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location('sciy_renderer', ROOT / 'scripts' / 'render-svg.py')
module = module_from_spec(spec)
spec.loader.exec_module(module)

NAMES = [
 ('A', '横向层级 / Horizontal stages'),
 ('B', '纵向层级 / Vertical stages'),
 ('C', '双列阶段 / Two-column stages'),
 ('D', '宽松交错 / Spacious alternating'),
]


def levels(doc):
    """Main-direction DAG layer assignment. Explicit feedback edges are excluded.

    If unexpected cycles exist, keep unplaced nodes in their original order.
    """
    nodes = doc.get('nodes', [])
    ids = [n['id'] for n in nodes]
    indegree = {k: 0 for k in ids}
    outgoing = {k: [] for k in ids}
    for e in doc.get('edges', []):
        a, b = e.get('from'), e.get('to')
        if a in indegree and b in indegree and a != b and e.get('kind') != 'feedback':
            outgoing[a].append(b)
            indegree[b] += 1
    ready = [k for k in ids if indegree[k] == 0]
    topo, depths = [], {k: 0 for k in ids}
    while ready:
        a = ready.pop(0)
        topo.append(a)
        for b in outgoing[a]:
            depths[b] = max(depths[b], depths[a] + 1)
            indegree[b] -= 1
            if indegree[b] == 0:
                ready.append(b)
    # Graceful cycle handling: don't make up new arcs or hang.
    remaining = [k for k in ids if k not in topo]
    for k in remaining:
        depths[k] = max(depths.values(), default=0) + 1
    layers = {}
    indexed = {n['id']: n for n in nodes}
    for nid in ids:
        layers.setdefault(depths[nid], []).append(indexed[nid])
    return [layers[k] for k in sorted(layers)]


def layout(doc, index):
    d = copy.deepcopy(doc)
    d['groups'] = []  # group boxes are redrawn during formal reconstruction
    layers = levels(d)
    count = len(d.get('nodes', []))
    if not count:
        raise ValueError('No nodes found: supply node/edge JSON before preview fallback')
    maxrow = max(len(layer) for layer in layers)
    L = len(layers)
    width = 1500
    height = max(820, 190 + max(count if index in [1,2] else maxrow, 3) * 115)
    d['canvas'] = {'width': width, 'height': height, 'background': '#FFFFFF'}
    d.setdefault('meta', {})['title'] = f"{doc.get('meta', {}).get('title', 'Workflow')} · Concept {NAMES[index][0]}"
    d['meta']['id'] = 'concept-' + NAMES[index][0]
    # Distinct geometries: horizontal; vertical; two-column column-major; alternating spaced columns.
    if index == 0:
        step_x = (width - 260) / max(L, 1)
        for c, layer in enumerate(layers):
            xs = 115 + c * step_x
            for j, node in enumerate(layer):
                w, h = min(190, max(120, step_x - 45)), 82
                ys = 155 + (j + 0.5) * (height - 320) / max(len(layer), 1) - h/2
                node.update(x=xs, y=ys, w=w, h=h)
    elif index == 1:
        total = count
        order = [n for layer in layers for n in layer]
        for i, node in enumerate(order):
            w, h = 480, 80
            y = 145 + i * 116
            node.update(x=(width - w)/2, y=y, w=w, h=h)
        d['canvas']['height'] = max(640, 245 + total * 116)
    elif index == 2:
        order = [n for layer in layers for n in layer]
        rows = math.ceil(len(order)/2)
        for i, node in enumerate(order):
            col = i % 2
            row = i // 2
            node.update(x=260 + col * 640, y=140 + row * 146, w=350, h=86)
        d['canvas']['height'] = max(640, rows * 146 + 255)
    else:
        step_x = (width - 275) / max(L, 1)
        for col, layer in enumerate(layers):
            for j, node in enumerate(layer):
                w, h = min(220, max(125, step_x - 32)), 92
                x = 110 + col * step_x
                y = 170 + (j+0.5) * (height - 320)/max(len(layer), 1) - h/2
                if (col + j) % 2: y += 34
                node.update(x=x, y=y, w=w, h=h)
    # Source waypoints were tied to old coordinates. Recompute feedback detours.
    lookup = {n['id']: n for n in d['nodes']}
    for edge in d.get('edges', []):
        edge.pop('points', None)
        if edge.get('kind') == 'feedback' and edge.get('from') in lookup and edge.get('to') in lookup:
            a, b = lookup[edge['from']], lookup[edge['to']]
            if index in (0, 3):
                y = max(75, min(a['y'], b['y']) - 80)
                edge['points'] = [[a['x'] + a['w']/2, a['y']], [a['x'] + a['w']/2, y], [b['x'] + b['w']/2, y], [b['x'] + b['w']/2, b['y']]]
            else:
                x = max(45, min(a['x'], b['x']) - 95)
                edge['points'] = [[a['x'], a['y'] + a['h']/2], [x, a['y'] + a['h']/2], [x, b['y'] + b['h']/2], [b['x'], b['y'] + b['h']/2]]
    # Edges preserve original semantics, never invented or removed.
    return d


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('outdir')
    parser.add_argument('--count', type=int, default=4, choices=(1,4))
    args = parser.parse_args()
    doc = json.loads(Path(args.input).read_text(encoding='utf-8'))
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    cards = []
    for i in range(args.count):
        label, title = NAMES[i]
        model = layout(doc, i)
        jp = out / f'concept-{label}.json'
        sp = out / f'concept-{label}.svg'
        jp.write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding='utf-8')
        module.render(model, sp)
        cards.append(f'<article><h2>{escape(title)}</h2><object data="{sp.name}" type="image/svg+xml"></object><p><a href="{sp.name}">打开矢量预览</a> · <a href="{jp.name}">查看模型</a></p></article>')
    content = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SCIY 离线方案预览</title><style>body{font-family:Arial,"Microsoft YaHei",sans-serif;background:#f5f7fa;color:#26374b;margin:0;padding:24px}header,article{background:white;border:1px solid #dce3eb;padding:18px;border-radius:12px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:16px;margin-top:16px}object{width:100%;height:400px;border:1px solid #e4e9ee}h2{font-size:18px}a{color:#315d87}</style></head><body><header><h1>SCIY · 本地矢量方案预览</h1><p>图片生成暂不可用时的离线后备方案，不是 AI 生图。预览仅用于构图选择，最终绘制会重新布局与检查。</p></header><main>'+''.join(cards)+'</main></body></html>'
    (out / 'PREVIEW-INDEX.html').write_text(content, encoding='utf-8')
    print(out / 'PREVIEW-INDEX.html')
    print(f'OK: {len(cards)} offline preview concepts')

if __name__ == '__main__':
    main()
