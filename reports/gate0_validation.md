> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Gate 0 oracle and provenance validation

**Verdict: CONDITIONAL — fixable limitations remain.**

Date: 2026-10-21 (Asia/Shanghai). Scope: independent CPU oracle and pinned-source inspection only. No world-model inference, checkpoint access, training, paid API or GPU work was performed. Gate 1 has not been executed or authorized.

## Evidence for this verdict

The numerical separation criterion is met: **12/16 frozen test states** have a Q* spread above **.005 m²**; the same count holds at .0025 and .01. The float64 oracle is validated by **16 successful tests**, including an independently written scalar reference, all 4,096 branches for two nontrivial queries, all 120 state/action worst-case witnesses, update order, signs, initial/boundary inclusion, probability factorization, angle invariance and sign symmetry. The H=16 fallback was therefore **not triggered and not run**. [E]

The scientific limitation is more specific than insufficient spread: **A0 is in the best set for all 12 informative test states, and constant A0 is within every practical margin in all 16 states**. Constant A0 has mean regret **1.28489505412e-05 m²** and maximum regret **0.000176067136293 m²**, below even .0025. Thus the frozen setup can expose action-ordering errors and harmful action choices, but offers weak evidence about state-dependent optimal-action selection. This is a design limitation observed before any learned-model comparison, not a finding about StressDream. [E; interpretation]

The fix is to retain the frozen states, include a constant-A0 comparator, and explicitly limit any future use to action-ranking/error diagnostics. A claim about nontrivial state-dependent decisions would require a separately authorized, newly preregistered design; no such redesign or favorable state selection occurred here. The preregistered spread rule is not changed: it is satisfied. The conditional verdict concerns the scientific interpretation of downstream decision selection, not a retrospective replacement of that numerical rule. Pending checkpoint/readout/runtime checks belong to Gate 1 and are not presented as failures of this oracle.

## Frozen configuration and mathematical conventions

- Physical dynamics: v=1 m/s, dt=.05 s, radius=.25 m, centered at (0,0), |a|<=1.25 rad/s.
- H=12, time points t=0..12, 0.6s. Every one of **4,096 sign strings** is enumerated per query. All **24 contexts ×5 actions=120 queries**, or **491,520 branch/query combinations**, are retained, including calibration cases. Sixteen test contexts contribute 80 queries and 327,680 combinations.
- Contexts: x=-rho, y=0; rho∈{.35,.45,.60,.75}; beta∈{0,.2,.4,.6,.8,1.0}. beta=.2,.8 are the eight calibration contexts; the other sixteen remain frozen test cases.
- A0: zero; A1: +.625 throughout; A2: +1.25 throughout; A3: +1.25 for first6 then zero; A4: zero then +1.25 for last6. Actions are rad/s and fixed before execution.
- Positions use **theta_t**, then theta_(t+1)=theta_t+.05 delta_t a_t. Disturbance bit t of a branch ID is least-significant-bit-first: zero bit means +1, one bit means -1. Angles are unwrapped in the implementation; periodic equivalence was tested.
- C=x²+y²-r², unsafe C<=0. Q*=min_branch min_time C; larger Q* is safer. Source learned danger margin m=-C, so worst danger is -Q*. Oracle regret of choosing a is max_a' Q*(a')-Q*(a), nonnegative. All units are m² except angles and positions as labeled.
- Exact support is independent of p for 0<p<1. Both p=.2 and .4 product probabilities are saved for secondary failure-probability summaries; they must not be conflated with worst-case action scores.
- Exhaustive discrete support is evaluated in float64, **not certified exact-real or continuous-time reachability**. The code does not check swept collisions between time samples, which are outside the declared discrete system.

All frozen H=12 paths stay inside the generator's +/-1.4m bounds because rho+vHdt<=1.35m. No termination discrepancy affects these queries. The 4,096 sign strings are not necessarily 4,096 distinct spatial futures: zero-action steps and the last turn can leave safety paths unchanged. No Monte Carlo sampling or random seed is needed.

Config SHA-256: `ea903212f8f0b66f92f401befe0890e03391a0f975a5418b62b05818b5af0097`. It was written before the oracle run. The H=16 contingency was frozen using the same contexts and an eight-step A3/A4 switch; since the trigger is false it has no measured results. The earlier proposal's unspecified alternative fallback pool was not instantiated or searched.

## Action separation results

