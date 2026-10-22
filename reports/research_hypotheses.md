> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Candidate hypotheses and feasibility gate

Audit date: 2026-10-21 (Asia/Shanghai). Paper: arXiv:2606.00267v2, 6 October 2026. Code revision: `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`.

Evidence labels: **[P] Documented by the paper** (author-reported results, not independently reproduced); **[C] Verified in source code** (static inspection); **[E] Executed and measured** (only explicitly identified audit operations); **[H] Hypothesis only** (includes proposed experiments and analytical interpretations). Unresolved provenance or access is marked **unverified**. No model inference, simulation experiment, training, paid API call, or outreach was performed.

## Shared decision contract

Use a fixed finite action set A(s) at each identical initial state s, a frozen WM and a declared horizon. The primary target is **support-worst-case safety**, matching StressDream's inner/outer robust setup. It is not an estimate of event probability. Let `C(s)=x²+y²−r²` and `Q*(s,a)=min_δ min_t C(s_t)` over every admissible turn-flip sequence δ. Select the action with largest Q*. True action quality is computed from physical dynamics independently of the learned scoring head. [H proposed definitions; paper §3,5 motivates contract]

### A. Failure discovery versus decision reliability — PRIMARY

| Gate | Assessment |
|---|---|
| 1. Precise question | At matched total inference cost, does increased StressDream failure discovery improve the ordering and selection of fixed candidate actions according to true finite-horizon worst-case safety? When can action-dependent search/readout errors decouple them? |
| 2. Closest work | StressDream §3,§5,§6.2,E.1 Fig. 17; Nakamura et al. 2024 regret; WorldGym §4.2; MiraBench §3–6; Yu et al. 2026 decision-centric evaluation. Sources and versions are in report 03. |
| 3. Already addressed | The robust action objective, possible-failure detection, qualitative alternatives, and policy success improvement after robust demonstration weighting. |
| 4. Unanswered remainder | A paired finite-action diagnostic linking changes in discovery recall to independently measured rank error and decision regret under fixed actions and total budget. No such complete measurement was identified in the inspected sources. |
| 5. Falsifiable hypothesis | Stronger steering can improve supported-failure recall while failing to improve, or worsening, action ordering/selection because errors differ across actions. The testable instance is a paired recall gain plus no practical regret gain at the predeclared budget/setting; it is not a claim that degradation must occur everywhere. |
| 6. Minimum setup | Released Dubins pretrained WM/head, an external fixed-action wrapper, independent stochastic-dynamics oracle and score/video bookkeeping. No policy training or VLM needed. |
| 7. Oracle | Exhaustive finite-horizon sign branching at H=12; compute exact Q* and binary support-failure labels within numerical tolerance. Monte Carlo is unnecessary for this support target. |
| 8. Essential controls | Identical s/a; paired initial diffusion noises; independent regularizer RNG; uniform per-action budget; BoN with matched measured time; learned score versus image-derived geometry; untouched-release versus explicitly reconciled implementation; safe/unsafe/action-tie coverage. |
| 9. Expected cost | Small CPU reachability calculations plus small pretrained-model inference/backprop; no training. Proposed primary test has 16 states × 5 actions × 3 diffusion starts and H=12. About 144k denoiser forward calls for ten updates before returned-sample regeneration, plus backward/regularizer cost and matched BoN. Wall time/VRAM are unmeasured. |
| 10. Negative results | Recall and ranking may improve together; almost all actions may tie; release/provenance errors may explain discordance; effects may disappear under image-derived scores or exact oracle. Each restricts or rejects the hypothesized mechanism and is still informative. |
| 11. PI relevance | Directly connects the lab's world-model steering to decision regret, safety observability and reliable action verification. It offers careful evaluation rather than claiming a new planner. |
| 12. Merits investigation? | **Yes, as a bounded diagnostic project.** Broader research value depends on a repeatable mechanism and later validation in one action-conditioned manipulation simulator. Do not promise a publishable contribution from this pilot alone. |

Mechanisms to distinguish [H]: (i) an accurate binary event detector saturates at “possible failure” for many actions but cannot order their severities; (ii) steering finds different-quality local optima for different actions; (iii) latent head errors change with steering strength; (iv) generated trajectories leave action-conditional physical support; (v) all rankings are actually correct and recall improvements are useful. The last outcome is a serious alternative, not a failure of the study.

### B. Plausibility versus failure severity — BACKUP

