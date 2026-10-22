> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Gate 0 versus Gate 0B

Evidence labels: **[E]** measured CPU-oracle result; **[C]** static source verification; **[A]** analytical deduction for the declared discrete model; **[U]** unresolved applicability. No world-model performance was measured.

## Distinct scientific contracts

Gate 0 is the frozen **safety ranking** benchmark, maximizing support-worst-case C in m². Gate 0B is a separately frozen **task decision** benchmark, maximizing expected squared-distance progress subject to the same support safety constraint. Utility U uses -4 for infeasible candidates solely to encode the hard constraint. The units are both m² but the meanings and scales differ; comparing their regret ratio would be misleading. Neither benchmark measures StressDream performance.

| Property | Gate 0 | Gate 0B D2 |
|---|---|---|
| Test contexts | 16 fixed grid states; all retained | 64 generated once with seed202610299; all retained |
| State family | x=-rho, heading offsets0,.4,.6,1 | 16 per quadrant, rho~U[.35,.75], inward-heading error~U[-1.4,1.4] |
| Candidates | Five positive/zero magnitude/timed profiles | Zero and +/- .625,+/-1.25 constant rates |
| Horizon | 12 | 12 |
| Safety rule | Maximize minimum C | Hard C>0 on all branches; then maximize expected target progress |
| Informative states at .005 | 12/16 | 43/64 |
| Best constant | A0, mean safety regret1.284895e-5 | A0, mean task regret0.103087418 |
| State-dependent decisions | A0 practically optimal in16/16 | 43 feasible states have a unique optimum, across five IDs |
| Numerical near-ties | Many; twelve numerical pair ties | Twenty-one all-infeasible contexts tie all five task scores |
| Safe/unsafe action queries | 31 safe,49 unsafe /80 | 175 safe,145 unsafe /320 |
| Mixed-safe/unsafe contexts | 4/16 | 12/64 |
| Fixed-action decision advantage | Negligible at chosen safety margins | 0.103087418m² mean task utility gain over hindsight best constant |

## All eight requested results for Gate 0B

1. **Meaningfully informative states:** 43/64 at all three margins. Distinguish this spread count from top-versus-runner-up separation: 43,41,40 unique meaningful decisions at .0025,.005,.01 respectively.
2. **Distinctly optimal actions:** all five IDs are unique optima somewhere. Three IDs (A0,Lfull,Rfull) each have at least four contexts, satisfying the frozen criterion. Half-rate optima are sparse, so claims about their prevalence are weak.
3. **Optimal action distribution:** the table below counts unique optima only. The remaining21 contexts have no feasible action and are not arbitrary tie-broken wins.
4. **Best constant-action regret:** A0 is the hindsight best constant, mean0.103087417724322m² and maximum0.368870120997610m² at p=.2. The same A0 was selected as best constant on design data; no test-fitted advantage is hidden by choosing an inferior constant.
5. **Oracle advantage:** 0.103087417724323m² mean U gain over the best constant. On the43 feasible contexts, A0 is always safe and conditional mean progress regret is0.153432435682712m². Thus this advantage is actual expected progress among feasible choices, **not an artifact of the -4 penalty**. A perfect constrained oracle declares infeasibility on21 contexts; this is not a collision-free policy for them.
6. **Pairwise separability:** at .005,373/640 task-score pairs separate;317/322 both-safe pairs separate. The latter shows meaningful discrimination without using an unsafe-versus-safe score discontinuity.
7. **Safety coverage:**31 contexts have all five candidates safe,12 mix safe/unsafe,21 have no safe candidate. Every initially unsafe count is zero; infeasibility develops along a future branch. Retaining these cases limits decision coverage to43/64 rather than suggesting universal solvability.
8. **Margin and p sensitivity:** provided below for all frozen contexts. No state filtering or revised threshold follows the test.

| Action ID | Unique optimal contexts p=.2 | Unique optimal contexts p=.4 | Unique winner with gap>.005 (p=.2) | Constant mean regret p=.2 (m²) |
|---|---:|---:|---:|---:|
| A0 | 8 | 8 | 8 | 0.103087418 |
| Lhalf | 1 | 1 | 1 | 0.691968196 |
| Lfull | 14 | 14 | 13 | 0.971996573 |
| Rhalf | 3 | 3 | 3 | 0.663569344 |
| Rfull | 17 | 17 | 16 | 0.931319513 |

| Margin (m²) | Informative /64 | Meaningfully unique optimum /64 | Separated pairs /640 | Separated pairs among both-safe /322 |
|---:|---:|---:|---:|---:|
| 0.0025 | 43 | 43 | 375 | 319 |
| 0.005 | 43 | 41 | 373 | 317 |
| 0.01 | 43 | 40 | 367 | 311 |

At p=.4, the number of informative states remains43/64, the singleton winner counts are unchanged, and best-constant regret remains positive at0.034950889156289m² (max0.124904751275464). Meaningful unique counts become40,40,37 across the three margins; separated pairs become371,364,345. This supports oracle diversity at both documented flip rates; it does not establish the released WM's distribution or calibration.

The shared scorer also retained expected-safety/CVaR fields in the raw held-out summary. Those are descriptive exploratory outputs, not additional selected test objectives or evidence used to choose the distribution. Final selection and success assessment use only the predeclared D2 contract and sensitivity fields.

## What did not improve under the original safety objective

On these same saved new test trajectories, if the decision metric is reverted to original Q*, A0 again has near-zero regret: mean5.62823647237e-07, max3.60207134232e-05m². Therefore the improvement is attributed to the explicitly changed task objective and probability weighting, not to a claim that rotating states and adding signed actions solved the original pure-safety degeneracy. [E]

## Scientific interpretation

The new oracle task passes every predeclared numerical held-out criterion, and has nontrivial state-dependent choices with active safety constraints. It improves the ability to test task decision selection, while the original benchmark remains useful for pessimistic safety ranking. A future learned-model study would need to distinguish safety support discovery from the probability-calibrated progress channel, and cannot interpret optimized-noise sample frequencies as expectations. Applicability to the released checkpoint remains conditional for the reasons in MODEL_SUPPORT_RISKS.md.

No confidence interval is attached to exhaustive finite-pool branch values. The64 contexts are one seeded draw from the declared generator; their exact frequencies are not universal population claims. Test generation was not repeated to improve the counts.
