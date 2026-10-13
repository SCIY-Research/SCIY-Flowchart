#!/usr/bin/env python3
import argparse
import html
import json
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def main():
    ap = argparse.ArgumentParser(description="Assemble vector SVG regions into one master SVG")
    ap.add_argument("manifest", help="assembly manifest JSON")
    ap.add_argument("output", help="output SVG")
    args = ap.parse_args()
    manifest_path = Path(args.manifest)
    doc = json.loads(manifest_path.read_text(encoding="utf-8"))
    canvas = doc.get("canvas", {})
    w, h = float(canvas.get("width", 1600)), float(canvas.get("height", 900))
    bg = canvas.get("background", "#ffffff")
    root = ET.Element(f"{{{SVG_NS}}}svg", {"width": f"{w:g}", "height": f"{h:g}", "viewBox": f"0 0 {w:g} {h:g}"})
    ET.SubElement(root, f"{{{SVG_NS}}}rect", {"width": "100%", "height": "100%", "fill": bg})

    base = manifest_path.parent
    for idx, part in enumerate(doc.get("parts", []), 1):
        source = (base / part["file"]).resolve()
        tree = ET.parse(source)
        src_root = tree.getroot()
        vb = src_root.attrib.get("viewBox")
        if not vb:
            sw = src_root.attrib.get("width", str(part["width"]))
            sh = src_root.attrib.get("height", str(part["height"]))
            vb = f"0 0 {sw} {sh}"
        nested = ET.SubElement(root, f"{{{SVG_NS}}}svg", {
            "id": f"part-{idx}",
            "x": str(part["x"]), "y": str(part["y"]),
            "width": str(part["width"]), "height": str(part["height"]),
            "viewBox": vb, "preserveAspectRatio": "xMidYMid meet"
        })
        for child in list(src_root):
            nested.append(child)

    if doc.get("cross_edges"):
        defs = ET.SubElement(root, f"{{{SVG_NS}}}defs")
        marker = ET.SubElement(defs, f"{{{SVG_NS}}}marker", {"id":"arrow-master","markerWidth":"10","markerHeight":"10","refX":"9","refY":"3","orient":"auto","markerUnits":"strokeWidth"})
        ET.SubElement(marker, f"{{{SVG_NS}}}path", {"d":"M0,0 L0,6 L9,3 z","fill":"#222222"})
        for e in doc["cross_edges"]:
            pts = " ".join(f"{float(p[0]):g},{float(p[1]):g}" for p in e["points"])
            ET.SubElement(root, f"{{{SVG_NS}}}polyline", {"points":pts,"fill":"none","stroke":"#222222","stroke-width":"2","stroke-linejoin":"round","stroke-linecap":"round","marker-end":"url(#arrow-master)"})
            if e.get("label"):
                p = e["points"][len(e["points"])//2]
                t = ET.SubElement(root, f"{{{SVG_NS}}}text", {"x":str(p[0]),"y":str(p[1]-8),"text-anchor":"middle","font-family":"Times New Roman,Source Han Sans SC,serif","font-size":"16","fill":"#111111"})
                t.text = str(e["label"])

    ET.ElementTree(root).write(args.output, encoding="utf-8", xml_declaration=True)
    print(args.output)

if __name__ == "__main__":
    main()
