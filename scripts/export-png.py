#!/usr/bin/env python3
"""Export PNG without requiring an external CLI if CairoSVG is installed."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description='Render SVG to PNG using CairoSVG or a local rasterizer')
    p.add_argument('svg');p.add_argument('png');p.add_argument('--width',type=int,default=2400)
    a=p.parse_args();svg=Path(a.svg).resolve();png=Path(a.png).resolve()
    png.parent.mkdir(parents=True,exist_ok=True)
    if not svg.is_file():raise SystemExit(f'SVG not found: {svg}')
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=a.width)
        print(str(png));return
    except ImportError:
        pass
    except Exception as ex:
        print(f'CairoSVG failed ({ex}); trying external converter.',file=sys.stderr)
    if shutil.which('inkscape'):
        cmd=['inkscape',str(svg),'--export-type=png',f'--export-filename={png}',f'--export-width={a.width}']
    elif shutil.which('rsvg-convert'):
        cmd=['rsvg-convert','-w',str(a.width),'-o',str(png),str(svg)]
    elif shutil.which('magick'):
        cmd=['magick','-background','white','-density','180',str(svg),str(png)]
    else:
        raise SystemExit('No SVG converter available: optional pip install cairosvg, or use Inkscape.')
    subprocess.run(cmd,check=True,timeout=90)
    print(str(png))

if __name__=='__main__':main()
