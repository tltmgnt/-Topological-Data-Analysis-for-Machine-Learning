"""Small matched leave-one-out comparison; descriptive research metrics only."""
import math
from .analysis import analyze


def compare(samples):
    if not isinstance(samples,list) or not 4<=len(samples)<=32:raise ValueError('require 4..32 samples')
    labels=[];topological=[];geometric=[]
    for sample in samples:
        if not isinstance(sample,dict) or set(sample)!={'id','label','cloud'} or not isinstance(sample['id'],str) or not sample['id'] or not isinstance(sample['label'],str) or not sample['label']:
            raise ValueError('exact id, label, cloud records required')
        if len(sample['id'])>64 or len(sample['label'])>64:raise ValueError('identifier too long')
        report=analyze(sample['cloud']);points=sample['cloud']['points']
        topological.append(report['finite_total_persistence']+[float(x) for x in report['betti_at_maximum']])
        ds=[math.dist(a,b) for i,a in enumerate(points) for b in points[i+1:]]
        geometric.append([sum(ds)/len(ds) if ds else 0,max(ds,default=0)])
        labels.append(sample['label'])
    if len({s['id'] for s in samples})!=len(samples):raise ValueError('sample IDs must be unique')
    classes=sorted(set(labels))
    if len(classes)!=2 or any(labels.count(c)<2 for c in classes):raise ValueError('exactly two labels with at least two samples each')
    def evaluate(features):
        predictions=[]
        for i,query in enumerate(features):
            train=[j for j in range(len(samples)) if j!=i]
            # Scaling learned only from training folds, separately for each feature family.
            means=[sum(features[j][k] for j in train)/len(train) for k in range(len(query))]
            scales=[max(abs(features[j][k]-means[k]) for j in train) or 1 for k in range(len(query))]
            centroids={c:[sum(features[j][k] for j in train if labels[j]==c)/sum(labels[j]==c for j in train) for k in range(len(query))] for c in classes}
            predictions.append(min(classes,key=lambda c:(sum(((query[k]-centroids[c][k])/scales[k])**2 for k in range(len(query))),c)))
        return {'predictions':predictions,'accuracy':sum(a==b for a,b in zip(labels,predictions))/len(labels)}
    return {'schema_version':1,'sample_ids':[s['id'] for s in samples],'labels':labels,
            'topological':evaluate(topological),'geometric_baseline':evaluate(geometric),
            'method':'leave-one-out nearest-centroid; training-only scaling; deterministic label tie-break',
            'independent_sample_origins_verified':False,'statistical_significance_established':False,
            'scope':'Descriptive supplied-data comparison; no held-out external study or scientific benefit established.'}
