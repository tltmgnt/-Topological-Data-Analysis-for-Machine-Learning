# Topological Data Analysis for Machine Learning

**TDAML** is a dependency-free Python toolkit for persistent H0/H1 of small point clouds, fixed-schema topological features, and an illustrative machine-learning workflow. It includes a transparent boundary-matrix reduction implementation, JSON reports, SVG barcodes, and a train-only standardized nearest-centroid baseline.

## Quick start

Requires Python 3.10 or newer. From the repository root:

```bash
python -m tdaml examples/circle.json --output output/report.json --svg output/barcode.svg
python -m tdaml examples/blob.json
python -m examples.classify
```

The CLI prints JSON and optionally writes a report and standalone SVG barcode. Blue bars represent H0 (components); red bars represent H1 (loops). Arrow-ended bars are still alive at the filtration cutoff. Open the SVG in a browser. Output parent directories are created; existing files are replaced.

Install the package to use the command:

```bash
python -m pip install .
tdaml --help
```

## Input and filtration settings

```json
{"points": [[0, 0], [1, 0], [1, 1], [0, 1]]}
```

Coordinates must be finite numeric arrays with a common dimension. Duplicate points are accepted as distinct vertices at distance zero. The metric is Euclidean distance in the supplied coordinates; features are not automatically normalized for units, point count, or sampling density.

```bash
python -m tdaml examples/circle.json --max-edge 1.2 --scales 0.2 0.6 1.0 1.2
```

`--max-edge` is the maximum **edge length**, not the radius of an offset ball. Default is 2.0. Feature scales default to 0.2, 0.6, 1.1, 1.8 and must be strictly increasing, nonnegative, and at most the cutoff. If changing the cutoff, adjust the scales when necessary.

## Python API

```python
from tdaml import persistence, betti, features, NearestCentroid

points = [[0, 0], [1, 0], [1, 1], [0, 1]]
report = persistence(points, max_edge=2)
print(report["intervals"])
print(betti(report, scale=1.1, dimension=1))  # 1
vector = features(report, scales=[0.2, 0.6, 1.1, 1.8])
print(vector["names"], vector["values"])

model = NearestCentroid().fit([[0, 1], [1, 1], [10, 2], [11, 2]], ["a", "a", "b", "b"])
print(model.predict([[0.5, 1], [10.5, 2]]))
```

## Persistent homology

For each threshold, the Vietoris–Rips complex includes an edge when its endpoint distance is at most the threshold, and a triangle when all three edges qualify. A simplex enters at its diameter. Vertices enter at zero. Simplices are sorted by filtration value, dimension, and vertex order so faces precede cofaces even at tied values.

The boundary matrix is reduced over GF(2) using binary columns and pivot elimination. Edges determine component mergers; triangle boundaries kill H1 cycles. The 2-skeleton suffices to compute persistent H0 and H1 of the full Rips filtration. Higher-dimensional homology is not reported.

Intervals use `[birth, death)` and zero-length intervals are omitted. For a unit square, the main loop is born at edge length 1 and dies at √2 when diagonal edges and triangles enter. A triangle has no positive-length H1 interval because its cycle is filled at birth.

A `null` death with `alive_at_cutoff: true` means the feature survives the **computed cutoff**. It is not a claim that a loop persists indefinitely in the full filtration. If the threshold reaches the point cloud's diameter, the full simplex is present, leaving one H0 class and no H1 classes. Increasing the cutoff can resolve previously censored deaths and change summary features.

## Fixed-schema features

For each dimension 0 and 1, features contain:

| Feature | Definition |
| --- | --- |
| Betti curve | Number of intervals alive at each supplied scale |
| Finite total persistence | Sum of death minus birth over finite intervals |
| Finite maximum persistence | Largest finite lifetime, or zero |
| Finite entropy | −Σ p log(p), where p is a finite lifetime divided by total finite persistence; zero when none exist |
| Alive-at-cutoff count | Number of intervals with unknown death beyond the cutoff |

For S scales, there are `2 × (S + 4)` numeric features, in the same order as the returned names. Intervals alive at the cutoff are excluded from finite-lifetime summaries; they remain represented by Betti values and the cutoff count. They are never assigned an invented finite death. These are cutoff-dependent features, not censored-data estimators.

Use identical ordered scales, cutoff, metric, preprocessing, and feature names for all samples. Fit coordinate preprocessing, feature standardization, feature selection, and any tuned scales on training data only. Split data at an appropriate independent subject/group level before model selection. This toolkit does not enforce a full experimental protocol for the caller.

## Machine-learning example

`python -m examples.classify` generates 12-point noisy rings and compact blobs with seed 42. It uses eight independent training clouds and four held-out test clouds. Cutoff and scales are fixed in advance. `NearestCentroid.fit` learns feature means and population standard deviations from training vectors only, then learns one centroid per class. Constant training features use scale 1. Predictions use Euclidean distance in standardized feature space; ties resolve by sorted string label.

The included fixture classifies all four held-out clouds correctly. This tiny, deliberately easy synthetic example is not a benchmark, evidence of generalization, or a demonstration that topology outperforms ordinary geometric features. Use broader datasets, baselines, grouped splits, and cross-validation for empirical claims. The classifier consumes numeric vectors and does not verify their feature metadata; callers must keep schemas aligned.

## Limits

Point clouds support 1–60 points and 1–100 coordinates per point. Filtrations are capped at 30,000 vertices/edges/triangles in total, so dense 60-point inputs can exceed the cap. Exact enumeration and matrix reduction are intended for small examples, not large-scale training pipelines. Distances and filtration values use floating-point arithmetic; near ties and extreme numeric ranges can be sensitive. No interval uncertainty or numerical error bound is provided.

There is no persistent H2, sparse approximation, distance-matrix input, persistent landscape/image transform, bottleneck distance, Mapper implementation, deep-learning integration, or trained production model. The implementation has analytic and independent H0 checks; it has not been cross-validated against an external persistence package.

## Development and verification

```bash
python -m unittest discover -s tests -v
```

The 13 tests cover known square/triangle barcodes, half-open intervals, duplicates, cutoff censoring, H0 against an independent Kruskal minimum-spanning-tree computation on 20 random clouds, geometric invariance and scaling, feature schemas, train-only scaling, reproducible held-out classification, input limits, and CLI JSON/SVG exports. CI installs the package and runs tests and examples on Python 3.10, 3.12, and 3.13.

Licensed under Apache 2.0; see [LICENSE](LICENSE).

## ResearchOS / TECT assurance layer

This repository includes the shared v0.1 research controller, a scoped executable domain pilot, replayable evidence/decision bundles, adversarial regression probes, and explicit unassured outcomes. See [the workflow](docs/RESEARCHOS.md), [versioned semantics](docs/TECT_SPEC.md), and [research-program traceability](docs/TECT_RESEARCH_PLAN.md). Existing domain results retain their documented limits. No claim state authorizes external or clinical execution.
