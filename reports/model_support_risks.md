> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Model-support risks for Gate 0B

Evidence labels: **[E]** measured CPU-oracle result; **[C]** static source verification; **[A]** analytical deduction for the declared discrete model; **[U]** unresolved applicability. No world-model performance was measured.

## Verified compatibility with the public physical generator

| Input / use | Source evidence | Gate 0B status |
|---|---|---|
| Initial position | [env.py:74–85](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/env.py#L74): sample x,y within approximately[-1.4,1.4], reject obstacle interior. | rho in[.35,.75], multiple sides; all outside obstacle. New ring/heading distribution is a subset with changed density, not guaranteed checkpoint coverage. |
| Heading | [env.py:85–86](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/env.py#L85): inward atan2 plus N(0,1), modulo2pi. | Error lies[-1.4,1.4], within1.4 standard deviations of that documented initial-heading distribution. Rotations preserve inward-relative geometry. No clearly new orientation channel is required. |
| Command | [generate_dataset.py:47–53](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/generate_dataset.py#L47): independent commands uniform[-1.25,1.25], sign reversal. | All signed rates are in the declared bounds. Exactly constant12-step profiles and endpoint rates have different joint density from random actions; bounds alone do not certify training support. |
| Horizon | [config.yaml:6](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/config.yaml#L6), [diffusion_world_model.py:199–217](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/models/diffusion_world_model.py#L199): length16 data sequences, one-step action conditioning; autoregressive generation. | H12 uses the same one-step interface as Gate0. It does not demand a new long-horizon architecture, but rollout composition can visit poorly represented states. |
| World bounds | [generate_dataset.py:59–65](https://github.com/CMU-IntentLab/StressDream/blob/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d/dubins/generate_dataset.py#L59): termination outside approximately1.4m. | Analytically rho+vHdt<=1.35; measured maximum absolute coordinate across all test branches0.8743689892m. No boundary conflict in the new test. |
| Task goal | Public Dubins model has image/action conditioning and a radius-margin head, no goal input. | g=(1,0) stays external. No goal marker or changed renderer is used. Terminal position must be derived independently from predicted pixels; the released margin head alone cannot evaluate target progress. |

These are source-based support plausibility arguments, not measurements of pretrained model capability. No checkpoint was opened or downloaded. [C,U]

## Unresolved issues that prevent an unconditional model-readiness claim

**1. Dynamics probability and expectation calibration.** Paper §5 uses p=.2; generator signature/CLI use p=.4; the released weights' actual training rate and data hash are unverified. Both finite supports are identical, so this did not affect Q*. Gate0B's expected goal progress depends on those probabilities. Diversity survives the .2/.4 sensitivity in this pool, but transferring a physical expectation to WM samples requires distributional fidelity that was not inspected. This is a specific unresolved model-support/calibration issue, not an automatic consequence of forbidding inference. [C,U]

**2. Training-sequence coverage.** Constant controls at rate limits are legal but their persistence differs from iid training commands. The WM conditions on one action/history step, which reduces but does not eliminate compounding distribution shift. Uniform initial-position sampling and inward noisy headings support the broad state family; unknown actual checkpoint data may not. No claim of guaranteed in-distribution rollouts is made. [C,U]

**3. New readout requirement.** Original signed danger head m=r²-x²-y² discards angular position. Two positions with identical radius can have different distances to the fixed goal. The head cannot identify target progress. A later independent image-based state/position reconstruction with task-level error calibration is essential; none ran here. It must not draw the goal into WM images or use true oracle states to score learned predictions. [A,U]

**4. Sampling distribution versus adversarial search.** StressDream's steered futures are a search distribution. Their average is not an unbiased estimate of expected physical progress. A future experiment would need a separately calibrated nominal/importance-accounted progress channel and a steered safety channel. Defining a task requiring those channels is valid, but the released steering demo does not already implement this constrained decision system. [A,U]

**5. Candidate infeasibility.**21/64 contexts have no support-safe action among the five choices; all are retained as infeasible tied sets. They do not count toward optimal-ID diversity. This is a property of the declared candidate set and robust constraint, not model failure. Abstention/coverage must accompany later comparisons; no hidden turn-off of the safety condition is allowed. [E]

**6. Existing provenance discrepancies.** Momentum .9 versus paper no momentum, explicit random-permutation coefficient0, concrete regularizer formula differences, pre-update score/post-update sample association, loose checkpoint loading and conditional trained-head loading remain as documented in Gate0. None was repaired in the frozen source or executed here. See its unchanged PROVENANCE_MATRIX.md. [C]

## What can be concluded now

No **known fatal input-range, obstacle-geometry or horizon conflict** was found for D2. Numerical diversity does not require placing states inside obstacles, changing physics, moving the obstacle or leaving training bounds. The decision task nevertheless differs from the original safety score, and its probability-calibrated use of the released model remains unresolved. The appropriate scientific status is conditional applicability, not a StressDream performance conclusion or permission to execute Gate1.

Primary immutable references: [paper §5 Eq.9](https://arxiv.org/html/2606.00267v2#S5), [C.1 implementation](https://arxiv.org/html/2606.00267v2#A3.SS1), [Appendix F distribution limitation](https://arxiv.org/html/2606.00267v2#A6). This gate uses the previously retained paper and pinned source; no new network access or paid API was needed.
