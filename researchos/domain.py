"""Scoped synthetic domain adapter; no external execution."""
import math
from tdaml import persistence, features

def check():
    points=[[0,0],[1,0],[1,1],[0,1]]; report=persistence(points,2)
    loops=[i for i in report['intervals'] if i['dimension']==1]
    passed=len(loops)==1 and loops[0]['birth']==1 and abs(loops[0]['death']-math.sqrt(2))<1e-12
    return {'domain':'topological-machine-learning','statement':'The unit-square Rips filtration has one positive H1 interval from 1 to sqrt(2).',
            'passed':passed,'configuration':{'points':points,'max_edge':2},
            'observed':{'persistence':report,'features':features(report,[0,1,1.2,2])},
            'scope':'Known analytic software fixture; no ML generalization or independent benchmark claim'}
