#!/usr/bin/env python3
"""SCIY v1.0: edit-ready PowerPoint; native editable boxes/text/line segments.
Colors/fonts are explicit (never inherited from a slide theme). Edges follow SVG
waypoints including the last arrowhead. No raster images embedded.
"""
import argparse
import json
import sys
from pathlib import Path
from palette_utils import palette_colors, flow_colors, mix_white, canonical
from layout_utils import route_edge, wrap_text, weighted_len


def main():
    try:
        from pptx import Presentation
        from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
        from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
        from pptx.dml.color import RGBColor
        from pptx.util import Inches, Pt
        from pptx.oxml.xmlchemy import OxmlElement
    except ImportError:
        print('python-pptx required: pip install python-pptx',file=sys.stderr);sys.exit(2)

    ap=argparse.ArgumentParser(description='Export diagram JSON as native editable PPTX')
    ap.add_argument('input');ap.add_argument('output');args=ap.parse_args()
    doc=json.loads(Path(args.input).read_text(encoding='utf-8'))
    palette=palette_colors(doc)
    colors=flow_colors(doc, {})
    def rgb(code):
        hexcode=(canonical(code) or palette[0])[1:]
        return RGBColor(*(int(hexcode[i:i+2],16) for i in (0,2,4)))
    canvas=doc.get('canvas',{})
    cw,ch=float(canvas.get('width',1600)),float(canvas.get('height',900))
    prs=Presentation()
    # Aspect ratio of slide matches master SVG: no stretching distortion.
    prs.slide_width=Inches(13.333)
    prs.slide_height=int(prs.slide_width*ch/cw)
    slide=prs.slides.add_slide(prs.slide_layouts[6])
    sx=float(prs.slide_width)/cw
    sy=float(prs.slide_height)/ch
    def xpt(v):return int(round(float(v)*sx))
    def ypt(v):return int(round(float(v)*sy))
    px_to_pt=(sx / 12700) # EMUs to points = 12700 EMU /pt
    # SVG uses 96 dpi CSS pixels; PPT scale coordinates to the same physical size.
    scale=min(sx,sy)/12700
    ty=doc.get('typography',{})
    en_font=ty.get('english_font','Times New Roman')
    zh_font=ty.get('chinese_font','Source Han Sans SC')
    def f_name(s):return zh_font if any(ord(ch)>127 for ch in str(s)) else en_font
    font_text=colors['text']

    def clean_theme_effect(shape):
        from pptx.oxml.ns import qn
        st=shape._element.find(qn('p:style'))
        if st is not None:
            shape._element.remove(st)

    def edit_text(shape,text,fontsize,bold=False,alignment=PP_ALIGN.CENTER,
                  vertical=MSO_ANCHOR.MIDDLE,lines=None):
        tf=shape.text_frame
        tf.clear()
        tf.word_wrap=False
        tf.margin_left=Pt(3);tf.margin_right=Pt(3)
        tf.margin_top=Pt(1);tf.margin_bottom=Pt(1)
        tf.vertical_anchor=vertical
        str_lines=(lines if lines is not None else str(text).split('\n'))
        for k,t in enumerate(str_lines):
            p=tf.paragraphs[0] if k==0 else tf.add_paragraph()
            p.alignment=alignment
            p.space_before=Pt(0);p.space_after=Pt(0)
            p.line_spacing=1.08
            run=p.add_run();run.text=str(t)
            run.font.name=f_name(t or text)
            run.font.size=Pt(fontsize)
            run.font.bold=bold
            run.font.color.rgb=rgb(font_text)
        return tf

    # Groups painted first; headings added on top AFTER edges
    for g in doc.get('groups',[]):
        sh=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,xpt(g['x']),ypt(g['y']),xpt(g['w']),ypt(g['h']))
        clean_theme_effect(sh)
        try: sh.adjustments[0]=0.035
        except (IndexError,TypeError): pass
        sh.fill.solid();sh.fill.fore_color.rgb=rgb(colors['group_fill'])
        sh.line.color.rgb=rgb(colors['group_stroke']);sh.line.width=Pt(0.9)
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        sh.line.dash_style=MSO_LINE_DASH_STYLE.DASH
        sh.text_frame.clear()

    nodes={n['id']:n for n in doc.get('nodes',[]) if 'id' in n}
    # Native editable line segments, arrowhead on FINAL segment only.
    for edge in doc.get('edges',[]):
        pts=route_edge(doc,edge)
        if len(pts)<2:continue
        col=colors.get(edge.get('kind','main'),colors['main'])
        for k,(p,q) in enumerate(zip(pts,pts[1:])):
            if p==q:continue
            c=slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,xpt(p[0]),ypt(p[1]),xpt(q[0]),ypt(q[1]))
            clean_theme_effect(c)
            c.line.color.rgb=rgb(col)
            c.line.width=Pt(1.25)
            if edge.get('kind') in ('feedback','constraint'):
                from pptx.enum.dml import MSO_LINE_DASH_STYLE
                c.line.dash_style=MSO_LINE_DASH_STYLE.DASH
            if k==len(pts)-2:
                line=c._element.spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
                if line is not None:
                    arrow=OxmlElement('a:tailEnd')
                    arrow.set('type','triangle');arrow.set('w','med');arrow.set('len','med')
                    line.append(arrow)

    # Native editable nodes, text with explicit contrast and manual wrapping.
    for index,n in enumerate(doc.get('nodes',[])):
        typ=n.get('type','process')
        shape_type=MSO_SHAPE.RECTANGLE
        if typ in ('rounded','note'):shape_type=MSO_SHAPE.ROUNDED_RECTANGLE
        elif typ=='decision':shape_type=MSO_SHAPE.DIAMOND
        elif typ in ('start','end'):shape_type=MSO_SHAPE.OVAL
        x,y,w,h=[float(n[k]) for k in ('x','y','w','h')]
        shape=slide.shapes.add_shape(shape_type,xpt(x),ypt(y),xpt(w),ypt(h))
        used=palette[:min(len(palette),3 if len(nodes)<=5 else 5)]
        ci=n.get('color_index',index)
        if not isinstance(ci,int):ci=index
        outline=canonical(n.get('stroke')) or used[ci%len(used)]
        emphasize=n.get('emphasis','normal')
        clean_theme_effect(shape)
        shape.fill.solid();shape.fill.fore_color.rgb=rgb(mix_white(outline,0.90 if emphasize=='muted' else 0.82 if emphasize=='strong' else 0.87))
        shape.line.color.rgb=rgb(outline);shape.line.width=Pt(1.3)
        node_pt=float(ty.get('node_pt',12))
        # exact same max-line-unit rule as SVG, preserving authored line breaks
        max_units=max(6,w/(node_pt*(4/3)*.82))
        lines=wrap_text(n.get('text',''),max_units)
        # Rendered image on slide typically uses 0.8x font compared to input pts.
        nominal=node_pt * (scale*(96/72))
        font=min(nominal,max(7.0,(h*scale-5)/(max(1,len(lines))*1.12)))
        edit_text(shape,n.get('text',''),font,emphasize=='strong',lines=lines)

    # Group labels are independent editable text shapes with explicit colors.
    gp=float(ty.get('group_pt',13)) * (scale*(96/72))
    for g in doc.get('groups',[]):
        lbl=str(g.get('label',''))
        if not lbl:continue
        x,y,w=float(g['x']),float(g['y']),float(g['w'])
        fontsize=min(gp,max(7.5,(w-30)*scale*1.4/max(1,weighted_len(lbl))))
        band=slide.shapes.add_textbox(xpt(x+15),ypt(y+6),xpt(w-29),ypt(32))
        clean_theme_effect(band)
        # ensures header behind type is opaque even when a route is very close
        edit_text(band,lbl,fontsize,True,PP_ALIGN.LEFT,MSO_ANCHOR.MIDDLE)

    # Main title and edge labels are text, not baked into SVG imagery.
    meta=doc.get('meta',{})
    if meta.get('title'):
        top=slide.shapes.add_textbox(xpt(35),ypt(4),xpt(cw-70),ypt(60))
        clean_theme_effect(top)
        title_pt=float(ty.get('title_pt',15))*(scale*(96/72))
        edit_text(top,meta['title'],title_pt,True)
    for e in doc.get('edges',[]):
        if not e.get('label'):continue
        pts=route_edge(doc,e)
        if len(pts)<2:continue
        xx,yy=pts[len(pts)//2]
        box=slide.shapes.add_textbox(xpt(xx-42),ypt(yy-15),xpt(84),ypt(25))
        clean_theme_effect(box)
        edit_text(box,e['label'],float(ty.get('node_pt',12))*.70)
    prs.save(args.output)
    print(args.output)

if __name__=='__main__':main()
