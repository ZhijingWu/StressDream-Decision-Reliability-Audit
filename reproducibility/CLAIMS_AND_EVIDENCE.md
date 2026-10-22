# Claim-to-evidence ledger

| Category | Claim | Public evidence |
|---|---|---|
| [P] | StressDream already includes Dubins checks, plausibility ablations, action comparisons and policy improvement | Original arXiv v2, cited in README; `reports/method_audit.md` |
| [C] | Paper p=.2 vs generator p=.4; deterministic demo; momentum/regularizer/sample-association differences | `reports/provenance_matrix.md`, with immutable upstream line links |
| [E] | 16 oracle tests; 12/16 informative; 106/160 pairs at .005 m² | `experiments/gate0/raw/ORACLE_UNIT_TESTS.log`, `CONTEXT_SUMMARY.csv`, `PAIRWISE_ACTION_DIFFERENCES.csv`, `oracle/` |
| [E] | A0 max robust regret ~.000176 m² | `experiments/gate0/ACTION_SEPARATION_RESULTS.csv`; calibration/test split retained |
| [E] | Gate 0B 64 contexts, 43 informative, 41 meaningful unique, five IDs; 21 infeasible | `experiments/gate0b/raw/HELDOUT_SUMMARY.json`, `HELDOUT_CONTEXTS.json`, `DECISION_DIVERSITY_RESULTS.csv` |
| [E] | Gate 0B mean best-constant task regret .103087 m² at p=.2 | Same summary/action CSV; `reports/oracle_design_spec.md` specifies goal, constraint and -4 m² sentinel |
| [E] | Checkpoints structurally compatible, saved heads present | `experiments/gate1a/raw/COMPATIBILITY_PASS.json`, `CHECKPOINT_TENSOR_INVENTORY.json`, `WEIGHT_CORRESPONDENCE.json`; origin hashes in `checkpoint_origins.json` |
| [E] | 43 nominal futures, 32 VAE pairs, 215 denoiser forwards | `experiments/gate1a/raw/COUNTERS.json` |
| [E] | Readout p95 .00738841/.00989602 m² | `experiments/gate1a/READOUT_RESULTS.csv`, `raw/READOUT_SUMMARY.json`; exact figure values in `note/evidence/FIGURE_MEASUREMENTS.json` |
| [E] | Worker ~38.0 s, sampled aggregate peak .318 GiB | `experiments/gate1a/raw/RUNTIME_SUMMARY.json` and `reports/runtime_and_memory.md` |
| [U] | Model/readout trajectory error confounding; incomplete final telemetry; training p unknown | `reports/input_output_measurements.md`, `scientific_feasibility_verdict.md`, `checkpoint_verification.md` |
| [H] | Better independent reader, then matched-total-cost nominal/BoN/steering comparison | `reports/research_hypotheses.md`, technical note §8; unexecuted |

No claimed result measures steering ranking improvement/degradation, a new algorithm, full paper reproduction or author/lab endorsement. No source mismatch is presented as proof about the paper's results. Gate 0B is a changed objective. Public reports are selected sanitized archival copies, and the manifest records both their original and public SHA-256 values.
