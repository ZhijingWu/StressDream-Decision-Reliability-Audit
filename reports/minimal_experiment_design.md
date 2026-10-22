> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Minimal diagnostic experiment — DESIGN ONLY

Audit date: 2026-10-21 (Asia/Shanghai). Paper: arXiv:2606.00267v2, 6 October 2026. Code revision: `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`.

Evidence labels: **[P] Documented by the paper** (author-reported results, not independently reproduced); **[C] Verified in source code** (static inspection); **[E] Executed and measured** (only explicitly identified audit operations); **[H] Hypothesis only** (includes proposed experiments and analytical interpretations). Unresolved provenance or access is marked **unverified**. No model inference, simulation experiment, training, paid API call, or outreach was performed.

## Question and scope

For fixed candidate actions at the same state, does StressDream's improvement in possible-failure discovery also improve **true worst-case action ordering and action selection**, at matched total compute? [H]

This protocol isolates the inference-time evaluation mechanism. It does not reproduce the six-task π0.5 fine-tuning experiment or claim online closed-loop policy improvement. No experiment described here has been executed. Checkpoint retrieval, dependency installation and any simulator/model launch require the user's later explicit authorization.

## Why the released Dubins module is the first choice

It contains an image encoder/decoder, action-conditioned latent transition, differentiable margin head, noise-steering entry point, known low-dimensional dynamics, renderer, controllable initial state and custom action arrays. It therefore supplies the necessary **interfaces** at much lower cost than Vista/Ctrl-World. [C; report 02]

It does not ship a faithful stochastic evaluation oracle or finite-action experiment harness. Build those in a new experiment directory, leaving the audited checkout unchanged. The paper's stochastic Eq. 9 must be implemented explicitly. The default `env.py` demo trajectory is insufficient as its replacement. [P,C; H proposed wrapper]

The pilot remains conditional on meaningful action separation and a reliable image readout. If those gates fail, no model performance conclusion is allowed.

## Fixed system and independent oracle

Use v=1 m/s, dt=.05 s, obstacle radius r=.25 m, angular rate within ±1.25 rad/s, and the exact discrete update order of paper Eq. 9 / generator:

`x[t+1]=x[t]+v dt cos θ[t]`

`y[t+1]=y[t]+v dt sin θ[t]`

`θ[t+1]=θ[t]+dt δ[t] a[t]`, independently `P(δ[t]=−1)=p`.

Primary p=.2 follows the paper; repeat oracle probability summaries at p=.4 to disclose release provenance uncertainty. The **support** oracle is identical for every 0<p<1 because all finite sign sequences have positive probability. This does not make failure probabilities or learned WM sampling distributions identical.

Set horizon H=12 (0.6 s). Enumerate all 2^12=4,096 sign sequences per state/action query, or equivalently branch a small binary tree. With float64 arithmetic, compute:

- `C(s)=x²+y²−r²` (larger is safer).
- `Q*(s,a)=min_δ min_(t=0..H) C(s[t])`.
- `Y*(s,a)=1[Q*(s,a)≤0]`: possible failure, rather than probability above a threshold.
- `a*(s)=argmax_a Q*(s,a)`.

Use `R(s)=max_a Q*(s,a)−Q*(s,ahat)` as exact robust decision regret in m². It is an outcome from independent dynamics, not the learned objective re-evaluated on its own outputs. Preserve the complete branch giving each minimum as an interpretable witness. Check oracle update order, action-zero equivalence and angle wrapping before use. [H]

Optionally sum branch probabilities to compute `Pf(s,a)` and tail severity as **secondary** summaries. Do not interpret a disagreement between worst-case selection and expected-risk selection as evidence against the method: they optimize different risk functionals. Steered sample fractions must never be used as Pf.

## States, action alternatives and separation gate

Proposed transparent initial-state pool: `(x,y)=(-ρ,0)` with ρ in `{.35,.45,.60,.75}` m, heading β in `{0,.2,.4,.6,.8,1.0}` radians relative to the +x direction, giving 24 contexts. The β=.2 and .8 cases form eight calibration contexts; the other sixteen are the locked test contexts. These numbers are a proposed pilot, not a power calculation or a representative natural deployment distribution.

Primary fixed action set, each of length H:

| Action ID | Angular-rate sequence, rad/s |
|---|---|
| A0 | all zero |
| A1 | all +0.625 |
| A2 | all +1.25 |
| A3 | +1.25 for first six steps, then zero |
| A4 | zero for first six steps, then +1.25 |

Fix and serialize the entire candidate set before running either method. Do not use only ± versions of the same absolute sequence: under unrestricted independent sign flips, those have the **same worst-case support**, creating artificial ranking ties. Time-varying absolute controls avoid that particular redundancy. [H analytical control]

An oracle-only gate, performed after later authorization and before any model comparison, reports the Q* spread and number of distinguishable pairs for **all** sixteen test contexts. Keep all contexts in aggregate results; separately report informative contexts with best-to-worst Q* spread greater than .005 m². This practical threshold corresponds to approximately 1 cm radial clearance near the obstacle boundary and is a design choice. Report sensitivity at .0025 and .01 m².

