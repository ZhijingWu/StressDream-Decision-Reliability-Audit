> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Gate 0B independent test specification

Status: frozen before held-out generation. This is a new task benchmark; original Gate 0 remains unchanged.

## Final immutable specification

The authoritative machine-readable file is `FROZEN_TEST_SPEC_V3.json`, SHA-256 `07d19464db19d088049d6ee1c3f565805f50105733523301e62354c5d63f5397`. Physical source revision: `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`. Selected design: `D2_progress_safe_mixed`.

Physical dynamics are unchanged: speed 1 m/s, dt=.05 s, center (0,0), obstacle radius .25 m. Position uses the old heading, then theta advances by dt*delta*a. Float64 exhaustive enumeration covers 4,096 independent-sign strings at H=12 (0.6 s). All time points t=0..12, including the initial state, enter the safety minimum. Support failures include C=0.

## Generator and split

There are 64 held-out contexts; no acceptance/rejection sampling, outcome filtering, threshold-based selection or model-based selection occurs. Generate with NumPy `Generator(PCG64(202610299))`:

1. For i=0..63, set phi_i=(i mod4)*pi/2+Uniform[0,pi/2), obtaining sixteen contexts per quadrant.
2. Independently draw rho_i~Uniform[.35,.75] m and e_i~Uniform[-1.4,1.4] rad.
3. Set x_i=rho_i*cos(phi_i), y_i=rho_i*sin(phi_i), theta_i=(phi_i+pi+e_i) mod2pi.
4. Permute context order with the same RNG and label T000..T063. Retain every context, including all-action-infeasible, ties and near-ties. The goal is g=(1,0) m for every context.

These are physical prior restrictions, not assertions that the released checkpoint contains these exact examples. All initial states are outside the obstacle by construction. For H=12, rho+vHdt<=1.35<1.4m bounds every path coordinate within the released training-generator termination region, independent of the disturbance sequence. No test scene is changed after evaluation.

Design/calibration used 32 contexts per pool, separately seeded: mixed=202610210 and oblique=202610211. The latter pool uses rho in [.60,.75] and e=independent fair sign*Uniform[.8,1.4]. The design stage compared four alternatives plus one disclosed amendment, all in design data. Final test seed202610299 is unused by either design generator. It supersedes an initially proposed test seed that collided with the oblique design seed; this correction happened before any held-out state generation. See `PRETEST_SEED_CORRECTION.json`. No design instance is carried into the test pool.

## Fixed candidates

The five open-loop sequences are constant over all twelve steps:

| ID | Angular rate (rad/s) |
|---|---:|
| A0 | 0 |
| Lhalf | -.625 |
| Lfull | -1.25 |
| Rhalf | +.625 |
| Rfull | +1.25 |

Names are only IDs: mathematically positive rate increases theta and is a counterclockwise turn; negative decreases theta. “L/R” is not relied on as a physical orientation label. No speed control, feedback or new world-model input is added.

## Risk functional and changed task objective

Let C(s)=x²+y²-.25². Compute Q*(s,a)=min_delta min_t C(s_t). The safe candidate set is F(s)={a:Q*(s,a)>0}. This is the same support-worst-case safety constraint as the Gate 0 oracle.

**D2 changes the decision objective.** Among safe candidates maximize expected squared-distance goal progress:

P_p(s,a)=||pos(s)-g||² - sum_delta Pr_p(delta)*||pos(s_H(a,delta))-g||².

Pr_p(delta)=p^(number of minus signs)*(1-p)^(number of plus signs), with independent flips. Primary p=.2 follows paper Eq.9; p=.4 is a separately reported provenance sensitivity. Expectations are exact finite weighted sums in float64, not Monte Carlo estimates. The released checkpoint's actual training p remains unresolved.

For common-denominator regret and constant-policy comparison use U_p(s,a)=P_p(s,a) if Q*>0, otherwise -4 m². The -4 encoding expresses a hard constraint, rather than a tuned tradeoff: |P_p|<=2*d0*L+L²<=2*1.75*.6+.6²=2.46 m². Every safe progress score therefore exceeds -4. No differences among infeasible actions are claimed. If F(s) is empty, every candidate has U=-4 and the correct decision is “no safe candidate”; all five IDs form a tied best set solely for score accounting. These contexts remain in every denominator and CSV.

The primary selection is argmax_a U_.2(s,a), with the entire maximizing set recorded at tolerance1e-12. Report singleton counts and tied sets, not arbitrary tie-broken winner diversity. Per-context regret is max_b U(s,b)-U(s,a). The best constant action minimizes mean regret on the complete test pool; this is an **optimistic hindsight constant comparator**, not a fitted deployed policy. Also report the design-selected constant and safe-only progress comparisons separately.

The fixed goal stays external to the world model: do not draw it into training-style images or pretend the WM was trained to accept goal conditioning. Future evaluation would require an independent pixel-derived position readout and unbiased probability accounting; optimized StressDream sample proportions do not estimate this expectation.

## Predeclared metrics, tolerances and assessment

Numeric tolerance=1e-12 m²; practical margins=.0025,.005,.01 m²; strict separability requires absolute difference>margin. Informative states have max U-min U>margin. Meaningfully unique optimal states additionally have top-minus-runner-up>margin. Record all pairs, U, Q*, feasibility, branch witnesses, probability sensitivity and boundary excursions.

Design gate required: >=50% informative at .005; at least three singleton-optimal IDs each occurring >=2/32; best-constant mean regret>.01; >=4 mixed-safe/unsafe contexts; no boundary excursion. This rule rejected the initial oblique goal-progress design despite numerical diversity, because safety was inactive. The sole additional design candidate D2 reused the unchanged mixed pool and passed this same rule. No further design search is allowed.

Held-out success criteria, fixed before generation: >=32/64 informative at .005; >=3 singleton-optimal IDs each with >=4/64 contexts; best-constant mean regret>.01; >=4 mixed-safe/unsafe contexts; no physical boundary excursion. Report all other margins regardless of the outcome. These criteria assess this finite benchmark, not general world-model performance. A final scientific verdict also considers support conflicts and provenance; numerical success alone does not establish model compatibility.

## Execution boundary and reproducibility

Only CPU physical oracles and static source inspection are permitted. No model, VAE, renderer, checkpoint or GPU is used. `raw/GATE0B_EXPERIMENT.py` retains initialization, design, disclosed amendment, seed correction and the exclusive one-time test stage; `raw/TEST_STARTED.json` prevents a second test execution into this directory. The final implementation hash is frozen in V3. Unit tests use design states only, including an independent scalar recurrence, full support sign/rotation symmetries, weighted expectation and hard-constraint score bounds.

Stop after the single held-out evaluation and reporting. Gate 1 is not authorized.
