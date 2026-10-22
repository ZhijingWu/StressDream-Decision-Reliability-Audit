> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Why A0 dominates the frozen safety-ranking benchmark

Date: 2026-10-21 (Asia/Shanghai). Original Gate 0 is preserved byte-for-byte, including its implementation, raw data and hashes. This analysis proposes a new task separately; it does not revise Gate 0.

Evidence labels: **[E]** measured CPU-oracle result; **[C]** static source verification; **[A]** analytical deduction for the declared discrete model; **[U]** unresolved applicability. No world-model performance was measured.

## Analytical diagnosis

For a fixed action sequence a and full independent sign support, the effective input at time t can be either +|a_t| or -|a_t|. Replacing a by any coordinatewise sign-flipped sequence is just a bijection of disturbance strings. Consequently the complete reachable trajectory set and Q*=min_delta min_t C are identical. **Left/right commands of equal magnitude cannot be different safety choices under this support-worst-case criterion.** This holds for every state and every finite horizon while all sign strings have positive probability; increasing H cannot remove this symmetry. [A]

Rotating the initial position and heading together around the centered circle rotates every trajectory, preserving x²+y² and hence Q*. The centered obstacle has no preferred side. Gate 0's x=-rho and nonnegative heading offsets therefore sample only one representative half of a rotational/reflection-symmetric geometry. Merely placing states on other sides reproduces the same relative-heading problem. [A]

Straight action A0 has no turn uncertainty. Nonzero magnitudes give the adversary turn directions that can bend the path inward; the worst case may be a very rare sign sequence, regardless of whether p=.2 or .4. A fixed positive commanded turn is not a guaranteed turn away from the obstacle. This explains A0's practical dominance in the explored close-range, short-horizon family; **it is not a theorem that A0 wins for every possible state/action design**. A counterexample to exact universal dominance already appears in Gate 0: head-on states have tiny nonzero-turn improvements caused by sampled-position geometry. [A,E]

H=12 covers only .6m of travel. If closest approach occurs before step6, A4's late turn cannot change the already attained minimum and can tie A0; A3 and A2 may tie when their worst contact precedes their action-profile difference. Because the metric includes t=0 and every sampled time, neither a later recovery nor goal attainment repairs an earlier low minimum. The final disturbance changes theta_H but not any scored position by H, yielding duplicate spatial futures. [A]

The five Gate 0 actions offer zero, two constant positive magnitudes, and two timed pulses. They supply scalar safety separation but little choice between qualitatively distinct guaranteed maneuvers. The centered obstacle, one relative-heading range, short travel horizon and support adversary combine to make straight a strong constant policy. Signed actions alone address none of the support symmetry. [A,E]

**Initial states already inside the obstacle are not the explanation here.** Every Gate 0 initial radius is >=.35m, above r=.25; every Gate 0B generated initial state is also outside by construction. If an initial state were inside, Q*<=C(s0)<=0 for all actions, so no hard-safe action could exist under an inclusive path-minimum constraint. It would create an unavoidable-infeasibility context, not evidence of a successful avoidance decision. No such initial context was selected or removed. [E,A]

## Separate design-pool evidence

All options below were declared before their design computations, with one disclosed design-only amendment. Each uses the same dynamics and float64 exhaustive branching. There was no learned-model access or favorable model-based search. Mixed design seed202610210; oblique seed202610211; 32 states per pool. A/B/C use the unchanged mixed states; D uses oblique; D2 returns to the already defined mixed pool without selecting or adding states.

| Design option | Informative /.005 | Singleton-optimal counts | Best constant mean regret (m²) | Mixed safe/unsafe contexts | Decision |
|---|---:|---|---:|---:|---|
| A_multiside | 30/32 | A0:19, A1:0, A2:0, A3:0, A4:1 | 1.71592102e-07 | 4 | A0 remains practically optimal |
| B_signed | 30/32 | A0:32, Lfull:0, Lhalf:0, Rfull:0, Rhalf:0 | 0 | 4 | A0 remains practically optimal |
| C_longer | 30/32 | A0:32, Lfull:0, Lhalf:0, Rfull:0, Rhalf:0 | 0 | 6 | A0 remains practically optimal |
| D_progress_safe | 32/32 | A0:1, Lfull:11, Lhalf:2, Rfull:17, Rhalf:1 | 0.1353968 | 0 | Rejected: safety inactive |
| D2_progress_safe_mixed | 22/32 | A0:4, Lfull:5, Lhalf:2, Rfull:11, Rhalf:0 | 0.107258456 | 4 | Selected on design only |

The H=16 option enumerates 65,536 strings per query. It still has zero best-constant safety regret on this design pool. This is a Gate 0B design alternative, **not execution of the Gate 0 fallback**. Gate 0's fallback remains untriggered and untouched. [E]

## Alternative risk functionals

On the signed H=12 **design pool**, replacing support worst-case C with expected path-minimum C gives a best-constant mean regret of 0.024999837 m² at p=.2. Lower-tail CVaR_.2 of path-minimum C gives 0.00475391323 m². These probability-weighted objectives can distinguish signed commands because p differs from .5. They are **different risk functionals**, not improvements to the original Q* definition. Their dependence on the unresolved checkpoint training probability is a central applicability risk. They were descriptive design diagnostics, not selected test objectives. [E]

The selected D2 retains hard support safety but maximizes expected external target progress among safe candidates. It changes both the decision reward and the aggregation of target performance; it cannot be called the original StressDream safety metric. It is motivated by the control requirement to make progress while avoiding failure, rather than by a particular learned method's errors. [A]

## Design history and independence

Initial A/B/C failed the decision-diversity gate. Initial D had diverse goals but no mixed-safe/unsafe cases, so the unchanged rule rejected it. One amendment, frozen in `DESIGN_AMENDMENT_1.json` before evaluation, tested the same D objective on the unchanged mixed pool; it passed. All rejected results remain under raw/. This is disclosed calibration/design iteration, not post-hoc held-out selection.

Before generating test states, an audit noticed that the initially proposed test seed coincided with the oblique design seed. `PRETEST_SEED_CORRECTION.json` switched only the test seed to unused202610299 and froze `FROZEN_TEST_SPEC_V3.json`. V1 and V2 records were retained. The final test was generated/evaluated once, with every outcome retained. No test-driven revision followed.