If fewer than eight contexts are informative, mark this action pool/horizon inconclusive; do not search test contexts based on observed StressDream behavior. The next prespecified step is the same simulator at H=16, with A3/A4 switching at eight steps and a frozen new test pool chosen only from oracle geometry. This costs 65,536 branches per query, still a CPU oracle, but is a separate preregistered follow-up. If that also lacks informative decisions or a faithful WM/readout, Dubins does not support the desired diagnostic at the accessible setting.

## Model methods and implementation arms

At each context/action, use three initial diffusion seeds `{11,29,47}`. Identical start-noise arrays are shared between nominal/BoN and StressDream where meaningful. Use separate deterministic streams for noise initialization, regularizer permutations and baseline additional draws; precompute arrays rather than relying on matching global seed alone. Ground-truth support enumeration has no random seed.

Methods, in priority order:

1. Nominal N=1.
2. Best-of-N with N=10, matching the paper's Dubins sample count as a reference arm.
3. StressDream released full-gradient settings, ten updates per step; retain every iteration for diagnostics, including checkpoints at 2 and 5 updates.
4. Best-of-N with N calibrated to match measured end-to-end cost of method 3 under the same per-action cap.
5. Required paper controls on a small prespecified calibration subset first: no plausibility and classifier guidance as described in C.1. The latter needs a new implementation because the public harness was not found. Do not label an unvalidated replacement “reproduced CG.”

Run the unmodified release arm first when permitted. A second clearly named reconciled arm would use momentum zero as in B.5 and exact score/noise/sample association, while logging all other departures. Do not silently switch the Dubins permutation coefficient from its released zero default or claim the reconciled arm exactly reproduces unpublished evaluation code. Keep release, bookkeeping-only correction, and further parameter reconciliation distinct in saved configs. If the initial issue is entirely a bookkeeping effect, report that limitation rather than attributing it to steering theory. [H]

For any comparison, evaluate **the actual returned latent/video**. The release scores before an update and may save a regenerated post-update sample; the future harness must retain aligned `(noise, latent, score)` tuples. This requirement also prevents saved last-noise tensors from being mistaken for the noise of a previously selected best video.

Do not add CEM, learned verifiers, diffusion-model retraining, multi-start hybrids or new planners in the first experiment. If later needed, compare the existing paper methods first; a hybrid of restarts and gradients is already suggested in Appendix F and is not automatically a new algorithm.

## Compute matching and accounting

Budget is equal **per candidate action**, so total decision cost includes all five actions. Calibrate BoN's N on the eight calibration contexts using warm steady-state latency; choose one N for the test set, independent of oracle difficulty and outcomes. Also enforce a per-action deadline: retain only completed generation+score pairs; if a method cannot produce a result in budget, record an explicit timeout/abstention. Do not quietly score a partial rollout as safe.

Publish two views: equal sample/iteration count for comparability with the paper, and equal measured end-to-end compute for the scientific question. Record:

| Cost | Required measurement |
|---|---|
| WM generation | Every denoiser forward, number of denoising steps, autoregressive length, batch size and dtype. |
| Backward | WM backward for full mode; head/decoder/VLM backward; gradient-checkpoint recomputation. A backward is not assumed to equal a forward. |
| Other work | VAE encode/decode, score evaluation, noise regularizers, normalization, initial candidate actions, best-sample regeneration and device transfers. |
| Latency | Synchronize accelerators around timers; cold-start load/download cost separate from warm inference. Exclude only display/video encoding from the primary decision timer; report it separately. |
| Memory | Peak allocated and reserved accelerator memory where applicable, plus CPU resident memory; fixed device-memory cap. |
| Diversity | Valid unique failure trajectories per query and per second, with contact-time bins of two timesteps and geometry separation above twice calibrated extraction error. Report sensitivity to bin width. |

Dubins uses a small learned head, so VLM calls are **zero**. It cannot empirically settle whether large VLM cost changes Vista/Ctrl-World conclusions. Report that scope rather than extrapolating. No hosted evaluator is needed.

## Independent readout and validity

Primary action selector uses the learned head exactly as the method does: `Qhat=−max_t mhat[t]` and selects max Qhat. An independent image-based channel recovers car position and heading from rendered/decoded RGB with fixed template/color geometry; it must not access the optimized latent head output. Calibrate pixel-to-world and extraction error on clean rendered states and VAE reconstructions using only calibration contexts. A simple reader may fail on artifacts; retain “unparseable” as a validity failure, not as a removed sample.

Compare the complete recovered path against all legal oracle branches for that **same** s,a, using one consistent branch for the whole sequence. Define normalized path distance as the minimum branch RMS position error divided by a frozen calibration tolerance, with a separate wrapped-angle criterion when orientation is reliable. Per-frame proximity to some branch is insufficient because it can switch incompatible disturbance histories. Report dynamics residuals and event timing as complementary diagnostics.

