"""Shared SCIY v1.0 geometry, text sizing and collision-aware orthogonal routes.
No dependency on proprietary diagram tools. The renderers both consume routes from here.
"""
from __future__ import annotations
from heapq import heappop, heappush
from math import inf


def weighted_len(s):
    return sum(1 if ord(ch) > 127 else 0.55 for ch in s)


def wrap_text(text, max_units):
    """Preserve author-supplied newlines. Long tokens wrap, no silent newline removal."""
    result = []
    for line in str(text or '').split('\n'):
        if not line:
            result.append(''); continue
        cur = ''
        tokens = line.split(' ') if ' ' in line else list(line)
        divider = ' ' if ' ' in line else ''
        for word in tokens:
            # oversized English tokens are broken only when unavoidable
            pieces=[]
            if weighted_len(word) > max_units:
                piece=''
                for char in word:
                    if piece and weighted_len(piece+char)>max_units:
                        pieces.append(piece);piece=''
                    piece+=char
                if piece: pieces.append(piece)
            else: pieces=[word]
            for part in pieces:
                test = part if not cur else cur+divider+part
                if cur and weighted_len(test) > max_units:
                    result.append(cur);cur=part
                else:
                    cur=test
        result.append(cur)
    return result or ['']


def center(n):
    return (float(n['x']) + float(n['w'])/2, float(n['y']) + float(n['h'])/2)


def orthogonal_route(a, b):
    ax,ay = center(a); bx,by=center(b)
    if abs(bx-ax) >= abs(by-ay):
        sx = float(a['x']+a['w']) if bx>=ax else float(a['x'])
        ex = float(b['x']) if bx>=ax else float(b['x']+b['w'])
        mx=(sx+ex)/2
        return [(sx,ay),(mx,ay),(mx,by),(ex,by)]
    sy=float(a['y']+a['h']) if by>=ay else float(a['y'])
    ey=float(b['y']) if by>=ay else float(b['y']+b['h'])
    my=(sy+ey)/2
    return [(ax,sy),(ax,my),(bx,my),(bx,ey)]


def heading_rects(doc):
    """Reserve actual label-bearing portion, not the entire group width."""
    out=[]
    group_px=float(doc.get('typography',{}).get('group_pt',13))*4/3
    for g in doc.get('groups',[]):
        label=str(g.get('label',''))
        if label:
            width=min(float(g['w'])-12, 24+weighted_len(label)*group_px*0.93)
            out.append((float(g['x'])+10, float(g['y'])+5,
                        float(g['x'])+10+max(1,width),float(g['y'])+37))
    return out


def node_rects(doc, exclude=frozenset()):
    return [(float(n['x']),float(n['y']),float(n['x']+n['w']),float(n['y']+n['h']))
            for n in doc.get('nodes',[]) if n.get('id') not in exclude]


def seg_hits_rect(p,q,r, pad=0):
    x1,y1,x2,y2=r
    x1-=pad;y1-=pad;x2+=pad;y2+=pad
    ax,ay=p; bx,by=q
    if abs(ax-bx)<1e-6:
        return x1 < ax < x2 and max(ay,by)>y1 and min(ay,by)<y2
    if abs(ay-by)<1e-6:
        return y1 < ay < y2 and max(ax,bx)>x1 and min(ax,bx)<x2
    # general segments (rare): reject conservatively by bounding box
    return max(ax,bx)>x1 and min(ax,bx)<x2 and max(ay,by)>y1 and min(ay,by)<y2


def path_hits(pts, rects):
    return [(i,k) for i,(p,q) in enumerate(zip(pts,pts[1:])) for k,r in enumerate(rects) if seg_hits_rect(p,q,r)]


def simplify(points):
    pts=[]
    for p in points:
        p=(round(float(p[0]),3),round(float(p[1]),3))
        if pts and pts[-1]==p:continue
        if len(pts)>=2:
            a,b=pts[-2],pts[-1]
            if abs((b[0]-a[0])*(p[1]-b[1])-(b[1]-a[1])*(p[0]-b[0]))<1e-7:
                pts[-1]=p;continue
        pts.append(p)
    return pts


def avoid_obstacles(start,end,obstacles,width,height,clearance=9):
    """Sparse rectilinear visibility-graph routing; minimizes Manhattan length and turns.
    Endpoints may lie on an obstacle boundary, but the route may not pass its interior.
    """
    sx,sy=start;ex,ey=end
    xs={float(sx),float(ex),0.0,float(width)}
    ys={float(sy),float(ey),0.0,float(height)}
    for r in obstacles:
        x1,y1,x2,y2=r
        for x in (x1-clearance,x2+clearance):
            if 0<x<width:xs.add(x)
        for y in (y1-clearance,y2+clearance):
            if 0<y<height:ys.add(y)
    xx=sorted(xs);yy=sorted(ys)
    xi={x:i for i,x in enumerate(xx)};yi={y:i for i,y in enumerate(yy)}
    source=(xi[float(sx)],yi[float(sy)],0)
    target=(xi[float(ex)],yi[float(ey)])
    best={source:0.0}; prev={}; heap=[(0.0,0.0,source)]
    explored=0; final=None
    while heap and explored<150000:
        _,score,cur=heappop(heap)
        if score>best.get(cur,inf)+1e-7:continue
        explored+=1
        i,j,orient=cur
        if (i,j)==target:final=cur;break
        for di,dj,neworient in [(-1,0,1),(1,0,1),(0,-1,2),(0,1,2)]:
            ni,nj=i+di,j+dj
            if not(0<=ni<len(xx) and 0<=nj<len(yy)):continue
            p=(xx[i],yy[j]);q=(xx[ni],yy[nj])
            if any(seg_hits_rect(p,q,r,pad=1) for r in obstacles):continue
            turn=18 if orient and orient!=neworient else 0
            nxt=(ni,nj,neworient)
            newcost=score+abs(p[0]-q[0])+abs(p[1]-q[1])+turn
            if newcost+1e-7<best.get(nxt,inf):
                best[nxt]=newcost;prev[nxt]=cur
                heuristic=abs(q[0]-ex)+abs(q[1]-ey)
                heappush(heap,(newcost+heuristic,newcost,nxt))
    if final is None:return None
    route=[]
    while final is not None:
        i,j,_=final
        route.append((xx[i],yy[j]));final=prev.get(final)
    return simplify(route[::-1])


def route_edge(doc, edge, repair=True):
    nodes={n['id']:n for n in doc.get('nodes',[]) if 'id' in n}
    a=nodes.get(edge.get('from')); b=nodes.get(edge.get('to'))
    if a is None or b is None:return []
    pts=[(float(p[0]),float(p[1])) for p in edge['points']] if edge.get('points') else orthogonal_route(a,b)
    # Route conflict is tested against both text heading and non-endpoint nodes
    blocked=heading_rects(doc)+node_rects(doc,{edge.get('from'),edge.get('to')})
    if repair and len(pts)>=2 and path_hits(pts,blocked):
        can=doc.get('canvas',{})
        fixed=avoid_obstacles(pts[0],pts[-1],blocked,float(can.get('width',1600)),float(can.get('height',900)))
        if fixed and not path_hits(fixed,blocked):return fixed
    return simplify(pts)


def collisions(doc, edge, routed=True):
    pts=route_edge(doc,edge,repair=routed)
    if len(pts)<2:return {'heading':[], 'node':[], 'route':pts}
    headings=path_hits(pts,heading_rects(doc))
    blocked=node_rects(doc,{edge.get('from'),edge.get('to')})
    return {'heading':headings,'node':path_hits(pts,blocked),'route':pts}