| Separation margin (m²) | Informative test states /16 | Separated pairs /160 | At/below margin (includes numeric ties) |
|---:|---:|---:|---:|
| 0.0025 | 12 | 108 | 52 |
| 0.005 | 12 | 106 | 54 |
| 0.01 | 12 | 94 | 66 |

Strict rule: spread or pairwise absolute difference must be **greater than** the stated margin. Numeric ties use |difference|<=1e-12, distinct from practical near-ties. There are **12 numerically tied pairs** among the 160 test pairs. At .005, **54/160** pairs are at or below the margin (12 numeric ties plus 42 additional near-ties).

All Q* values below are m², rounded to nine decimals only for display. CSV/NPZ retain float64 round-trip precision. Best sets use numerical tolerance, not the .005 practical margin.

| ID | rho | beta | A0 | A1 | A2 | A3 | A4 | Spread | Best set (1e-12) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C00 | 0.35 | 0.0 | -0.062500000 | -0.062497554 | -0.062490161 | -0.062490161 | -0.062500000 | 0.000009839 | A2|A3 |
| C02 | 0.35 | 0.4 | -0.043422809 | -0.051122142 | -0.057024657 | -0.057024657 | -0.043422809 | 0.013601848 | A0|A4 |
| C03 | 0.35 | 0.6 | -0.023320479 | -0.032042966 | -0.042102492 | -0.042102492 | -0.023320479 | 0.018782013 | A0|A4 |
| C05 | 0.35 | 1.0 | +0.024357677 | +0.018913245 | +0.010193228 | +0.010193228 | +0.024357677 | 0.014164449 | A0|A4 |
| C06 | 0.45 | 0.0 | -0.062500000 | -0.062499990 | -0.062499848 | -0.062490161 | -0.062490238 | 0.000009839 | A3 |
| C08 | 0.45 | 0.4 | -0.031581958 | -0.047329553 | -0.057977205 | -0.056651581 | -0.033755873 | 0.026395247 | A0 |
| C09 | 0.45 | 0.6 | +0.002519281 | -0.017807222 | -0.038433594 | -0.035225534 | +0.001296334 | 0.040952876 | A0 |
| C11 | 0.45 | 1.0 | +0.080931981 | +0.066807840 | +0.043746282 | +0.045665284 | +0.080931981 | 0.037185699 | A0|A4 |
| C12 | 0.6 | 0.0 | -0.062500000 | -0.062499979 | -0.062499657 | -0.062490161 | -0.062490161 | 0.000009839 | A3|A4 |
| C14 | 0.6 | 0.4 | -0.007900256 | -0.043942547 | -0.061195223 | -0.056068531 | -0.025678211 | 0.053294966 | A0 |
| C15 | 0.6 | 0.6 | +0.052298631 | +0.002117719 | -0.039341087 | -0.023019654 | +0.032870174 | 0.091639718 | A0 |
| C17 | 0.6 | 1.0 | +0.192991170 | +0.153672415 | +0.083789683 | +0.110403369 | +0.192991170 | 0.109201487 | A0|A4 |
| C18 | 0.75 | 0.0 | -0.040000000 | -0.039956037 | -0.039823933 | -0.039902299 | -0.039902299 | 0.000176067 | A2 |
| C20 | 0.75 | 0.4 | +0.031045105 | -0.015760667 | -0.034275558 | -0.030383263 | +0.007083443 | 0.065320664 | A0 |
| C21 | 0.75 | 0.6 | +0.117197947 | +0.041814666 | -0.006938875 | +0.010927832 | +0.080268925 | 0.124136822 | A0 |
| C23 | 0.75 | 1.0 | +0.335818616 | +0.250732878 | +0.146974587 | +0.191358474 | +0.315240612 | 0.188844029 | A0 |

Non-informative cases are C00,C06,C12,C18 (all beta=0), and all remain in the outputs. The safe/unsafe distinction is also not uniform: **49/80 test queries** can fail, **31/80** are robust-safe; **4/16 contexts** have both safe and unsafe alternatives. Eight contexts have all five actions potentially unsafe and four have all five safe. No test Q* is boundary-ambiguous at 1e-12; smallest |Q*| is 0.00129633389299 m².

| Context | Numerically tied pairs |
|---|---|
| C00 | A0=A4, A2=A3 |
| C02 | A0=A4, A2=A3 |
| C03 | A0=A4, A2=A3 |
| C05 | A0=A4, A2=A3 |
| C11 | A0=A4 |
| C12 | A3=A4 |
| C17 | A0=A4 |
| C18 | A3=A4 |

