#!/usr/bin/env python3
import argparse
import html
import json
import math
import os
import re
from pathlib import Path

from palette_utils import flow_colors, palette_colors, mix_white, canonical
from layout_utils import wrap_text, route_edge

ROOT = Path(__file__).resolve().parents[1]


def load_styles():
    styles = {}
    style_root = ROOT / "styles"
    if style_root.exists():
        for tokens in style_root.glob("*/tokens.json"):
            try:
                data = json.loads(tokens.read_text(encoding="utf-8"))
                key = data.get("style_id")
                palette = data.get("palette")
                if key and isinstance(palette, dict):
                    styles[key] = palette
            except Exception:
                pass
    # Backward-compatible aliases from v0.1
    aliases = {
        "academic-minimal": "academic-classic",
        "academic-blue": "technical-architecture",
        "academic-module": "academic-modular",
        "presentation-clean": "academic-classic",
    }
    for old, new in aliases.items():
        if new in styles:
            styles[old] = styles[new]
    if not styles:
        styles["academic-classic"] = {
            "bg": "#ffffff", "group_fill": "#ffffff", "group_stroke": "#b8b8b8",
            "node_fill": "#ffffff", "node_stroke": "#202020", "strong_fill": "#f0f0f0",
            "muted_fill": "#fafafa", "text": "#111111", "secondary": "#666666",
            "main": "#222222", "feedback": "#555555", "constraint": "#777777"
        }
    return styles


STYLES = load_styles()


def slug(s):
    s = re.sub(r"[^A-Za-z0-9_-]+", "-", s or "diagram").strip("-")
    return s or "diagram"


def esc(s):
    return html.escape(str(s), quote=True)


