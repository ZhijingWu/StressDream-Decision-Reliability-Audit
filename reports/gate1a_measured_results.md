> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. Measured Gate 1A record; no later steering/ranking experiment is implied.

# StressDream Gate 1A measured pilot

The released Dubins VAE/WM and saved prediction heads are structurally compatible with the frozen source and available CPU environment. The small pilot generated its entire approved workload, but its independent image readout did not meet the prespecified measurement accuracy needed for scientific ranking/progress evaluation. Training flip probability and nominal expectation calibration remain unresolved.

- Gate 0 safety ranking: **CONDITIONAL**, technically loadable but measurement readiness unmet.
- Gate 0B constrained expected progress: **NO-GO at present**, readout precision and probability calibration unresolved.
- Checkpoint architecture/loading: **PASS**, verified with restricted CPU loading and required trained-head namespace.

| Domain | Parseable | Position MAE / p95 / max (m) | Heading MAE / p95 / max (rad) | abs C error MAE / p95 / max (m²) |
|---|---:|---|---|---|
| Clean validation | 16/16 | 0.00806933 / 0.013917 / 0.0142502 | 0.0750525 / 0.136126 / 0.179155 | 0.00378325 / 0.00738841 / 0.0119187 |
| VAE validation | 16/16 | 0.00820425 / 0.0139683 / 0.0155625 | 0.0769019 / 0.138445 / 0.175725 | 0.00412928 / 0.00989602 / 0.0116139 |

Both validation domains parsed 16/16 images; all 43 generated future frames parsed. These coverage counts do not remedy the measured safety/progress error. The full bounded work was 43 future latents,32 VAE reconstruction pairs and 215 denoiser evaluations, using two H12 trajectories and nine two-step samples from C01/Dm000/Dm001 calibration/design contexts only, plus one warm-up. No frozen held-out test context was evaluated or selected.

Final prediction completed at 12.05min from the first transfer; nominal inference worker wall time 37.9848s, sampled aggregate peak RSS 0.318GiB. See RUNTIME_AND_MEMORY.md for timer scope and limitations. Complete H12 wall times were 3.83758s and 3.74434s on this CPU, excluding initial-frame encoding and including artifact/readout overhead. No larger-experiment cost or matched-compute performance is inferred.

One transfer ended early and was safely resumed from the same approved URL, before any loading. A separate final-export bug occurred after all model calls because sample standard deviation is undefined for scalar diagnostic tensors. Raw evidence was recovered without rerunning inference; lost telemetry is listed explicitly in INPUT_OUTPUT_MEASUREMENTS.md and raw/OUTPUT_ARTIFACT_VALIDATION.json. This report does not hide the failed process exit or claim a completely successful export.

The separate detailed reports are CHECKPOINT_VERIFICATION.md, INPUT_OUTPUT_MEASUREMENTS.md, READOUT_VALIDATION_RESULTS.md, RUNTIME_AND_MEMORY.md and SCIENTIFIC_FEASIBILITY_VERDICT.md. CSVs retain individual readout errors, sensitivity counts, external-goal checks, timings and whole-trajectory physical support matches. Raw checkpoint metadata, exact contexts/noise/actions, original logs and executed scripts remain alongside them. All source, seven audit reports, Gate 0, Gate 0B and Gate 1A preparation files are checked against the pre-run hashes. SHA256SUMS.json covers this measured bundle except itself; checkpoint hashes are recorded separately without duplicating payloads into deliverables.

No claim about StressDream action-ranking performance is supported or made. **STOP after Gate 1A.**
