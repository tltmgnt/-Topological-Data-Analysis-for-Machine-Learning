"""Bounded Vietoris-Rips persistence over GF(2), dimensions zero and one."""
from itertools import combinations
import math


def diagram(points, maximum):
    if not isinstance(points,list) or not 1<=len(points)<=24:
        raise ValueError('require 1..24 points')
    if not isinstance(points[0],list) or not 1<=len(points[0])<=4:
        raise ValueError('point dimension must be 1..4')
    dim=len(points[0])
    for p in points:
        if not isinstance(p,list) or len(p)!=dim or any(type(x) not in (int,float) or not math.isfinite(x) or abs(x)>1e6 for x in p):
            raise ValueError('bounded finite coordinates with matching dimensions required')
    if type(maximum) not in (int,float) or not math.isfinite(maximum) or not 0<=maximum<=1e7:
        raise ValueError('maximum edge length must be finite and in [0,1e7]')
    distances={edge:math.dist(points[edge[0]],points[edge[1]]) for edge in combinations(range(len(points)),2)}
    cells=[(0.0,(i,)) for i in range(len(points))]
    cells.extend((d,e) for e,d in distances.items() if d<=maximum)
    for tri in combinations(range(len(points)),3):
        radius=max(distances[e] for e in combinations(tri,2))
        if radius<=maximum:cells.append((radius,tri))
    cells.sort(key=lambda x:(x[0],len(x[1]),x[1]))
    index={cell:i for i,(_,cell) in enumerate(cells)}
    reduced,pivots,births,pairs={}, {},set(),{}
    for j,(_,cell) in enumerate(cells):
        column=set() if len(cell)==1 else {index[face] for face in combinations(cell,len(cell)-1)}
        while column and max(column) in pivots:
            column.symmetric_difference_update(reduced[pivots[max(column)]])
        reduced[j]=column
        if not column:births.add(j)
        else:
            pivot=max(column);pivots[pivot]=j;pairs[pivot]=j
    result=[]
    for i in sorted(births):
        birth,cell=cells[i];dimension=len(cell)-1
        if dimension>1:continue
        death=cells[pairs[i]][0] if i in pairs else None
        if death is None or death>birth:
            result.append({'dimension':dimension,'birth':birth,'death':death,'right_censored':death is None})
    return sorted(result,key=lambda x:(x['dimension'],x['birth'],float('inf') if x['death'] is None else x['death']))


def analyze(data):
    if not isinstance(data,dict) or set(data)!={'schema_version','points','max_edge_length'} or type(data['schema_version']) is not int or data['schema_version']!=1:
        raise ValueError('expected schema_version 1, points, max_edge_length')
    intervals=diagram(data['points'],data['max_edge_length'])
    return {'schema_version':1,'domain':'tda','field':'GF(2)','filtration':'Vietoris-Rips edge-length convention',
            'intervals':intervals,'betti_at_maximum':[sum(x['dimension']==d and x['death'] is None for x in intervals) for d in (0,1)],
            'finite_total_persistence':[sum(x['death']-x['birth'] for x in intervals if x['dimension']==d and x['death'] is not None) for d in (0,1)],
            'status':'PASS','execution_authorized':False,
            'scope':'H0/H1 of the supplied finite point-cloud filtration; unpaired intervals are right-censored at max_edge_length, not proven infinite. No H2, statistical significance, source authentication or generalization claim.'}
