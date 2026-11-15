"""Small train-only standardized nearest-centroid baseline for feature vectors."""
import math


class NearestCentroid:
    def fit(self, vectors, labels):
        if not isinstance(vectors,list) or not vectors or not isinstance(labels,list) or len(vectors)!=len(labels):
            raise ValueError('Provide nonempty vectors and one string label per vector')
        if any(not isinstance(label,str) or not label for label in labels): raise ValueError('Labels must be nonempty strings')
        self.dimension=len(vectors[0])
        self._validate(vectors)
        n=len(vectors)
        self.mean=[math.fsum(row[j]/n for row in vectors) for j in range(self.dimension)]
        self.scale=[math.sqrt(math.fsum((row[j]-self.mean[j])**2/n for row in vectors)) or 1.0 for j in range(self.dimension)]
        transformed=self._transform(vectors)
        self.centroids={}
        for label in sorted(set(labels)):
            selected=[row for row,l in zip(transformed,labels) if l==label]
            self.centroids[label]=[math.fsum(row[j]/len(selected) for row in selected) for j in range(self.dimension)]
        return self

    def _validate(self,vectors):
        if self.dimension<1 or any(not isinstance(row,(list,tuple)) or len(row)!=self.dimension or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in row) for row in vectors):
            raise ValueError('Feature vectors must share a nonzero dimension and have finite numeric values')

    def _transform(self,vectors):
        return [[(row[j]-self.mean[j])/self.scale[j] for j in range(self.dimension)] for row in vectors]

    def predict(self,vectors):
        if not hasattr(self,'centroids'): raise ValueError('Fit the classifier before prediction')
        self._validate(vectors)
        return [min(self.centroids,key=lambda label:math.dist(row,self.centroids[label])) for row in self._transform(vectors)]
