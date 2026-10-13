#!/usr/bin/env python3
"""SCIY Flowchart v1.0 smoke and packaging checks (stdlib + optional pptx)."""
from __future__ import annotations
import json
import py_compile
import subprocess
import sys
import tempfile
import zipfile
import shutil
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors=[]; passes=[]

def ck(value, label):
    (passes if value else errors).append(label)

critical = [
    'SKILL.md', 'README.md', 'VERSION', 'SELECTION-GALLERY.html', 'SELECTION-GALLERY.md',
    'STYLE-GALLERY.html', 'STYLE-GALLERY.md', 'COLOR-GALLERY.html', 'COLOR-GALLERY.md',
    'references/STRUCTURE-REFERENCE-SOURCES.md', 'references/COLOR-PALETTE-SOURCES.md',
    'references/structure-reference-manifest.json','references/color-palettes.json',
    'references/ai-concept-stage.md','references/color-system.md',
    'references/interaction-flow-v1.0.md','references/one-click-defaults.md',
    'references/visual-prompting.md',
    'scripts/concept-preview.py', 'scripts/build-selection-gallery.py',
    'scripts/palette_utils.py','scripts/render-svg.py','scripts/validate-diagram.py',
    'scripts/assemble-svg.py','scripts/export-png.py','scripts/export-pptx.py',
    'scripts/split-image.py', 'scripts/layout_utils.py', 'scripts/check-semantics.py', 'references/test-prompts-v1.0.md',
]
for f in critical:
    ck((ROOT/f).is_file(), f'file {f}')
slugs = ('academic-classic','academic-modular','technical-architecture','timeline-stage','swimlane','cycle-feedback','network-concept','illustrated-workflow')
for i, slug in enumerate(slugs,1):
    p=ROOT/f'examples/style-gallery/sciy-ai/{i:02d}-{slug}.png'
    ck(p.exists() and p.stat().st_size>10000, f'local backup image {i:02d}')

try:
    refs=json.loads((ROOT/'references/structure-reference-manifest.json').read_text(encoding='utf-8'))
    pals=json.loads((ROOT/'references/color-palettes.json').read_text(encoding='utf-8'))
    ck(len(refs)==32 and len({p['id'] for p in refs})==32, '32 unique academic references')
    ck(len(pals)==8 and len({p['id'] for p in pals})==8, '8 unique color palettes')
except Exception as e:
    errors.append(f'manifests: {e}'); refs=[];pals=[]
try:
    view=(ROOT/'SELECTION-GALLERY.html').read_text(encoding='utf-8')
    ck(view.count('class="ref"')==32, '32 references shown in combined chooser')
    ck(view.count('data-key="P0')==8, '8 colors shown in combined chooser')
    ck('data-fallback=' in view and 'this.onerror=null' in view, 'offline/failure image fallback')
    ck('chooseStructure' in view and 'chooseColor' in view, 'joint choice controls')
    ck('structure' in view and '来源/许可' in view, 'source links/rights note')
except Exception as e:
    errors.append(f'combined gallery: {e}')
try:
    skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    ck('SELECTION-GALLERY.html' in skill, 'combined gallery is default path')
    ck('scripts/check-semantics.py' in skill, 'scientific semantic audit is documented')
    ck('Only an explicit request' in skill and 'No default route' in skill,
       'Quick requires explicit user selection; no default route')
    ck('There is no default family 01' in skill,
       'no default first structural family')
    ck('only after image selection' in skill and 'No default drawing method' in skill,
       'Custom asks Global versus Region after concept selection')
    ck('output language' in skill and 'SAME question' in skill,
       'language and typography asked with structure and palette')
    ck('retry a transient failure at most once' in skill,
       'bounded retry contract')
except Exception as e:
    errors.append(f'SKILL.md: {e}')

for f in sorted((ROOT/'scripts').glob('*.py')):
    try: py_compile.compile(str(f), doraise=True);passes.append('syntax '+f.name)
    except Exception as e:errors.append(f'syntax {f.name}: {e}')

# Some locked-down Windows/Codex sandboxes cannot auto-clean TemporaryDirectory.
# Create under the skill parent (writable install), then cleanup as best-effort.
try:
    t=Path(tempfile.mkdtemp(prefix='sciy-v10-test-',dir=str(ROOT.parent)))
except (PermissionError,OSError):
    t=Path(tempfile.mkdtemp(prefix='sciy-v10-test-'))
try:

    ex=ROOT/'examples/sample-diagram.json'
    cmd=[sys.executable, str(ROOT/'scripts/concept-preview.py'),str(ex),str(t/'four'),'--count','4']
    v=subprocess.run(cmd, text=True, capture_output=True)
    ck(v.returncode==0 and (t/'four/PREVIEW-INDEX.html').exists() and all((t/f'four/concept-{a}.svg').exists() for a in 'ABCD'),'offline preview 4 SVGs')
    v=subprocess.run([sys.executable,str(ROOT/'scripts/concept-preview.py'),str(ex),str(t/'one'),'--count','1'],text=True,capture_output=True)
    ck(v.returncode==0 and (t/'one/concept-A.svg').exists() and not (t/'one/concept-B.svg').exists(),'offline one-click 1 SVG')
    try:
        basic=json.loads(ex.read_text(encoding='utf-8'))
        for tag,palid in [('npg','P01'),('jama','P03')]:
            data=dict(basic);data['color']={'palette_id':palid}
            jp=t/f'{tag}.json';jp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
            sv=t/f'{tag}.svg'
            v=subprocess.run([sys.executable,str(ROOT/'scripts/render-svg.py'),str(jp),str(sv)],text=True,capture_output=True)
            ck(v.returncode==0 and sv.exists(),f'SVG render {palid}')
            if sv.exists():
                txt=sv.read_text(encoding='utf-8')
                ck(('#E64B35' if palid=='P01' else '#374E55') in txt, f'SVG honoring {palid}')
        ck((t/'npg.svg').read_bytes()!=(t/'jama.svg').read_bytes(),'palette change actually changes export')
        import importlib.util
        if importlib.util.find_spec('pptx'):
            outfile=t/'color.pptx'
            v=subprocess.run([sys.executable,str(ROOT/'scripts/export-pptx.py'),str(t/'jama.json'),str(outfile)],text=True,capture_output=True)
            ck(v.returncode==0 and outfile.exists(),'native PPTX export smoke test')
            if outfile.exists():
                with zipfile.ZipFile(outfile) as z:
                    slide=z.read('ppt/slides/slide1.xml').decode('utf-8')
                    ck('374E55' in slide,'PPTX honoring custom palette')
        else:
            print('SKIP optional PPTX test: python-pptx not installed')
    except Exception as e:
        errors.append(f'render tests: {e}')

finally:
    try: shutil.rmtree(t)
    except OSError: print('NOTE: self-check temporary directory cleanup deferred:',t)

print('SCIY Flowchart self-check v1.0')
for label in passes:print('PASS',label)
for label in errors:print('FAIL',label)
print(f'Summary: {len(passes)} PASS / {len(errors)} FAIL')
sys.exit(1 if errors else 0)
