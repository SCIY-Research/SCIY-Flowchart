#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
style_dirs = sorted([p for p in (ROOT / "styles").iterdir() if p.is_dir() and (p / "preview.png").exists()])
if not style_dirs:
    raise SystemExit("No style previews found under styles/")
thumbs=[]
for d in style_dirs:
    im=Image.open(d/"preview.png").convert("RGB")
    im.thumbnail((560,355))
    canvas=Image.new("RGB",(590,395),"white")
    canvas.paste(im,((590-im.width)//2,10))
    dr=ImageDraw.Draw(canvas)
    dr.text((20,370),d.name,fill="black")
    thumbs.append(canvas)
rows=(len(thumbs)+1)//2
out=Image.new("RGB",(1180,rows*395),"white")
for i,im in enumerate(thumbs):
    out.paste(im,((i%2)*590,(i//2)*395))
gallery=ROOT/"examples"/"style-gallery"
gallery.mkdir(parents=True,exist_ok=True)
out.save(gallery/"style-gallery.png",quality=95)
print(gallery/"style-gallery.png")
