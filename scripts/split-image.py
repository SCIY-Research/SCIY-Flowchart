#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def main():
    try:
        from PIL import Image
    except Exception:
        print("Pillow is required for physical image cropping. Install it or crop with another available tool.", file=sys.stderr)
        sys.exit(2)

    ap = argparse.ArgumentParser(description="Crop a source flowchart into semantic regions")
    ap.add_argument("image")
    ap.add_argument("regions_json", help='JSON file: [{"id":"part-a","x":0,"y":0,"w":500,"h":400}, ...]')
    ap.add_argument("output_dir")
    args = ap.parse_args()
    regions = json.loads(Path(args.regions_json).read_text(encoding="utf-8"))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    im = Image.open(args.image)
    W, H = im.size
    for r in regions:
        x, y, w, h = map(int, (r["x"], r["y"], r["w"], r["h"]))
        x2, y2 = min(W, x+w), min(H, y+h)
        crop = im.crop((max(0,x), max(0,y), x2, y2))
        target = out / f"{r['id']}.png"
        crop.save(target)
        print(target)

if __name__ == "__main__":
    main()
