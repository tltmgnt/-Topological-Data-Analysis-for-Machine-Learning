"""Reproducible toy example; run python -m examples.classify from repository root."""
import json
import math
import random
from tdaml import persistence, features, NearestCentroid


def cloud(label, rng):
    if label=='ring':
        return [[math.cos(2*math.pi*i/12)+rng.uniform(-0.025,0.025),math.sin(2*math.pi*i/12)+rng.uniform(-0.025,0.025)] for i in range(12)]
    return [[rng.uniform(-0.3,0.3),rng.uniform(-0.3,0.3)] for _ in range(12)]


def demo(seed=42):
    rng=random.Random(seed); scales=[0.2,0.6,1.1,1.8]
    # Split sample identities before fitting the scaler or classifier.
    train=[(cloud(label,rng),label) for label in ['ring','blob'] for _ in range(4)]
    test=[(cloud(label,rng),label) for label in ['ring','blob'] for _ in range(2)]
    vector=lambda points:features(persistence(points,2),scales)['values']
    model=NearestCentroid().fit([vector(p) for p,_ in train],[label for _,label in train])
    truth=[label for _,label in test]; prediction=model.predict([vector(p) for p,_ in test])
    return {'seed':seed,'training_samples':len(train),'test_samples':len(test),'truth':truth,'predictions':prediction,
            'accuracy':sum(a==b for a,b in zip(truth,prediction))/len(test),
            'note':'Tiny synthetic demonstration, not evidence of real-world predictive performance'}


if __name__=='__main__': print(json.dumps(demo(),indent=2))
