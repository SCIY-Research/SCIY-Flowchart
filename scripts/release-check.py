#!/usr/bin/env python3
"""Deterministic SCIY v1.0 integration tests. Uses a public paper-derived example.
Optional packages: python-pptx, CairoSVG; SVG and semantic checks use stdlib.
"""
from __future__ import annotations
import json,subprocess,sys,tempfile,zipfile,importlib.util
from pathlib import Path
from layout_utils import collisions,wrap_text
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

def cmd(*a):
    r=subprocess.run([PY,*map(str,a)],text=True,capture_output=True,timeout=45)
    if r.returncode:
        raise AssertionError(f"COMMAND FAILED {a}:\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()

def test():
    src=ROOT/'examples/release-case-ml-gap.json'
    doc=json.loads(src.read_text(encoding='utf-8'))
    assert len(doc['groups'])==4
    assert len(doc['edges'])>=15
    assert wrap_text('Training feature\nrepresentations',20)==['Training feature','representations']
    for edge in doc['edges']:
        collision=collisions(doc,edge)
        assert not collision['heading'],(edge['id'],'group-header collision')
    with tempfile.TemporaryDirectory(prefix='sciy-v10-release-') as t:
        t=Path(t)
        cmd(ROOT/'scripts/check-semantics.py',src)
        cmd(ROOT/'scripts/validate-diagram.py',src)
        svg=t/'test.svg';png=t/'test.png';pptx=t/'test.pptx'
        cmd(ROOT/'scripts/render-svg.py',src,svg)
        assert svg.exists() and svg.stat().st_size>1000
        if importlib.util.find_spec('cairosvg'):
            cmd(ROOT/'scripts/export-png.py',svg,png,'--width','1600')
            assert png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
        else:
            print('SKIP PNG conversion: CairoSVG not installed')
        if importlib.util.find_spec('pptx'):
            cmd(ROOT/'scripts/export-pptx.py',src,pptx)
            with zipfile.ZipFile(pptx) as z:
                data=z.read('ppt/slides/slide1.xml').decode('utf-8')
                assert '<a:tailEnd type="triangle"' in data, 'PPT arrows missing'
                assert '23313D' in data, 'explicit text color missing'
                assert 'ML-GAP: RNA-seq' in data, 'title missing'
                assert 'E64B35' not in data, 'wrong theme/palette'
                assert 'B24745' in data or '374E55' in data, 'selected palette missing'
                assert z.testzip() is None
        else:
            print('SKIP PPTX export: python-pptx not installed')
        bad=json.loads(src.read_text(encoding='utf-8'))
        bad['edges'].append({'id':'bad','from':'baseline','to':'ae'})
        badfile=t/'bad.json';badfile.write_text(json.dumps(bad),encoding='utf-8')
        proc=subprocess.run([PY,str(ROOT/'scripts/check-semantics.py'),str(badfile)],capture_output=True,text=True)
        assert proc.returncode!=0 and 'parallel alternatives incorrectly linked' in proc.stdout
    print('RELEASE CHECK: PASS — semantics, routes, SVG, optional PNG/PPTX, negative scientific assertion')

if __name__=='__main__':test()
