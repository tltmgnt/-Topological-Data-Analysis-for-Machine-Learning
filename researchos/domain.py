"""Executable synthetic domain adapter, not independent scientific reproduction."""
from tda_ml import analyze
DATA={'schema_version': 1, 'points': [[0, 0], [1, 0], [1, 1], [0, 1]], 'max_edge_length': 2}

def check():
    result=analyze(DATA)
    return {'domain':result['domain'],'statement':'The supplied synthetic bounded tda and machine learning fixture satisfies its declared reference checks.','passed':bool(result["betti_at_maximum"]==[1,0] and len([x for x in result["intervals"] if x["dimension"]==1])==1),
            'configuration':DATA,'observed':result,'scope':'Exact GF(2) Vietoris–Rips H0/H1 persistence for at most 24 points in 1–4 dimensions. Filtration uses maximum edge length. Triangles suffice to compute H1; H2 is deliberately omitted. Unpaired intervals are right-censored, not proven infinite. A deterministic matched leave-one-out nearest-centroid comparison uses training-only feature scaling. No external empirical benefit is established.'}