The backup hypothesis B is supported only by discrepancies larger than reconstruction/extraction uncertainty. No trained OOD surrogate is needed, and passing this tolerance is not a proof of physical correctness outside this simulator.

## Separate scientific metrics

| Question | Metric |
|---|---|
| Did it discover real possible failures? | Query-level TPR/recall against exact Y*, TNR and precision; also **valid-witness recall**, requiring both a failure prediction and a parseable physically consistent generated failure path. |
| Does it order actions correctly? | Pairwise accuracy among oracle pairs separated by >.005 m², tie-aware Kendall τ-b, tie fraction and Qhat-vs-Q* scatter. Predicted ties count as half correct for strict pairs; oracle near-ties are reported separately. |
| Does selection matter? | Mean/median/worst robust regret R; rate of selecting an unsafe action when a robust-safe alternative exists; coverage/timeout rate. |
| Is the signal faithful? | Head-vs-image event disagreement, action-conditional path residual, unparseable fraction, noise-statistic diagnostics. |
| Is it economical? | Valid-witness recall, valid unique failures and decision regret versus measured latency/calls/memory. |

Aggregate one context-level result after averaging its three diffusion starts; bootstrap whole contexts to retain within-context action/seed pairing. Show per-context outcomes and paired uncertainty intervals. Sixteen fixed synthetic contexts give a **diagnostic**, not a universal prevalence estimate or a well-powered general superiority test. Borderline `Q*≈0` and score differences below numerical tolerance are explicitly tagged rather than flipped by floating-point noise.

## Hypothesis decision and controls

Define `Δrecall = recall(SD)−recall(BoN-time)` and `ΔR = mean R(SD)−mean R(BoN-time)`. Before seeing test outputs, adopt .005 m² as a practical regret margin, and zero as the directional recall margin.

- Evidence **consistent with decoupling**: paired recall gain has a positive 95% context-bootstrap interval, while regret is practically equivalent (entire interval inside ±.005 m²) or worse (interval above +.005 m²). At least one independently checked action-order error must be present; report readout/support/cost controls to explain it.
- Evidence **against this tested instance**: recall improves and regret improves by more than .005 m² with its paired interval below −.005, accompanied by better ordering. This rejects the proposed decoupling pattern on this setting; it does not prove a general implication.
- **Inconclusive**: uncertainty overlaps relevant bounds, no recall gain, too many tied actions, poor readout, or unresolved checkpoint/provenance differences. “No significant improvement” alone is not evidence of equivalence.

Sensitivity/ablation priorities: steering checkpoints 2/5/10; horizon 8/12 on matched prefixes; penalty strength 0/.5/1/2 on calibration cases; learned head versus independent geometry; aligned bookkeeping; release momentum versus zero; radius-only versus explicitly activated permutation/spectral terms; independent versus shared regularizer RNG. Freeze calibration choices before test comparisons and label post-hoc exploration. Not every arm belongs in the first pilot; expand only to resolve an observed concern, under the later authorization.

## Resource envelope and next environment

For the locked 16×5×3 test: H=12 gives 240 state/action/seed queries. Ten updates and five denoising steps yield approximately 144,000 denoiser forward calls, up to another similar number for release best-sample regeneration, plus backward, encoding/decoding and regularizers. BoN-time adds its own measured matched cost. Oracle enumeration covers 80 distinct state/action pairs, roughly 327,680 complete sign sequences, without rendering every branch. Shared prefixes can reduce CPU work.

Needed after authorization: about 77 MB of tracked Dubins weights, a small isolated Python environment and ordinary CPU resources; a modest local GPU could accelerate the small WM, but VRAM/latency must be measured before choosing it. There is no training. No reliable hour estimate is available from source inspection; reserve one working session for setup/oracle validation and treat total inference duration as a pilot measurement, with a user-approved cap. Large VLM/video checkpoints are unnecessary.

If Dubins remains non-discriminative or image readout fails after the prespecified horizon check, the next scientifically valid **manipulation** setup is a fresh isolated Push-T simulator with resettable true states, fixed action chunks, an explicitly bounded initial-state nuisance distribution, and a compatible frozen action-conditioned WM checkpoint. This is a proposed follow-up with unresolved checkpoint availability; do not borrow or modify the researcher's existing Push-T work. Simulator outcomes, rather than latent distance, would be the oracle. Ctrl-World's supplied coffee-bag replay alone is not an equivalent replacement: it lacks resettable counterfactual hardware outcomes for all fixed action alternatives. [H]

Protocol references: [StressDream §3,5,C.1](https://arxiv.org/html/2606.00267v2#A3.SS1), [B.6 cost](https://arxiv.org/html/2606.00267v2#A2.SS6), [E.1 action examples](https://arxiv.org/html/2606.00267v2#A5.SS1), [Appendix F](https://arxiv.org/html/2606.00267v2#A6); immutable code anchors are in report 02.

**STOP: proposal only. No checkpoint retrieval or experimental execution is authorized by this document.**
