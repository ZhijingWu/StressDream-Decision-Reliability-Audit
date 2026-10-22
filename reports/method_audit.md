> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# StressDream method audit

Audit date: 2026-10-21 (Asia/Shanghai). Paper: arXiv:2606.00267v2, 6 October 2026. Code revision: `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`.

Evidence labels: **[P] Documented by the paper** (author-reported results, not independently reproduced); **[C] Verified in source code** (static inspection); **[E] Executed and measured** (only explicitly identified audit operations); **[H] Hypothesis only** (includes proposed experiments and analytical interpretations). Unresolved provenance or access is marked **unverified**. No model inference, simulation experiment, training, paid API call, or outreach was performed.

## Scientific finding

StressDream already connects pessimistic imagination to policy improvement. The defensible opportunity is a controlled diagnostic of when failure discovery preserves **relative action quality**, rather than proposing the general idea of decision-relevant world modeling. Its plausibility notion is explicitly relative to the learned world-model distribution; neither typical-looking noise nor a compelling failure video certifies a physically valid counterfactual. This boundary is acknowledged in Appendix F. [P; H interpretation]

The complete main text and Appendices A–F were read in the v2 HTML, including equation text, figure captions and tables. The official project page, its embedded demonstration descriptions, Dubins demonstration page, and typical-set explanation were checked. This audit did not independently score the demonstration videos or reproduce plotted values. The HTML contains the supplementary technical material; no separate supplementary PDF was needed or identified from the supplied official links. [E audit scope]

