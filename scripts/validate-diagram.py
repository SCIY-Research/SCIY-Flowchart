#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from layout_utils import collisions, wrap_text, weighted_len
from importlib.util import spec_from_file_location, module_from_spec


def overlap(a, b, pad=4):
    return not (
        a["x"] + a["w"] + pad <= b["x"] or
        b["x"] + b["w"] + pad <= a["x"] or
        a["y"] + a["h"] + pad <= b["y"] or
        b["y"] + b["h"] + pad <= a["y"]
    )


def main():
    ap = argparse.ArgumentParser(description="Validate SCIY diagram JSON")
    ap.add_argument("input")
    args = ap.parse_args()
    doc = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors, warnings = [], []
    canvas = doc.get("canvas", {})
    cw, ch = float(canvas.get("width", 0)), float(canvas.get("height", 0))
    if cw <= 0 or ch <= 0:
        errors.append("canvas width/height must be positive")

    nodes = doc.get("nodes", [])
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate node IDs found")
    node_map = {n.get("id"): n for n in nodes if n.get("id")}

    for n in nodes:
        for k in ("id", "text", "x", "y", "w", "h"):
            if k not in n:
                errors.append(f"node {n.get('id','?')} missing {k}")
        if all(k in n for k in ("x", "y", "w", "h")):
            if n["w"] <= 0 or n["h"] <= 0:
                errors.append(f"node {n.get('id')} has non-positive size")
            if cw and ch and (n["x"] < 0 or n["y"] < 0 or n["x"] + n["w"] > cw or n["y"] + n["h"] > ch):
                warnings.append(f"node {n.get('id')} extends outside canvas")
        if len(str(n.get("text", ""))) > 90:
            warnings.append(f"node {n.get('id')} has very long text; consider a note or split node")
        if all(k in n for k in ('x','y','w','h')) and n['w']>0 and n['h']>0:
            font_px=float(doc.get('typography',{}).get('node_pt',12))*4/3
            lines=wrap_text(n.get('text',''),max(6,n['w']/(font_px*.82)))
            if len(lines)*font_px*1.20>float(n['h'])-6:
                warnings.append(f"node {n.get('id')} may overflow vertically ({len(lines)} lines)")

    for e in doc.get("edges", []):
        if e.get("from") not in node_map:
            errors.append(f"edge {e.get('id','?')} has unknown from={e.get('from')}")
        if e.get("to") not in node_map:
            errors.append(f"edge {e.get('id','?')} has unknown to={e.get('to')}")
        pts = e.get("points")
        if pts is not None and len(pts) < 2:
            errors.append(f"edge {e.get('id','?')} points must contain at least 2 points")
        if pts is not None:
            for p in pts:
                if not isinstance(p,(list,tuple)) or len(p)!=2 or not all(isinstance(z,(int,float)) for z in p):
                    errors.append(f"edge {e.get('id','?')} contains a malformed waypoint")
                    break
        if e.get('from') in node_map and e.get('to') in node_map and (pts is None or len(pts)>=2):
            try:
                result=collisions(doc,e,routed=True)
                if result['heading']:
                    errors.append(f"edge {e.get('id','?')} crosses group title after routing; adjust positions/waypoints")
                if result['node']:
                    warnings.append(f"edge {e.get('id','?')} passes through unrelated node; consider rearranging")
                points=result['route']
                if len(points)>1 and any((x<0 or y<0 or x>cw or y>ch) for x,y in points):
                    warnings.append(f"edge {e.get('id','?')} routed outside canvas")
            except Exception as ex:
                errors.append(f"edge {e.get('id','?')} route invalid: {ex}")

    # Only flag overlap for nodes in same group (or both ungrouped); group boxes may intentionally overlap nodes.
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            if a.get("group") == b.get("group") and all(k in a for k in ("x","y","w","h")) and all(k in b for k in ("x","y","w","h")):
                if overlap(a, b):
                    warnings.append(f"nodes {a.get('id')} and {b.get('id')} overlap or are too close")

    typo = doc.get("typography", {})
    if float(typo.get("node_pt", 12)) < 9:
        warnings.append("node font is below 9 pt; readability may be poor")

    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"Validation complete: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
