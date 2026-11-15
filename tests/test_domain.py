import copy,itertools,json,math,tempfile,unittest
from pathlib import Path
from tda_ml import analyze
from tda_ml.learning import compare
from tda_ml.io import create,verify,load

def cloud(points,r=2):return {'schema_version':1,'points':points,'max_edge_length':r}

class DomainTests(unittest.TestCase):
    def test_square_barcode(self):
        r=analyze(cloud([[0,0],[1,0],[1,1],[0,1]]))
        h1=[x for x in r['intervals'] if x['dimension']==1]
        self.assertEqual(len(h1),1);self.assertEqual(h1[0]['birth'],1);self.assertAlmostEqual(h1[0]['death'],math.sqrt(2))
        self.assertEqual(r['betti_at_maximum'],[1,0])
    def test_triangle_zero_lifetime_omitted(self):
        self.assertEqual(analyze(cloud([[0,0],[1,0],[0,1]]))['betti_at_maximum'],[1,0])
        self.assertFalse(any(x['dimension']==1 for x in analyze(cloud([[0,0],[1,0],[0,1]]))['intervals']))
    def test_censored_square(self):
        r=analyze(cloud([[0,0],[1,0],[1,1],[0,1]],1))
        self.assertEqual(r['betti_at_maximum'],[1,1]);self.assertTrue(all(x['right_censored'] for x in r['intervals'] if x['dimension']==1))
    def test_duplicate_points(self):self.assertEqual(analyze(cloud([[0],[0],[0]],0))['betti_at_maximum'],[1,0])
    def test_disconnected_points(self):self.assertEqual(analyze(cloud([[0],[2],[4]],1))['betti_at_maximum'],[3,0])
    def test_isometry_permutation(self):
        p=[[0,0],[1,0],[1,1],[0,1]];q=[[5-y,7+x] for x,y in reversed(p)]
        self.assertEqual(analyze(cloud(p))['intervals'],analyze(cloud(q))['intervals'])
    def test_scaling(self):
        p=[[0,0],[1,0],[1,1],[0,1]]
        a=analyze(cloud(p));b=analyze(cloud([[2*x,2*y] for x,y in p],4))
        for x,y in zip(a['intervals'],b['intervals']):
            self.assertEqual(y['birth'],2*x['birth'])
            if x['death'] is not None:self.assertEqual(y['death'],2*x['death'])
    def test_exhaustive_small_cloud_rank_oracle(self):
        # Independent graph connectivity and enumerated triangle-boundary span oracle.
        universe=[[x,y] for x in range(3) for y in range(2)]
        for size in range(1,5):
            for ps in itertools.combinations(universe,size):
                for r in [0,1,1.5,3]:
                    edges=[e for e in itertools.combinations(range(size),2) if math.dist(ps[e[0]],ps[e[1]])<=r]
                    groups=[{i} for i in range(size)]
                    for a,b in edges:
                        merged=set().union(*(g for g in groups if a in g or b in g));groups=[g for g in groups if a not in g and b not in g]+[merged]
                    span={0}
                    for tri in itertools.combinations(range(size),3):
                        if all(e in edges for e in itertools.combinations(tri,2)):
                            column=sum(1<<edges.index(e) for e in itertools.combinations(tri,2));span|={x^column for x in list(span)}
                    rank=len(span).bit_length()-1
                    expected=[len(groups),len(edges)-size+len(groups)-rank]
                    self.assertEqual(analyze(cloud(list(ps),r))['betti_at_maximum'],expected)
    def test_learning_balanced_and_label_swap(self):
        samples=[{'id':str(i),'label':'a' if i<2 else 'b','cloud':cloud([[0],[1+i]])} for i in range(4)]
        r=compare(samples);self.assertEqual(len(r['topological']['predictions']),4);self.assertFalse(r['statistical_significance_established'])
        with self.assertRaises(ValueError):compare(samples+samples)
    def test_limits_and_nonfinite(self):
        for d in [cloud([]),cloud([[True]]),cloud([[1],[1,2]]),cloud([[float('inf')]]),cloud([[0]],float('nan')),cloud([[0]]*25)]:
            with self.assertRaises(ValueError):analyze(d)
    def test_replay_and_forgery(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';create(p,cloud([[0],[1]]));self.assertEqual(verify(p)['betti_at_maximum'],[1,0])
            (p/'report.json').write_text('{}')
            with self.assertRaises(ValueError):verify(p)
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x'
            for raw in ['{"a":1,"a":2}','NaN','1e400']:
                p.write_text(raw)
                with self.assertRaises(ValueError):load(p)