Every pair's signed and absolute Q* difference is in `raw/PAIRWISE_ACTION_DIFFERENCES.csv`. Every action's robust regret, exact-support label, near-optimal flags and witness ID/sign string is in `ACTION_SEPARATION_RESULTS.csv`. `raw/WORST_CASE_WITNESSES.csv` contains all 13 states of all 120 selected witnesses (1,560 rows), with both safety C and danger margin -C.

## Oracle validity, numerical accuracy and actual execution

The successful execution used Python 3.13.5 ([LOCAL_PATH_REDACTED] NumPy 2.1.3, CPU only, one BLAS/OpenMP thread. The recorded horizon run took **0.254790 seconds**, including numerical aggregation, witness construction and NPZ writing; it excludes interpreter startup, unit tests and report generation. This is a single-run CPU-oracle timing, not a world-model runtime estimate.

All 120 witnesses match the vector oracle exactly in its internal replay; independent scalar replay from delivered CSV has maximum residual **0 m²**. Product probability mass sums are 1.0000000000000007 at p=.2 and 1.0 at p=.4, a float64 roundoff effect. Raw probabilities slightly above one by this tolerance were preserved, not silently clipped. No fabricated uncertainty intervals are needed for exhaustive enumeration of a fixed finite pool; generalization beyond this pool is unmeasured.

An initial attempt computed H=12 but stopped while serializing a NumPy integer in the summary. The numerical recurrence and frozen configuration were unchanged; the pair-count conversion was corrected to Python integer, a serialization integration test was added, all 16 tests rerun, and the full export completed. The initial traceback is retained as `raw/ORACLE_RUN_FAILED_SERIALIZATION.log`. Final results refer only to the successful run and final implementation hash.

## Provenance conclusions

See `PROVENANCE_MATRIX.md` for immutable line links and exact values. Verified issues are p=.2 paper versus .4 generator; deterministic demo GT; momentum .9 versus no momentum in B.5; zero explicit isotropy coefficient despite full-regularizer mode; concrete formula/threshold differences; pre-update score versus post-update sample association; and loose/conditional checkpoint loading. Their effect on learned predictions was not measured.

The source checksum comparison confirms **87/87 present tracked files unchanged**, HEAD `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`, clean status before/after. Original reports, all other projects and sparse-excluded weights were untouched. The oracle imports NumPy and standard-library code only; execution metadata records `torch_imported=false`.

## Artifact map and reproduction

Required deliverables: `ORACLE_IMPLEMENTATION.py`, `ORACLE_UNIT_TESTS.py`, `ACTION_SEPARATION_RESULTS.csv`, `PROVENANCE_MATRIX.md`, `GATE0_VALIDATION_REPORT.md`, `GATE1_READINESS.md`.

Supporting evidence: `CONFIG.json`; raw pairwise/context/witness CSVs; compressed per-branch minima/probability weights (`allow_pickle=False` readable); successful and failed execution logs; execution metadata; input/source/output validation hashes; and `SHA256SUMS.json`.

Physical directory: `[LOCAL_PATH_REDACTED]`.

App-facing path is the same directory through the existing workspace output junction: `[LOCAL_PATH_REDACTED]`.

Exact PowerShell execution commands are retained in `raw/EXECUTION_COMMANDS.ps1`. To reproduce without replacing this frozen run, copy the two oracle Python files plus CONFIG.json into a new isolated directory and use that directory in Set-Location. The original config freeze command uses exclusive file creation and deliberately refuses to overwrite CONFIG.json.

```powershell
Set-Location -LiteralPath '[LOCAL_PATH_REDACTED]'
$env:PYTHONIOENCODING='utf-8'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
& '[LOCAL_PATH_REDACTED]' -B '.\ORACLE_IMPLEMENTATION.py' --freeze-config '.\CONFIG.json'
& '[LOCAL_PATH_REDACTED]' -B '.\ORACLE_UNIT_TESTS.py'
& '[LOCAL_PATH_REDACTED]' -B '.\ORACLE_IMPLEMENTATION.py' --config '.\CONFIG.json' --output-dir '.'
```

For replay of an existing frozen config, skip the freeze command. Logs include exact successful outputs. `raw/BUILD_REPORTS.py` checks raw CSV against NPZ and independently replays all witnesses before building these reports. Hashes in SHA256SUMS.json cover all delivered evidence except that manifest itself; the manifest lists its exclusion explicitly to avoid a circular self-hash.

**Stop after Gate 0. Gate 1 remains unexecuted and requires explicit authorization.**
