> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Gate 0B final verdict

**CONDITIONAL — Decision diversity is improved, but an unresolved model-support or numerical limitation remains.**

Date: 2026-10-21 (Asia/Shanghai).

The new **oracle decision task exists and meets its frozen numerical criteria**. It uses unchanged Dubins physical dynamics, H12 and64 independently generated held-out contexts, all retained. At .005m²,43/64 contexts have informative task-score spread and41/64 have a meaningfully unique best action. Unique optima span five IDs: A0=8,Lhalf=1,Lfull=14,Rhalf=3,Rfull=17;21 contexts have no feasible action and remain tied/infeasible. Three IDs each appear at least four times, as required before testing. [E]

The hindsight best constant remains A0, but its mean regret is now **0.103087417724322m²** and maximum **0.368870120997610m²**. Oracle mean advantage is0.103087417724323m². A0 is safe in every context where any candidate is safe; its feasible-context regret0.153432435682712m² is therefore a genuine expected-progress gap, not a safety-penalty artifact. There are373/640 separated task-score pairs at .005, including317/322 both-safe pairs. Safety coverage is175 safe and145 unsafe action queries, with12 mixed contexts. [E]

This result **changes the objective**: maximize expected progress toward external g=(1,0) subject to full-support safety, with infeasible actions encoded below every feasible score. It is not the original StressDream worst-case safety metric. Under original Q* on the same new test states, constant A0 still has mean regret5.62823647237e-7m². Multiside states, signed actions and H16 did not produce meaningful pure-safety decision diversity on the permitted design pools. [E,A]

The conditional issue is applicability to the **released pretrained WM**, not numerical separation: its training p/data provenance is unverified, while the new objective needs calibrated probability weights and an independent terminal-position readout that the scalar safety head cannot supply. All physical state/action ranges and H12 are compatible with the documented generator and no fatal boundary conflict is known. These facts make the task a credible next candidate, but not a verified pretrained-model benchmark yet. Model support cannot be certified without the separately authorized checks in a later gate. [C,U]

At p=.4, diversity remains: the same singleton winner counts and best-constant mean regret0.034950889156289m². This sensitivity reduces concern that the task is numerically specific to p=.2; it does not verify actual checkpoint calibration or world-model dynamics. [E]

## Integrity and reproducibility

- Gate0: all27 files unchanged from before this gate; original ranking results are preserved.
- Frozen source: all87 present tracked files unchanged; HEAD `b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d`; clean Git status.
- Final test spec SHA-256: `07d19464db19d088049d6ee1c3f565805f50105733523301e62354c5d63f5397`.
- CPU-only tests:11 successful tests before the single held-out run; independent scalar witness replay and raw branch aggregation errors are0m². Output validation used saved branch data, not a second generated test pool.
- Design disclosure: four declared initial options, one additional design-only mixed-pool task option, and one pretest seed-collision correction. Every design result, rejected option and prior spec remains saved. No post-hoc test selection occurred.
- All six requested deliverables, configs, scripts, commands, seeds, raw CSV/NPZ outputs, logs and SHA-256 manifest are in this directory. Root scientific results are in DECISION_DIVERSITY_RESULTS.csv; full pairs and witnesses are under raw/.

No world model, renderer, VAE, checkpoint, training, paid API or outreach was executed. **Stop after Gate0B. Gate1 remains unexecuted and requires explicit authorization.**