| Gate | Assessment |
|---|---|
| 1. Precise question | Conditional on fixed s and a, do regularized steered videos satisfy a complete physically realizable trajectory, and can any discrepancy explain action-ranking errors better than noise typicality or visual quality alone? |
| 2. Closest work | StressDream C.1–C.3, E.1–E.3, F; DNO §3; MiraBench action following/optimism; WMB and WorldLens. |
| 3. Already addressed | True-dynamics failure labels and aggregate safety extrema; individual regularizer ablations and latent OOD; independent quality evaluators; explicit base-model distribution limitation. |
| 4. Unanswered remainder | Conditional **whole-path** consistency: a sequence of individually plausible frames can still fail to correspond to any single admissible disturbance path for the supplied actions. The existing aggregate detection and OOD evidence does not fully establish this property. |
| 5. Falsifiable hypothesis | Over a steering-pressure sweep, some outputs remain noise-typical and visually legible but deviate from every oracle branch beyond reconstruction-calibrated tolerance. If valid, test whether deviations associate with incorrect action ordering; no prior assumption that they will. |
| 6. Minimum setup | The same Dubins model, exact branch set and independent renderer-based state recovery. Use the primary data collection rather than starting a video-scale experiment. |
| 7. Oracle | Minimum complete-path distance to any legal branch, plus bounded-step dynamics residuals and geometry-based collisions. Calibrate extraction error on clean rendered and VAE-reconstructed trajectories. |
| 8. Essential controls | Nominal/BoN, no regularizer, radius-only, released full penalty, explicit isotropy restoration; p provenance; blinded image review; unparseable outputs retained in denominators. Keep threshold selection separate from test scenes. |
| 9. Expected cost | CPU branch matching and decoding generated latents; model costs shared with A. No learned density surrogate needs to be trained. Extra ablations only after an authorized pilot identifies a reason. |
| 10. Negative results | All steered videos may remain within tolerance; state extraction may be too inaccurate; violations may be equally common in nominal predictions; apparent issues may be readout artifacts rather than dynamics errors. |
| 11. PI relevance | Studies whether learned safety/prediction representations preserve what action evaluation needs, complementing the lab's partially observable safety work. |
| 12. Merits investigation? | **Yes, backup and mechanism check.** It becomes worthwhile if independent path checking is reliable and adds information beyond controls StressDream already reports. Broad “noise regularization is not physics” wording alone is insufficient. |

Do not reject a very rare but physically supported trajectory as an artifact. Do not call an unsupported learned-WM output a real-world rare event merely because it appears plausible. Noise-shell statistics, output OOD, semantics, physical support and event probability are distinct tests. [H]

### C. Equal-budget failure discovery — REQUIRED CONTROL / DEFER STANDALONE

| Gate | Assessment |
|---|---|
| 1. Precise question | Does StressDream produce more distinct physically valid failures than BoN under the same end-to-end latency and memory cap, and how does this depend on full versus approximate gradients and restarts? |
| 2. Closest work | StressDream B.6 Table 1,E.2 Fig. 22,F; DNO and diffusion inference-time alignment; ELASTIC §3–5 for the lab's compute agenda. |
| 3. Already addressed | Equal candidate/iteration comparison, complexity accounting for verifier/WM backward passes, runtime estimates, and forty random samples versus twenty steering steps on five long-tail examples. |
| 4. Unanswered remainder | End-to-end measured efficiency curves including decoding, scoring, backward passes, regularization, best-sample regeneration, batching, memory and independently validated failure diversity. |
| 5. Falsifiable hypothesis | An advantage persists for valid-failure discovery at at least one preregistered cost level; alternatively matching all overhead removes it. Both outcomes are scientifically possible. |
| 6. Minimum setup | Dubins wall-time/call-count instrumentation and independent geometric validation. To claim a VLM-cost conclusion, a later video-model test with frozen local verifier and approved checkpoints is necessary. |
| 7. Oracle | Exact support-failure labels; independent geometry for each generated trajectory; predeclared distinctness bins by contact time and path geometry. |
| 8. Essential controls | First reproduce paper baselines: nominal, BoN, no plausibility, classifier guidance. Report same-generation-count and same-time arms separately. Fix hardware/precision/batch size; include warmup and transfers, disclose exclusions. |
| 9. Expected cost | Can share A/B outputs. Full-scale Vista (~10 GB model and 48–80 GB steering memory per README) is too large as a first undergraduate diagnostic; Ctrl-World also adds substantial weights/verifier cost. |
| 10. Negative results | Steering may lose at small budgets but win later; duplicates or invalid failures may erase its alignment-score advantage; vectorized BoN may change the frontier; all comparisons may be hardware-specific. |
| 11. PI relevance | Aligned with efficient deployment-time generation and ELASTIC, but overlaps existing compute research and may be mainly an engineering audit without a deeper pattern. |
| 12. Merits investigation? | **Mandatory measurement control; weaker standalone lead.** Reconsider only if a stable, meaningful regime change or allocation insight emerges. |

## Choice and stopping rules

Primary A; backup B. Include C as a fairness control within A. Do not start three independent projects. The sequence is: resolve release provenance → validate oracle/readout → run a tiny authorized paired diagnostic → decide whether there is an effect/mechanism worth extending. [H]

Stop or reformulate if the candidate actions have no meaningful oracle separation, reconstruction error swamps safety differences, the frozen checkpoint does not represent the claimed environment, or the only finding is a public-demo bookkeeping error. Report such outcomes honestly; none justifies a general reliability claim about StressDream. A persistent positive finding would still require an updated novelty search and a second environment before proposing a new algorithm. [H]
