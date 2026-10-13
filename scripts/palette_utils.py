"""SCIY flowchart color utility. Standalone and stdlib-only.

The user's palette overrides style token colors. Structure references NEVER
supply their own colors. All colors are validated HEX strings before export.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
DEFAULT = ['#3C5488', '#4DBBD5', '#00A087']


def canonical(color):
    if not isinstance(color, str):
        return None
    color = color.strip()
    if re.fullmatch(r'#[0-9a-fA-F]{3}', color):
        color = '#' + ''.join(c * 2 for c in color[1:])
    return color.upper() if HEX.fullmatch(color) else None


def mix_white(hex_color, fraction=0.84):
    """Blend foreground with white. fraction=1 returns pure white."""
    h = canonical(hex_color)
    if not h:
        raise ValueError('Expected a HEX color')
    a = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    out = [round(x * (1 - fraction) + 255 * fraction) for x in a]
    return '#' + ''.join(f'{v:02X}' for v in out)


def palette_colors(doc):
    """Supports doc.color and doc.palette. Supports P01...P08 or a custom list.

    Invalid colors gracefully fall back rather than breaking SVG/PPTX output.
    """
    choice = doc.get('color') or doc.get('palette') or {}
    if isinstance(choice, str):
        choice = {'palette_id': choice}
    if isinstance(choice, list):
        choice = {'colors': choice}
    if not isinstance(choice, dict):
        choice = {}
    raw = choice.get('colors')
    if isinstance(raw, str):
        raw = [x.strip() for x in raw.split(',')]
    if isinstance(raw, list):
        valid = [canonical(x) for x in raw]
        valid = [x for x in valid if x]
        if valid:
            return valid[:8]
    ident = str(choice.get('palette_id') or choice.get('id') or '').strip().upper()
    if ident:
        try:
            presets = json.loads((ROOT / 'references' / 'color-palettes.json').read_text(encoding='utf-8'))
            for p in presets:
                if ident == str(p.get('id', '')).upper() or ident == str(p.get('name', '')).upper():
                    valid = [canonical(x) for x in p['colors']]
                    return [v for v in valid if v]
        except (OSError, ValueError, KeyError, TypeError):
            pass
    return DEFAULT.copy()


def flow_colors(doc, style):
    """Create usable paint tokens. Preserve shape/layout family not its colors."""
    picks = palette_colors(doc)
    p = picks[0]
    s = picks[1] if len(picks) > 1 else p
    t = picks[2] if len(picks) > 2 else s
    return {
        **style,
        'bg': '#FFFFFF',
        'group_fill': mix_white(p, 0.96),
        'group_stroke': mix_white(p, 0.57),
        'node_fill': mix_white(p, 0.89),
        'node_stroke': p,
        'strong_fill': mix_white(s, 0.81),
        'muted_fill': mix_white(t, 0.91),
        'text': '#23313D',
        'secondary': '#52616E',
        'main': p,
        'feedback': t,
        'constraint': s,
    }
