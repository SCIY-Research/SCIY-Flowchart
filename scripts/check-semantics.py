#!/usr/bin/env python3
"""Check declared scientific graph assertions; never hallucinate scientific causality.
Scientific accuracy ultimately requires source-based human review.

Optional doc.semantic_assertions:
 {"required_edges": [["a","b"]], "forbidden_edges": [["train","test"]],
  "parallel_branches": [["baseline","autoencoder","mixup"]],
  "required_nodes": ["validation"]}
"""
import argparse,json,sys
from pathlib import Path

def audit(doc):
    asserts=doc.get('semantic_assertions') or {}
    edges={(e.get('from'),e.get('to')) for e in doc.get('edges',[])}
    ids={n.get('id') for n in doc.get('nodes',[])}
    errors=[];warnings=[]
    for item in asserts.get('required_nodes',[]):
        if item not in ids:errors.append(f'missing required node {item}')
    for source,target in asserts.get('required_edges',[]):
        if (source,target) not in edges:errors.append(f'missing required dependency {source} -> {target}')
    for source,target in asserts.get('forbidden_edges',[]):
        if (source,target) in edges:errors.append(f'prohibited dependency {source} -> {target}')
    for branch in asserts.get('parallel_branches',[]):
        for a in branch:
            for b in branch:
                if a!=b and (a,b) in edges:
                    errors.append(f'parallel alternatives incorrectly linked: {a} -> {b}')
    if not asserts:
        warnings.append('No semantic_assertions supplied: scientific graph must be verified against original source.')
    return errors,warnings

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args()
    errs,warns=audit(json.loads(Path(a.input).read_text(encoding='utf-8')))
    for v in errs:print('ERROR:',v)
    for v in warns:print('WARNING:',v)
    print(f'Semantic check: {len(errs)} error(s), {len(warns)} warning(s)')
    sys.exit(bool(errs))
