import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from tdaml import persistence, betti, features, NearestCentroid


class PersistenceTests(unittest.TestCase):
    def test_singleton_and_duplicates(self):
        for points in [[[0,0]],[[0,0],[0,0],[0,0]]]:
            result=persistence(points,0)
            self.assertEqual(result['intervals'],[{'dimension':0,'birth':0.0,'death':None,'alive_at_cutoff':True}])
            self.assertEqual(betti(result,0,0),1)

    def test_two_points_and_half_open_death(self):
        result=persistence([[0],[2]],2)
        self.assertEqual(betti(result,1.99,0),2)
        self.assertEqual(betti(result,2,0),1)
        self.assertEqual([i['death'] for i in result['intervals'] if i['death'] is not None],[2])

    def test_square_loop_birth_and_death(self):
        result=persistence([[0,0],[1,0],[1,1],[0,1]],2)
        loops=[i for i in result['intervals'] if i['dimension']==1]
        self.assertEqual(len(loops),1)
        self.assertEqual(loops[0]['birth'],1)
        self.assertAlmostEqual(loops[0]['death'],math.sqrt(2))
        self.assertEqual(betti(result,1.1,1),1)
        self.assertEqual(betti(result,math.sqrt(2),1),0)

    def test_triangle_fills_at_birth(self):
        result=persistence([[0,0],[1,0],[0.5,0.8]],2)
        self.assertEqual([i for i in result['intervals'] if i['dimension']==1],[])

    def test_truncation_censors_loop(self):
        result=persistence([[0,0],[1,0],[1,1],[0,1]],1.1)
        loop=next(i for i in result['intervals'] if i['dimension']==1)
        self.assertIsNone(loop['death']); self.assertTrue(loop['alive_at_cutoff'])
        with self.assertRaises(ValueError): betti(result,1.2,1)

    def test_h0_matches_independent_kruskal(self):
        rng=random.Random(9)
        for _ in range(20):
            points=[[rng.random(),rng.random()] for _ in range(6)]
            parent=list(range(6))
            def find(i):
                while parent[i]!=i: i=parent[i]
                return i
            expected=[]
            edges=sorted((math.dist(points[i],points[j]),i,j) for i in range(6) for j in range(i+1,6))
            for length,i,j in edges:
                a,b=find(i),find(j)
                if a!=b: parent[a]=b; expected.append(length)
            actual=sorted(i['death'] for i in persistence(points,2)['intervals'] if i['dimension']==0 and i['death'] is not None)
            self.assertEqual(actual,expected)

    def test_permutation_translation_and_scaling(self):
        points=[[0,0],[1,0],[1,1],[0,1]]
        result=persistence(points,2)
        moved=persistence([[p[1]+7,-p[0]+3] for p in reversed(points)],2)
        self.assertEqual(result['intervals'],moved['intervals'])
        scaled=persistence([[2*v for v in p] for p in points],4)
        for a,b in zip(result['intervals'],scaled['intervals']):
            self.assertAlmostEqual(2*a['birth'],b['birth'])
            if a['death'] is not None: self.assertAlmostEqual(2*a['death'],b['death'])

    def test_input_validation_and_cap(self):
        for points in [[],[[0],[1,2]],[[float('nan')]],[[True]],'bad']:
            with self.assertRaises(ValueError): persistence(points)
        with self.assertRaises(ValueError): persistence([[0]],-1)
        with self.assertRaises(ValueError): persistence([[0]]*60)


class FeatureAndModelTests(unittest.TestCase):
    def test_schema_and_finite_summaries(self):
        result=persistence([[0],[1]],2)
        vector=features(result,[0,1,2])
        self.assertEqual(len(vector['names']),len(vector['values']))
        mapped=dict(zip(vector['names'],vector['values']))
        self.assertEqual(mapped['H0_finite_total_persistence'],1)
        self.assertEqual(mapped['H0_finite_entropy'],0)
        self.assertEqual(mapped['H0_alive_at_cutoff_count'],1)
        self.assertEqual(len(vector['values']),14)
        self.assertTrue(all(math.isfinite(v) for v in vector['values']))
        for scales in [[],[1,0],[0,3]]:
            with self.assertRaises(ValueError): features(result,scales)

    def test_train_only_scaling(self):
        model=NearestCentroid().fit([[0,1],[2,1],[10,1],[12,1]],['a','a','b','b'])
        original_mean=list(model.mean)
        self.assertEqual(model.predict([[1,1],[11,1]]),['a','b'])
        model.predict([[10000,1]])
        self.assertEqual(model.mean,original_mean)
        self.assertEqual(model.scale[1],1)
        with self.assertRaises(ValueError): NearestCentroid().predict([[0]])
        with self.assertRaises(ValueError): model.predict([[0]])

    def test_reproducible_holdout_example(self):
        from examples.classify import demo
        first=demo(); second=demo()
        self.assertEqual(first,second)
        self.assertEqual(first['training_samples'],8)
        self.assertEqual(first['test_samples'],4)
        self.assertEqual(first['accuracy'],1.0)


class CliTests(unittest.TestCase):
    def test_exports(self):
        with tempfile.TemporaryDirectory() as d:
            report=Path(d)/'report.json'; svg=Path(d)/'barcode.svg'
            proc=subprocess.run([sys.executable,'-m','tdaml','examples/circle.json','--output',str(report),'--svg',str(svg)],capture_output=True,text=True,check=True)
            result=json.loads(proc.stdout)
            self.assertEqual(result,json.loads(report.read_text()))
            self.assertTrue(any(i['dimension']==1 for i in result['intervals']))
            ET.parse(svg)

    def test_invalid_scales(self):
        proc=subprocess.run([sys.executable,'-m','tdaml','examples/circle.json','--max-edge','0.1'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2)
        self.assertNotIn('Traceback',proc.stderr)


if __name__=='__main__': unittest.main()