Primary sources: [paper v2](https://arxiv.org/html/2606.00267v2), [version history](https://arxiv.org/abs/2606.00267), [project](https://stressdream.github.io/), [Dubins demonstration](https://stressdream.github.io/dubins/index.html), [typical-set explanation](https://stressdream.github.io/gaussian_typical_set/index.html), [frozen repository](https://github.com/CMU-IntentLab/StressDream/tree/b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d).

## Claim-to-evidence map

| Required element | Audited finding | Exact paper locator / source |
|---|---|---|
| Formal problem | Robust evaluation is an inner search for high-impact plausible futures for a fixed action, inside an outer choice of actions with low worst-case criterion. The method primarily develops the inner search. | [§3, Eq. 4–5](https://arxiv.org/html/2606.00267v2#S3), [Appendix F](https://arxiv.org/html/2606.00267v2#A6) [P] |
| Inputs / outputs | A frozen action-conditioned diffusion WM takes observation history, future ego-action sequence, and initial noise; predicts future observations. A deterministic sampler makes the future a function of its initial noise for fixed conditioning. | [§2, Eq. 1–3](https://arxiv.org/html/2606.00267v2#S2) [P] |
| Optimization variable | Initial Gaussian noise, independently re-optimized for successive autoregressive segments in the implementation; neither action nor pretrained WM weights is optimized by this steering loop. | §3 Eq. 5, §4 Eq. 8; `dubins/steer.py:207–341`; `ctrl_world/run_steering.py:309–396` [P,C] |
| Semantic objective | Qwen yes/no log-probability difference measures a text-defined event. Driving also uses X-CLIP positive/negative text comparisons. The target can describe failure or another event. | [§4.1 Eq. 6](https://arxiv.org/html/2606.00267v2#S4.SS1), [B.3](https://arxiv.org/html/2606.00267v2#A2.SS3) [P] |
| Plausibility objective | Penalize atypical radius, blockwise isotropy departure and spectral structure. These are finite statistical checks on noise, not a physical dynamics certificate. | [§4.2](https://arxiv.org/html/2606.00267v2#S4.SS2), [B.1–B.2](https://arxiv.org/html/2606.00267v2#A2.SS1) [P; H qualification] |
| Gradient paths | Large-model experiments approximate the sampler Jacobian by a scaled identity: differentiate criterion through video decoder/VLM to generated clean latent, transfer that gradient to noise, and differentiate regularizers directly in noise space. Small Dubins uses full sampler backpropagation. | [§4.3 Eq. 7–8](https://arxiv.org/html/2606.00267v2#S4.SS3), [B.4](https://arxiv.org/html/2606.00267v2#A2.SS4), [C.1](https://arxiv.org/html/2606.00267v2#A3.SS1) [P,C] |
| Failure detection | Dubins: rollout safety threshold and true-dynamics Monte Carlo labels. Driving: held-out event alignment and plausibility judges. Manipulation: human success/failure labels, with Robometer as secondary evidence. | §5 Fig. 1; [D.4](https://arxiv.org/html/2606.00267v2#A4.SS4); [E.1 Fig. 18–21](https://arxiv.org/html/2606.00267v2#A5.SS1) [P] |
| Downstream improvement | Successful demonstrations are weighted by whether steered imaginations fail; fine-tune π0.5-droid using weighted regression / flow matching. This is an actual downstream intervention, rather than only a claim of possible use. | [§6.2 Fig. 6–7](https://arxiv.org/html/2606.00267v2#S6.SS2), [D.5](https://arxiv.org/html/2606.00267v2#A4.SS5), [E.4 Fig. 25](https://arxiv.org/html/2606.00267v2#A5.SS4) [P] |
| Baselines / budgets | Nominal, Best-of-N, no plausibility, and Dubins classifier guidance; equal candidate/iteration counts are the main comparison, with explicit additional backward-pass cost discussed. | §5; §6.1; [B.6 Table 1](https://arxiv.org/html/2606.00267v2#A2.SS6); [E.2 Fig. 22](https://arxiv.org/html/2606.00267v2#A5.SS2) [P] |
| Existing ablations / limitations | Optimistic steering, separate regularizer removals, latent OOD surrogate, base versus collision-finetuned model, held-out quality metrics; local optimization, sequential rollout optimization, base-model support gaps, runtime and reward hacking explicitly discussed. | C.2–C.3, Table 4, Fig. 14–15; E.1–E.3, Fig. 18–24; Appendix F [P] |

## Formal reconstruction and signs

For fixed history h and action sequence a, write the frozen deterministic generator as `o = fθ(ε,h,a)`. The schematic robust decision in Eq. 4 is `argmin_a max_ε Ctest(fθ(ε,h,a))`, with plausibility encouraged by the noise criterion. The implemented inner search optimizes semantic impact plus plausibility regularization. This is a search for supported bad outcomes; optimized sample counts are **not unbiased estimates of real failure probability**. [P; H interpretation]

Using R for positive penalties, the corresponding minimization is `L(ε) = -Csem(fθ(ε,h,a); ℓ) + R(ε)`. For Qwen, Eq. 6 is `Csem = log p(Yes | o,ℓ) − log p(No | o,ℓ)`. The paper's penalty components correspond to:

- Radius: `(‖ε‖₂ − √D)²`.
- Isotropy: `(1/k) ‖Σhat − I_k‖²_F`, averaged over random coordinate permutations and blocks.
- Spectral: variance of spatial-frequency-bin average powers.

Appendix B.2 supplies concentration arguments for these statistics under Gaussian noise. Small values are necessary diagnostics of the intended prior behavior in this formulation; the arguments do not establish that all optimized videos are physically reachable or conditionally faithful to a. [P; H interpretation]

Dubins uses a learned latent safety head in place of a VLM. The paper defines **safety** `C(s)=x²+y²−0.25²`, with failure at `C≤0`. The released dataset and head use **danger margin** `m(s)=0.25²−x²−y² = −C(s)`, with positive meaning unsafe. Pessimistic code maximizes m. These opposite signs are compatible once explicitly converted. [§5 Eq. 9; `dubins/env.py:102`; `dubins/dataset.py:90`; `dubins/steer.py:274–281`; P,C]

## Three instantiations

| Domain | Conditioning and output | Optimization / evaluation details |
|---|---|---|
| Dubins | Rendered RGB 128×128, scalar angular velocity, one-step latent transition; autoregressive rollouts; D=1,024. | Five denoising steps, ten steering updates per generated step; full gradient. Paper dynamics independently flip the commanded turn sign with p=0.2. 4,000 training trajectories, 5,000 evaluation state–action sequences. [§5; C.1 Tables 2–3] |
| Driving | Vista, 25 frames at 576×1024, four 2-D future waypoints, D=921,600. | Fifty denoising steps, twenty steering updates, β=300; X-CLIP and driving-tuned Qwen2.5-VL. Fine-tuning uses PAI-AV, nuScenes and Nexar. Evaluation: 100 pairs over eight event categories plus 200 imminent-collision examples. [§6; D.1 Tables 5–6; D.3] |
| Manipulation | Ctrl-World, five future frames from three cameras at 192×320, D=57,600; paper describes joint-position/gripper actions. | Fifty denoising steps, ten steering updates, β=100; Qwen3-VL-4B. Six tasks: Block Stack, Knife Put, Stacked Utensil Pick, Coffee Bean Pour, Open Coffee Bag, Open Candy Bag. [§6; D.1–D.2] |

Table 7 gives task-specific manipulation fine-tuning data counts (250, 170, 200, 100, 170, 150 respectively), refining the main text's approximate description. D.1 reports 10,000 fine-tuning iterations for Ctrl-World; these are **prior training costs**, separate from test-time steering. [P]

## Ground truth and reported gains

In C.1, each Dubins state/action query is labeled from 10,000 stochastic ground-truth trajectories. One observed failure makes the query positive; no observed failure makes it negative. The main text's “minimum achievable” wording therefore describes a Monte Carlo approximation, not exhaustive reachability. Zero failures in 10,000 independent trials gives an approximate one-sided 95% upper failure-probability bound of 0.0003; it does not prove impossibility. [P; H statistical interpretation]

Figures 1 and 14 compare detection and predicted safety extremes with true-dynamics references. This is already substantive evidence against merely generating arbitrary high-scoring failures. C.3 further uses a learned flow-matching OOD surrogate on generated latents and individual regularizer ablations in Table 4. It would be incorrect to describe either dynamics-based checking or output-space OOD checking as entirely absent. [P]

The authors report failure recall rising from 54% to 94%, and policy success from 39% to 71% in the headline results. These values are **paper-reported**, not results of this audit. In §6.2 and D.5, forty successful demonstrations per task receive weights 1.0 if still successful under pessimistic imagination and 0.1 if imagined to fail. Weights affect both the fine-tuning loss and sampling. π0.5-droid is fine-tuned for 10k steps on one H100; the policy is evaluated over twenty rollouts per task. [§1; §6.2; D.5; Fig. 7,25; P]

E.1 Fig. 17 includes **qualitative comparisons of different candidate action sequences**, so “StressDream never compares actions” is false. E.1 Fig. 21 reports imagined failures among demonstrations that happened to succeed, and correctly cautions that this is not necessarily a false-positive rate under partial observability. A single real success cannot establish zero conditional risk. [P]

## Baselines and compute already addressed

| Comparison | What is already evaluated | Limit of the evidence |
|---|---|---|
| Dubins | Nominal N=1, Best-of-N N=10, ten-step StressDream, StressDream without plausibility, approximate clean-latent classifier guidance. | Classification and aggregate safety extremes, rather than an isolated, within-state finite-action ranking/regret diagnostic. |
| Main driving/manipulation | Random Best-of-N under the stated candidate/iteration budget; plausibility removal; external alignment/quality evaluation. | Equal generation counts do not automatically match backward-pass cost or wall time. |
| Rare events | E.2: five selected long-tail driving examples, forty random samples versus twenty optimization steps. | Small selected subset; alignment metric; no complete end-to-end matched-cost frontier with distinct valid failures. |
| Complexity | B.6 Table 1: BoN `N(K Td + Tv)`; approximate StressDream `N(K Td + 2Tv)`; full-gradient variant `N(2K Td + 2Tv)`. | A coarse analytical cost model, not measured universal GPU/wall-clock equivalence. Decoder, regularization, transfers, best-sample re-generation and batching can matter. |

Appendix B.6 reports roughly 1–2 minutes per Vista generation and about thirty minutes for twenty optimization iterations on an H100. The release README says approximately thirty to forty minutes. These are attributed estimates, not audited timings. [P,C]

## Existing controls and explicit limitations

Existing: regularizer removal (main figures and C.3 Table 4); optimistic versus pessimistic steering (C.2); full gradient for the small model versus approximation discussion (B.4,C.1); different VLMs and viewpoints (B.3 Fig. 10–11); collision-finetuned versus base Vista (Fig. 5,23); plausibility of sticky candies / closed bags (Fig. 2); held-out WMB, Gemini, Robometer and WorldLens diagnostics (D.4,E.1). [P]

Explicit limitations: local rather than global noise search; sequential rather than joint optimization of autoregressive noises; supported events limited by base-model training; physical errors in the base WM cannot be repaired by noise regularization; substantial generation/verification cost; reward hacking; scene-dependent prompt quality. [Appendix F; P]

Remaining questions are bounded, not universal omissions: uncertainty around action-wise bias and ranking, physical validity of full generated trajectories under an identical action sequence, and matched **total** cost rather than candidate count. These questions are motivated by the existing evidence and require experiments. They are not findings that StressDream fails. [H]

## Release differs from paper abstraction

See report 02 for immutable code links. The important static findings are: default deterministic Dubins demo oracle; p=0.4 in dataset-generation defaults and the official Dubins page versus p=0.2 in the paper; Dubins SGD momentum=0.9 versus B.5's no-momentum description; zero explicit permutation-penalty coefficient in Dubins YAML; different concrete spectral/isotropy formulas; five rather than ten Ctrl-World iterations in the released YAML; and end-effector/gripper conditioning in the released Ctrl-World replay loader versus the paper's stated joint-action interface. These establish **provenance and comparability questions**, not measured performance problems. [C]
