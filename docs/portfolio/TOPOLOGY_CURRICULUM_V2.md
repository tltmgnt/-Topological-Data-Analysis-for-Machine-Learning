# Topology compatibility and curriculum v2 — -Topological-Data-Analysis-for-Machine-Learning

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | specialized mathematical tool |
| Minimum useful mathematics | Computational algebraic topology: bounded Vietoris–Rips persistence |
| Relationships to preserve | Filtration order, GF(2) boundaries, H0/H1 intervals and split isolation |
| Concrete operation / capstone | Trace a square before and after diagonals/triangles enter; explain an H1 birth, death and right-censored interval |
| Necessity and scope boundary | Use only the documented small point-cloud domain; no H2 or empirical learning benefit is established |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with computational algebraic topology: bounded vietoris–rips persistence and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify filtration order, gf(2) boundaries, h0/h1 intervals and split isolation. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain computational algebraic topology: bounded vietoris–rips persistence. | Trace a square before and after diagonals/triangles enter; explain an H1 birth, death and right-censored interval. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

The table is a guided selection of source lines, not an assertion that the whole repository is covered. Line numbers refer to the inspected source blob `a5d5aed1f934626e76e38522deedc8b3569ff848` in [tda_ml/analysis.py](../../tda_ml/analysis.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [1](../../tda_ml/analysis.py#L1) | `"""Bounded Vietoris-Rips persistence over GF(2), dimensions zero and one."""` | Explain the stated scope and identify a claim the implementation does not establish. |
| [2](../../tda_ml/analysis.py#L2) | `from itertools import combinations` | Identify the dependency and explain which operation needs it. |
| [3](../../tda_ml/analysis.py#L3) | `import math` | Identify the dependency and explain which operation needs it. |
| [6](../../tda_ml/analysis.py#L6) | `def diagram(points, maximum):` | State the input/output contract and trace one normal and one failing case. |
| [7](../../tda_ml/analysis.py#L7) | `if not isinstance(points,list) or not 1<=len(points)<=24:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [8](../../tda_ml/analysis.py#L8) | `raise ValueError('require 1..24 points')` | Construct the triggering input and explain why rejection preserves the contract. |
| [9](../../tda_ml/analysis.py#L9) | `if not isinstance(points[0],list) or not 1<=len(points[0])<=4:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [10](../../tda_ml/analysis.py#L10) | `raise ValueError('point dimension must be 1..4')` | Construct the triggering input and explain why rejection preserves the contract. |
| [11](../../tda_ml/analysis.py#L11) | `dim=len(points[0])` | Explain the statement, track its state change and predict its effect on the worked example. |
| [12](../../tda_ml/analysis.py#L12) | `for p in points:` | State the loop invariant, termination argument and one boundary case. |
| [13](../../tda_ml/analysis.py#L13) | `if not isinstance(p,list) or len(p)!=dim or any(type(x) not in (int,float) or not math.isfinite(x) or abs(x)>1e6 for x in p):` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [14](../../tda_ml/analysis.py#L14) | `raise ValueError('bounded finite coordinates with matching dimensions required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [15](../../tda_ml/analysis.py#L15) | `if type(maximum) not in (int,float) or not math.isfinite(maximum) or not 0<=maximum<=1e7:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [16](../../tda_ml/analysis.py#L16) | `raise ValueError('maximum edge length must be finite and in [0,1e7]')` | Construct the triggering input and explain why rejection preserves the contract. |
| [17](../../tda_ml/analysis.py#L17) | `distances={edge:math.dist(points[edge[0]],points[edge[1]]) for edge in combinations(range(len(points)),2)}` | Trace discovery order and state the reachability or shortest-path invariant. |
| [18](../../tda_ml/analysis.py#L18) | `cells=[(0.0,(i,)) for i in range(len(points))]` | State the loop invariant, termination argument and one boundary case. |
| [19](../../tda_ml/analysis.py#L19) | `cells.extend((d,e) for e,d in distances.items() if d<=maximum)` | Trace discovery order and state the reachability or shortest-path invariant. |
| [20](../../tda_ml/analysis.py#L20) | `for tri in combinations(range(len(points)),3):` | State the loop invariant, termination argument and one boundary case. |
| [21](../../tda_ml/analysis.py#L21) | `radius=max(distances[e] for e in combinations(tri,2))` | Trace discovery order and state the reachability or shortest-path invariant. |
| [22](../../tda_ml/analysis.py#L22) | `if radius<=maximum:cells.append((radius,tri))` | Trace both branches and identify the condition that changes the result. |
| [23](../../tda_ml/analysis.py#L23) | `cells.sort(key=lambda x:(x[0],len(x[1]),x[1]))` | Explain the statement, track its state change and predict its effect on the worked example. |
| [24](../../tda_ml/analysis.py#L24) | `index={cell:i for i,(_,cell) in enumerate(cells)}` | State the loop invariant, termination argument and one boundary case. |
| [25](../../tda_ml/analysis.py#L25) | `reduced,pivots,births,pairs={}, {},set(),{}` | Explain the statement, track its state change and predict its effect on the worked example. |
| [26](../../tda_ml/analysis.py#L26) | `for j,(_,cell) in enumerate(cells):` | State the loop invariant, termination argument and one boundary case. |
| [27](../../tda_ml/analysis.py#L27) | `column=set() if len(cell)==1 else {index[face] for face in combinations(cell,len(cell)-1)}` | State the loop invariant, termination argument and one boundary case. |
| [28](../../tda_ml/analysis.py#L28) | `while column and max(column) in pivots:` | State the loop invariant, termination argument and one boundary case. |
| [29](../../tda_ml/analysis.py#L29) | `column.symmetric_difference_update(reduced[pivots[max(column)]])` | Explain the statement, track its state change and predict its effect on the worked example. |
| [30](../../tda_ml/analysis.py#L30) | `reduced[j]=column` | Explain the statement, track its state change and predict its effect on the worked example. |
| [31](../../tda_ml/analysis.py#L31) | `if not column:births.add(j)` | Trace both branches and identify the condition that changes the result. |
| [32](../../tda_ml/analysis.py#L32) | `else:` | Trace both branches and identify the condition that changes the result. |
| [33](../../tda_ml/analysis.py#L33) | `pivot=max(column);pivots[pivot]=j;pairs[pivot]=j` | Explain the statement, track its state change and predict its effect on the worked example. |
| [34](../../tda_ml/analysis.py#L34) | `result=[]` | Explain the statement, track its state change and predict its effect on the worked example. |
| [35](../../tda_ml/analysis.py#L35) | `for i in sorted(births):` | State the loop invariant, termination argument and one boundary case. |
| [36](../../tda_ml/analysis.py#L36) | `birth,cell=cells[i];dimension=len(cell)-1` | Explain the statement, track its state change and predict its effect on the worked example. |
| [37](../../tda_ml/analysis.py#L37) | `if dimension>1:continue` | Trace both branches and identify the condition that changes the result. |
| [38](../../tda_ml/analysis.py#L38) | `death=cells[pairs[i]][0] if i in pairs else None` | Trace both branches and identify the condition that changes the result. |
| [39](../../tda_ml/analysis.py#L39) | `if death is None or death>birth:` | Trace both branches and identify the condition that changes the result. |
| [40](../../tda_ml/analysis.py#L40) | `result.append({'dimension':dimension,'birth':birth,'death':death,'right_censored':death is None})` | Explain the statement, track its state change and predict its effect on the worked example. |
| [41](../../tda_ml/analysis.py#L41) | `return sorted(result,key=lambda x:(x['dimension'],x['birth'],float('inf') if x['death'] is None else x['death']))` | Predict the returned value and distinguish a computed result from authorization. |
| [44](../../tda_ml/analysis.py#L44) | `def analyze(data):` | State the input/output contract and trace one normal and one failing case. |
| [45](../../tda_ml/analysis.py#L45) | `if not isinstance(data,dict) or set(data)!={'schema_version','points','max_edge_length'} or type(data['schema_version']) is not int or data['schema_version']!=1:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [46](../../tda_ml/analysis.py#L46) | `raise ValueError('expected schema_version 1, points, max_edge_length')` | Construct the triggering input and explain why rejection preserves the contract. |
| [47](../../tda_ml/analysis.py#L47) | `intervals=diagram(data['points'],data['max_edge_length'])` | Explain the statement, track its state change and predict its effect on the worked example. |
| [48](../../tda_ml/analysis.py#L48) | `return {'schema_version':1,'domain':'tda','field':'GF(2)','filtration':'Vietoris-Rips edge-length convention',` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [49](../../tda_ml/analysis.py#L49) | `'intervals':intervals,'betti_at_maximum':[sum(x['dimension']==d and x['death'] is None for x in intervals) for d in (0,1)],` | State the loop invariant, termination argument and one boundary case. |
| [50](../../tda_ml/analysis.py#L50) | `'finite_total_persistence':[sum(x['death']-x['birth'] for x in intervals if x['dimension']==d and x['death'] is not None) for d in (0,1)],` | State the loop invariant, termination argument and one boundary case. |
| [51](../../tda_ml/analysis.py#L51) | `'status':'PASS','execution_authorized':False,` | Explain the statement, track its state change and predict its effect on the worked example. |
| [52](../../tda_ml/analysis.py#L52) | `'scope':'H0/H1 of the supplied finite point-cloud filtration; unpaired intervals are right-censored at max_edge_length, not proven infinite. No H2, statistical significance, source authentication or generalization claim.'}` | Explain the statement, track its state change and predict its effect on the worked example. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_domain.py](../../tests/test_domain.py)
- [tests/test_researchos.py](../../tests/test_researchos.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. Use only the documented small point-cloud domain; no H2 or empirical learning benefit is established.
