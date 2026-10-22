> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Related work and novelty check

Audit date: 2026-10-21 (Asia/Shanghai). Paper: arXiv:2606.00267v2, 6 October 2026. Code revision: `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`.

Evidence labels: **[P] Documented by the paper** (author-reported results, not independently reproduced); **[C] Verified in source code** (static inspection); **[E] Executed and measured** (only explicitly identified audit operations); **[H] Hypothesis only** (includes proposed experiments and analytical interpretations). Unresolved provenance or access is marked **unverified**. No model inference, simulation experiment, training, paid API call, or outreach was performed.

## Novelty verdict

The broad claim “visual/failure-generation quality need not imply decision quality” is established research territory. Decision-focused regret, policy-ranking evaluation, optimism-bias diagnostics, uncertainty calibration and compute allocation all predate or overlap the proposed project. **No algorithmic novelty is established by this audit.** [P external literature; H novelty assessment]

The narrower candidate is a paired study of **StressDream steering intensity, true-dynamics worst-case action ordering, and decision regret at fixed candidate actions and measured total compute**. The reviewed work does not fully settle this specific relationship. This is a bounded search conclusion, not a claim that no unpublished or unlocated work does so. [H]

## Literature matrix

The following sources were consulted at primary paper/publisher pages. Load-bearing sources were read beyond abstracts in the named sections; contextual entries are explicitly limited.

