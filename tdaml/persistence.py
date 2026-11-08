"""Small Vietoris–Rips filtrations and persistent H0/H1 over GF(2)."""
import itertools
import math


def point_cloud(points):
    if not isinstance(points,(list,tuple)) or not 1<=len(points)<=60:
        raise ValueError('Point clouds must have 1 to 60 points')
    result=[]; dimension=None
    for p in points:
        if not isinstance(p,(list,tuple)) or not p or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in p):
            raise ValueError('Points must be nonempty finite numeric coordinate arrays')
        if dimension is None: dimension=len(p)
        if len(p)!=dimension or dimension>100:
            raise ValueError('Points must share a dimension, at most 100')
        result.append(tuple(float(v) for v in p))
    return result


def persistence(points, max_edge=2.0):
    """Edge threshold is Euclidean distance, not ball radius. Includes triangles.

    Zero-length intervals are omitted. Null deaths mean alive at the cutoff,
    not a claim of infinite persistence in an untruncated complex.
    """
    points=point_cloud(points)
    if isinstance(max_edge,bool) or not isinstance(max_edge,(int,float)) or not math.isfinite(max_edge) or max_edge<0:
        raise ValueError('max_edge must be finite and nonnegative')
    distances={}
    simplices=[(0.0,0,(i,)) for i in range(len(points))]
    for i,j in itertools.combinations(range(len(points)),2):
        distance=math.dist(points[i],points[j])
        if not math.isfinite(distance): raise ValueError('Coordinate range exceeds finite distance arithmetic')
        distances[(i,j)]=distance
        if distance<=max_edge: simplices.append((distance,1,(i,j)))
    for i,j,k in itertools.combinations(range(len(points)),3):
        diameter=max(distances[(i,j)],distances[(i,k)],distances[(j,k)])
        if diameter<=max_edge: simplices.append((diameter,2,(i,j,k)))
    if len(simplices)>30000: raise ValueError('Filtration exceeds 30000 simplices; reduce point count or max_edge')
    simplices.sort() # filtration, dimension, lexicographic vertices: faces precede cofaces
    indices={vertices:i for i,(_,_,vertices) in enumerate(simplices)}
    pivots={}; births=set(); paired={}
    for index,(_,dimension,vertices) in enumerate(simplices):
        boundary=0
        if dimension:
            for face in itertools.combinations(vertices,dimension): boundary ^= 1<<indices[face]
        while boundary:
            pivot=boundary.bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=boundary; paired[pivot]=index; break
            boundary ^= pivots[pivot]
        if not boundary: births.add(index)
    intervals=[]
    for index in sorted(births):
        birth,dimension,_=simplices[index]
        if dimension>1: continue
        death=simplices[paired[index]][0] if index in paired else None
        if death is not None and death==birth: continue
        intervals.append({'dimension':dimension,'birth':birth,'death':death,
                          'alive_at_cutoff':death is None})
    intervals.sort(key=lambda d:(d['dimension'],d['birth'],math.inf if d['death'] is None else d['death']))
    return {'point_count':len(points),'ambient_dimension':len(points[0]),
            'max_edge':float(max_edge),'simplex_count':len(simplices),
            'coefficient_field':'GF(2)','complex':'Vietoris–Rips through dimension 2',
            'interval_convention':'[birth, death); zero-length intervals omitted',
            'intervals':intervals}


def betti(report, scale, dimension):
    if not isinstance(scale,(int,float)) or not math.isfinite(scale) or not 0<=scale<=report['max_edge']:
        raise ValueError('scale must lie within the computed filtration')
    if dimension not in (0,1): raise ValueError('Only dimensions 0 and 1 are available')
    return sum(i['dimension']==dimension and i['birth']<=scale and (i['death'] is None or scale<i['death']) for i in report['intervals'])


def features(report, scales):
    """Fixed-schema Betti curves plus finite-lifetime and cutoff summaries.

    All samples must use identical scales/max_edge to be comparable.
    """
    if not isinstance(scales,(list,tuple)) or not scales:
        raise ValueError('scales must be a nonempty numeric array')
    if any(isinstance(s,bool) or not isinstance(s,(int,float)) or not math.isfinite(s) or not 0<=s<=report['max_edge'] for s in scales):
        raise ValueError('Every scale must lie within the computed filtration')
    if any(a>=b for a,b in zip(scales,scales[1:])): raise ValueError('scales must be strictly increasing')
    names=[]; values=[]
    for dimension in (0,1):
        for scale in scales:
            names.append(f'H{dimension}_betti_at_{float(scale)!r}'); values.append(float(betti(report,scale,dimension)))
        intervals=[i for i in report['intervals'] if i['dimension']==dimension]
        lifetimes=[i['death']-i['birth'] for i in intervals if i['death'] is not None]
        total=math.fsum(lifetimes)
        entropy=-math.fsum((v/total)*math.log(v/total) for v in lifetimes) if total else 0.0
        for name,value in [('finite_total_persistence',total),('finite_max_persistence',max(lifetimes,default=0.0)),('finite_entropy',entropy),('alive_at_cutoff_count',sum(i['death'] is None for i in intervals))]:
            names.append(f'H{dimension}_{name}'); values.append(float(value))
    return {'names':names,'values':values,'scales':list(scales),'max_edge':report['max_edge']}


def barcode_svg(report):
    intervals=report['intervals']; width=800; height=max(100,50+22*len(intervals))
    cutoff=report['max_edge']; scale=680/(cutoff or 1)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><title>Persistence barcode; arrows mark intervals alive at the filtration cutoff</title><rect width="100%" height="100%" fill="white"/>',f'<text x="80" y="20" font-size="14">0</text><text x="700" y="20" font-size="14">cutoff {cutoff:g}</text>']
    for index,interval in enumerate(intervals):
        y=45+22*index; color='#2563eb' if interval['dimension']==0 else '#dc2626'
        start=80+interval['birth']*scale
        end=80+(cutoff if interval['death'] is None else interval['death'])*scale
        parts.append(f'<text x="20" y="{y+4}" font-size="12">H{interval["dimension"]}</text><line x1="{start}" y1="{y}" x2="{end}" y2="{y}" stroke="{color}" stroke-width="4"/>')
        if interval['death'] is None: parts.append(f'<path d="M {end-6} {y-5} L {end} {y} L {end-6} {y+5}" fill="none" stroke="{color}" stroke-width="2"/>')
    return ''.join(parts)+'</svg>\n'