def render(doc, out_path, style_override=None):
    canvas = doc.get("canvas", {})
    width = float(canvas.get("width", 1600))
    height = float(canvas.get("height", 900))
    meta = doc.get("meta", {})
    style_name = style_override or meta.get("style", "academic-classic")
    style = flow_colors(doc, STYLES.get(style_name, STYLES.get("academic-classic", next(iter(STYLES.values())))))
    bg = canvas.get("background", style["bg"])
    typo = doc.get("typography", {})
    en_font = typo.get("english_font", "Times New Roman")
    zh_font = typo.get("chinese_font", "Source Han Sans SC")
    node_pt = float(typo.get("node_pt", 12))
    group_pt = float(typo.get("group_pt", 13))
    title_pt = float(typo.get("title_pt", 15))
    # SVG px approximation at 96 dpi
    node_px = node_pt * 96 / 72
    group_px = group_pt * 96 / 72
    title_px = title_pt * 96 / 72
    diagram_id = slug(meta.get("id") or Path(out_path).stem)
    arrow_id = f"arrow-{diagram_id}"

    nodes = {n["id"]: n for n in doc.get("nodes", [])}
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}">')
    parts.append(f'<rect width="100%" height="100%" fill="{esc(bg)}"/>')
    parts.append('<defs>')
    parts.append(f'<marker id="{arrow_id}" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/></marker>')
    parts.append('</defs>')

    title = meta.get("title")
    if title:
        parts.append(f'<text x="{width/2:g}" y="42" text-anchor="middle" font-family="{esc(en_font)},{esc(zh_font)},serif" font-size="{title_px:g}" font-weight="700" fill="{style["text"]}">{esc(title)}</text>')

    for g in doc.get("groups", []):
        x, y, w, h = map(float, (g["x"], g["y"], g["w"], g["h"]))
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="18" fill="{style["group_fill"]}" stroke="{style["group_stroke"]}" stroke-width="1.5" stroke-dasharray="6 5"/>')


    # edges behind nodes
    for e in doc.get("edges", []):
        pts = route_edge(doc, e)
        if len(pts)<2: continue
        color = style.get(e.get("kind", "main"), style["main"])
        dash = ' stroke-dasharray="7 5"' if e.get("kind") in ("feedback", "constraint") else ""
        points = " ".join(f"{x:g},{y:g}" for x, y in pts)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#{arrow_id})"{dash}/>')
        if e.get("label"):
            mx, my = pts[len(pts)//2]
            label = esc(e["label"])
            parts.append(f'<rect x="{mx-30:g}" y="{my-14:g}" width="60" height="22" rx="5" fill="{bg}" opacity="0.95"/>')
            parts.append(f'<text x="{mx:g}" y="{my+2:g}" text-anchor="middle" font-family="{esc(en_font)},{esc(zh_font)},serif" font-size="{node_px*0.9:g}" fill="{style["text"]}">{label}</text>')

    # Group labels in a high-contrast opaque reserved header strip, above connectors.
    for g in doc.get("groups", []):
        if not g.get("label"):continue
        x,y,w = float(g['x']),float(g['y']),float(g['w'])
        lbl=str(g['label'])
        from layout_utils import weighted_len
        label_w=min(w-18,28+weighted_len(lbl)*group_px*.93)
        parts.append(f'<rect x="{x+11:g}" y="{y+5:g}" width="{label_w:g}" height="32" fill="{style["group_fill"]}"/>')
        parts.append(f'<text x="{x+18:g}" y="{y+28:g}" font-family="{esc(en_font)},{esc(zh_font)},serif" font-size="{group_px:g}" font-weight="700" fill="{style["text"]}">{esc(lbl)}</text>')

    active_palette = palette_colors(doc)
    for index, n in enumerate(doc.get("nodes", [])):
        x, y, w, h = map(float, (n["x"], n["y"], n["w"], n["h"]))
        emphasis = n.get("emphasis", "normal")
        idx = n.get("color_index", index)
        if not isinstance(idx, int): idx = index
        use_colors = active_palette[:min(len(active_palette), 3 if len(doc.get("nodes", [])) <= 5 else 5)]
        stroke = canonical(n.get("stroke")) or use_colors[idx % len(use_colors)]
        fill = mix_white(stroke, 0.90 if emphasis == "muted" else 0.82 if emphasis == "strong" else 0.87)
        node_type = n.get("type", "process")
        if node_type in ("start", "end"):
            parts.append(f'<ellipse cx="{x+w/2:g}" cy="{y+h/2:g}" rx="{w/2:g}" ry="{h/2:g}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        elif node_type == "decision":
            p = [(x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)]
            ps = " ".join(f"{px:g},{py:g}" for px,py in p)
            parts.append(f'<polygon points="{ps}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        else:
            rx = 18 if node_type in ("rounded", "note") else 8
            dash = ' stroke-dasharray="5 4"' if node_type == "note" else ""
            parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')

        max_units = max(6, w / (node_px * 0.82))
        lines = wrap_text(n.get("text", ""), max_units)
        line_h = node_px * 1.25
        total_h = line_h * len(lines)
        start_y = y + h/2 - total_h/2 + node_px
        weight = "700" if emphasis == "strong" else "400"
        for i, line in enumerate(lines):
            ty = start_y + i * line_h
            parts.append(f'<text x="{x+w/2:g}" y="{ty:g}" text-anchor="middle" font-family="{esc(en_font)},{esc(zh_font)},serif" font-size="{node_px:g}" font-weight="{weight}" fill="{style["text"]}">{esc(line)}</text>')

    parts.append('</svg>')
    Path(out_path).write_text("\n".join(parts), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Render SCIY diagram JSON to SVG")
    ap.add_argument("input", help="diagram JSON")
    ap.add_argument("output", help="output SVG")
    ap.add_argument("--style", choices=sorted(STYLES), default=None)
    args = ap.parse_args()
    doc = json.loads(Path(args.input).read_text(encoding="utf-8"))
    render(doc, args.output, args.style)
    print(args.output)

if __name__ == "__main__":
    main()