| Work / verified version | Evidence actually consulted | What it establishes for this investigation | Remaining distinction |
|---|---|---|---|
| **StressDream**, Seo et al., arXiv:2606.00267v2, 2026; official pages identify CoRL 2026. [Paper](https://arxiv.org/html/2606.00267v2) | Full method and Appendices A–F; especially §3,5,6.2; C.1–C.3; E.1 Fig. 17,21; E.4; F. | Robust action objective, true-dynamics failure checks, quality/OOD controls, action examples and measured policy improvement already exist. | A separate within-state finite-action rank/regret curve versus steering pressure and total budget was not identified. |
| **Not All Errors Are Made Equal: A Regret Metric for Detecting System-level Trajectory Prediction Failures**, Nakamura, Tian, Bajcsy; arXiv:2403.04745v4, 2024; CoRL 2024 stated on arXiv. [Paper](https://arxiv.org/html/2403.04745v4) | §3–4, §6–8; generalized regret and limitations. | Prediction failures should be judged by downstream decision impact; counterfactual regret and calibration are already central Intent Lab ideas. | Human-trajectory predictors and deployed interactions, rather than diffusion-noise steering in action-conditioned video futures. |
| **WorldGym: World Model as An Environment for Policy Evaluation**, Quevedo et al.; arXiv:2506.00613v3, 30 Sep 2025. [Paper](https://arxiv.org/html/2506.00613v3) | §2,3.2,4.1–4.2,6. | Explicitly tests simulated/real policy performance agreement and relative policy rankings. | Policy-level Monte Carlo evaluation; does not establish that adversarially steered futures preserve within-state worst-case action ranking. |
| **MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models**, Yang et al.; arXiv:2605.29360v1, 28 May 2026. [Paper](https://arxiv.org/html/2605.29360v1) | §3–6, Fig. 4; perturbation and evaluator definitions. | Physical plausibility, action following and optimism bias are separable; visual quality is not an action-fidelity certificate. | Tests nominal/perturbed action reliability across WMs; the reviewed protocol does not isolate StressDream's gradient steering, exact stochastic reachability and robust decision regret together. |
| **How Should World Models Be Evaluated for Embodied Decision-Making? A Decision-Making-Centric Position**, Yu et al.; arXiv:2606.15032v2, 28 Jun 2026. [Paper](https://arxiv.org/html/2606.15032v2) | §2.2,2.6,5–6; declared decision contracts and ranking/uncertainty metrics. | Counterfactual fidelity, ranking, exploitability and optimization utility are already proposed evaluation targets. It is a position/synthesis paper, not empirical proof about StressDream. | The possible contribution must be a specific diagnosis with evidence, not naming those metrics. |
| **Safe-Sim: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries**, Chang et al.; arXiv:2401.00391v3, 6 Aug 2024. [Paper](https://arxiv.org/html/2401.00391v3), [ECCV primary listing](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/3157_ECCV_2024_paper.php) | §3,5,6.3–6.5. | Guided diffusion already generates plausible, reactive adversarial traffic to challenge planners, with safety and realism metrics. | Structured agent trajectories and closed-loop traffic adversaries, rather than initial video-noise optimization. Do not call adversarial failure discovery new. |
| **Inference-Time Alignment of Diffusion Models with Direct Noise Optimization**, Tang et al.; ICML 2025, PMLR 267:58905–58930. [Publisher](https://proceedings.mlr.press/v267/tang25h.html), [preprint v3](https://arxiv.org/html/2405.18881v3) | §2–3 and publisher abstract; noise optimization, OOD reward hacking, probability regularization. | Noise optimization and statistical prior regularization already address reward hacking. | No general guarantee of action-conditioned physical validity for video WMs or correct robust action ordering. |
| **WorldModelBench: Judging Video Generation Models As World Models**, Li et al.; arXiv:2502.20694v1, 28 Feb 2025. [Paper](https://arxiv.org/html/2502.20694v1) | §3.1–3.3,4–5. | Instruction following and physics-focused judgment supplement perceptual metrics. StressDream already uses this held-out evaluator. | Judge consistency and physical-looking content are different from a simulator-verified counterfactual under an exact action. |
| **WorldLens: Full-Spectrum Evaluations of Driving World Models in Real World**, Liang et al.; arXiv:2512.10958v2, 1 Jun 2026. [Paper](https://arxiv.org/html/2512.10958v2) | §3.1–3.4 and metric definitions; checked against StressDream E.1. | Evaluation includes action following and downstream aspects, beyond generic video quality. StressDream uses a subset of analytic generation-quality metrics. | Those subset metrics do not supply exact conditional reachability. The broader WorldLens agenda must be acknowledged before claiming a new evaluation framework. |
| **How Well Do Latent World Models Understand Partially Observable Safety Constraints?**, Kim, Nakamura, Bajcsy; arXiv:2510.06492v3, 12 Oct 2026. [Paper](https://arxiv.org/html/2510.06492v3) | §3–5, especially estimation/prediction gaps and calibration. | Safety-relevant observability and future predictability can fail separately; calibration/privileged sensing are prior mitigation directions. | Our first diagnostic fixes fully observed synthetic state to isolate steering/ranking, rather than claiming to solve partial observability. |
| **When to Act, Ask, or Learn: Uncertainty-Aware Policy Steering**, Yuan, Wu, Bajcsy; arXiv:2602.22474v2, 12 May 2026; RSS 2026 stated on arXiv. [Paper](https://arxiv.org/html/2602.22474v2) | III–IV, conformal prediction and verifier/base-policy composition. | VLM action selection requires calibrated uncertainty; candidate-action verification is already studied. | It calibrates a verifier and low-level policy composition, rather than steered video-noise search against exact dynamics. |
| **ELASTIC: Efficiently Learning to Adaptively Scale Test-Time Compute for Generative Control Policies**, Li et al.; arXiv:2606.31132v1, 30 Jun 2026. [Paper](https://arxiv.org/html/2606.31132v1) | §3–5, compute cost and matched-budget experiments. | State-dependent sequential/parallel compute allocation is a current lab research topic. | The proposed C audit concerns valid world-model failure discovery and full verification/backward costs, rather than learning an action-denoising compute policy. |
| **One Risk to Rule Them All: A Risk-Sensitive Perspective on Model-Based Offline Reinforcement Learning**, Rigter, Lacerda, Hawes; arXiv:2212.00124v3 / NeurIPS 2023. [Paper](https://arxiv.org/html/2212.00124v3), [proceedings](https://papers.nips.cc/paper_files/paper/2023/hash/f49287371916715b9209fa41a275851e-Abstract-Conference.html) | §3–4; risk-measure and uncertainty formulation. | Risk-averse model-based control must distinguish model uncertainty from environmental stochasticity. | Support-worst-case discovery is not the same quantity as CVaR or expected failure risk. Retained as a foundational pre-2024 reference. |
| **Risk-Sensitive Reward-Free Reinforcement Learning with CVaR**, Ni, Liu, Lai; ICML 2024, PMLR 235. [Publisher](https://proceedings.mlr.press/v235/ni24c.html) | Publisher abstract and metadata only; contextual. | CVaR is a probability-weighted tail criterion, with a substantial existing literature. | No claim about StressDream results is inferred from this paper. |

## Coverage of the seven requested themes

| Theme | Closest audited evidence | Consequence for the research framing |
|---|---|---|
| Adversarial / rare events | Safe-Sim; StressDream §5,E.2; DNO | Frame the contribution around the diagnostic target and oracle, not the existence of adversarial generation. |
| WM reliability | MiraBench; WorldGym; latent partially observable safety paper | Separate action fidelity, outcome validity, and value/ranking quality. |
| Risk-sensitive model-based planning | 1R2R; Ni et al.; StressDream Eq. 4 | Declare a risk functional before interpreting pessimistic samples. |
| Decision-focused prediction | Regret paper; WorldGym; decision-centric position | Ranking and regret are established tools; the study must reveal a specific mechanism or boundary. |
| Generative plausibility | DNO; StressDream B.1–B.2,C.3; WMB; WorldLens | Noise statistics and quality judges are complementary to physical support checks. |
| Action-conditioned failure detection | MiraBench; StressDream Fig. 1,17,21 | Failure recall alone is incomplete; include specificity, action alternatives and discrimination. |
| Uncertainty / counterfactual evaluation | UPS; latent safety constraints; Regret; WorldGym | A successful logged trajectory is not the no-failure counterfactual distribution. |

## Novelty gate for each candidate

**A — retain as primary, narrowly.** StressDream has the robust objective, qualitative action comparisons, and real downstream fine-tuning gains. What was not found is a controlled, within-state, fixed-candidate rank/regret-versus-steering study with an independent exact finite-horizon oracle and matched total cost. A positive result would diagnose where search helps decisions; a negative result would identify where it already works and provide a reusable evaluation protocol. A generic “failure recall is not enough” paper would be insufficient. [H]

**B — retain as backup, narrowly.** StressDream already checks true stochastic dynamics, individual regularizers, output-latent OOD and quality. Investigate **whole-trajectory action-conditional reachability**, while retaining a distinction between marginal image plausibility and a dynamically consistent path. The broad assertion “typicality does not guarantee physics” is already acknowledged in Appendix F and related work. [H]

**C — require as a control; defer as a standalone project.** StressDream already compares BoN, discusses backward overhead, and includes a forty-versus-twenty sample test. A systematic valid-failure-per-second/memory frontier could still matter, but merely reporting gradients are more expensive is not a novel scientific result. Algorithmic compute allocation is additionally close to ELASTIC and general diffusion test-time scaling. [H]

## Search record, provenance and uncertainty

Discovery channel: connected internet search/open tool, official arXiv pages, primary conference/publisher pages, official project/repository pages, and direct HTTPS retrieval for retained reading notes. No paid API was used. Searches included:

- `adversarial world model safety testing diffusion rare event generation 2024 2025 2026 robotics`
- `world model action ranking decision reliability evaluation benchmark 2025 2026`
- `risk sensitive model based planning diffusion world models CVaR 2024 2025`
- `"StressDream" "action" ranking`
- `"MiraBench" "Action"`, `"world model" "policy ranking" 2026 benchmark`
- `SafeSim adversarial diffusion 2024 safety critical scenarios arxiv`
- `"Inference-Time Alignment of Diffusion Models with Direct Noise Optimization"`
- `"WorldModelBench" arxiv 2025`

Access date for all sources: 2026-10-21. Primary paper version strings were checked in the downloaded HTML or arXiv record. Source HTML was retained only for audit notes; local SHA-256 provenance is appended below. No separate bibliographic graph, formal retraction/correction database, citation-forward completeness check or private lab material was available. Search failure or absent public code does not establish nonexistence. Current primary records, rather than search snippets, support the findings above.

The position paper is a synthesis, MiraBench is a 2026 preprint, and benchmark results use different task/model populations. None establishes a universal claim about all video world models. Unreviewed discoveries were not treated as scientific evidence. Public prior work substantially narrows the novelty claim but cannot certify exclusivity. A focused update should precede any later manuscript submission. [H]

## Retained-source integrity record

These are SHA-256 hashes of the retained HTML bytes, not claims about model weights or experimental data. Initial TLS failures for MiraBench/UPS were resolved by a later successful retrieval; the record below describes the successful retained copies. Snapshots are reading notes under `work/`, separate from deliverables. Paper quotations/figures are not redistributed in this bundle.

| Source | Bytes | SHA-256 |
|---|---:|---|
| [mirabench](https://arxiv.org/html/2605.29360) | 950,221 | `0f3eb3973ac4b4d920618ec6798b21632fa0279dacb5c7d88a39cbc7f430d100` |
| [worldgym](https://arxiv.org/html/2506.00613v3) | 292,032 | `b75c77a7162f0c926718f861aaf9604377ef95b3c711cda505b21d71ca5fda41` |
| [regret](https://arxiv.org/html/2403.04745v4) | 239,029 | `dcdb4d1a514751864de9f199357cc35ea22991f2fe695726e6cce74622d97e45` |
| [decision_position](https://arxiv.org/html/2606.15032v2) | 560,797 | `6ea099594eef28eac10379fed603329ee19f533cadf9c75f382288b5ec4e815d` |
| [safesim](https://arxiv.org/html/2401.00391v3) | 311,580 | `b3a78ec2794a2e6653945456162e5d9a03f7abbbc99f47b833e29b926347a252` |
| [dno](https://arxiv.org/html/2405.18881) | 410,145 | `98011867a500c7cdb4b147d1f90c16c4bd63094ec1a49d00132330ba98383bff` |
| [wmb](https://arxiv.org/html/2502.20694) | 281,966 | `17b834d6f950359741400033143986f483b43d686e86cf4cf868b53911a487a8` |
| [worldlens](https://arxiv.org/html/2512.10958) | 1,317,043 | `83395338e2bf8f3cf5e44a93c7665a22904132285232a6c8aaea879a6ec59972` |
| [ups](https://arxiv.org/html/2602.22474v2) | 482,568 | `98af4a1d3b8f9f2894583c39f51009eb964c48a8bd24538bd6d52f125c977ef7` |
| [partial_safety](https://arxiv.org/html/2510.06492v3) | 328,954 | `23bf9706a6fb92ef7e29595c03423103f8f63e1924d16075fa90a42431922770` |
| [risk1r2r](https://arxiv.org/html/2212.00124) | 594,888 | `067ed14cabe252ae9997c07f799363033c73835a8a15b0b2cc4e8d73f213d1fa` |
| [elastic](https://arxiv.org/html/2606.31132) | 231,870 | `0a60f60fe333f88ab0e0fe4bded870e8faae4d04b2f1ac1be39bd1a466dfa031` |
| [pi](https://www.cs.cmu.edu/~abajcsy/) | 32,760 | `17899b4d9b54ec8cdd583c99fac3595e2c77d2976026c0ffb09cf1db81131edd` |
| [lab](https://cmu-intentlab.github.io/) | 17,609 | `ef4ea9cf551951bd704380556ccc7df7de69c379921a9016100e2cecf818e070` |
| [student](https://zhijingwu.github.io/) | 33,277 | `574ff4882c888eb3b6407d6f7a51a1a9722947acff23b52c1aa96c84aebac3d1` |
| [StressDream-v2](https://arxiv.org/html/2606.00267v2) | 875,582 | `ee1333dfa73fbbba99f669d898ad335fb72cf6c6ee916965d57a0f3254938b74` |
| [StressDream-project](https://stressdream.github.io/) | 109,891 | `6120e1b6983fc8e3fc754cfadde65b55cd5133dbc25adfd6eeea99a019ad4ab0` |
