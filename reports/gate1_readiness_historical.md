> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. This historical stage predates the measured Gate 1A; later measured status is in gate1a_measured_results.md and scientific_feasibility_verdict.md. Hypotheses and experiment designs remain proposals unless a later measurement record explicitly states execution.

# Gate 1 feasibility requirements — NOT EXECUTED

Gate 0 status: **CONDITIONAL**. The oracle and numerical separation check are validated, but constant A0 is practically optimal on all sixteen test contexts. None of the checks below authorizes model execution, checkpoint retrieval, training or a full experiment.

## Minimal readiness checklist

| Requirement | Acceptance evidence required in a later authorized gate | Current status |
|---|---|---|
| Decision scope | Retain the frozen sixteen test contexts. Add constant A0 as a comparator and separate ranking diagnostics from any claim of nontrivial state-dependent action selection. A new decision-diverse pool needs a new preregistration/authorization, with the old results retained. | Design limitation identified; no redesign run. |
| Checkpoint compatibility | Authorized files must have recorded origin, byte size and SHA-256; confirm VAE, denoiser and trained prediction-head keys/shapes and shared training revision. Fail closed on missing heads or incompatible keys; inspect all loose-load missing/unexpected keys. Document unresolved training p rather than assuming .2 or .4. | Not downloaded or inspected. |
| Input/output contract | Verify 128x128 RGB preprocessing [-1,1], float dtype, one-step scalar angular rate, action/time indexing, initial-image deterministic encoding and actual 4x16x16 latent shape. Confirm danger margin m=-C on known valid inputs; boundary convention explicit. | Static assumptions only. |
| Independent image readout | A geometry/template-based reader must use decoded pixels rather than the learned head or privileged latent values. Calibrate position/heading error and failure detection on eight calibration contexts only, with clean renderer and reconstructed inputs separated. Keep test states frozen. | No renderer, VAE or readout executed. |
| Readout accuracy versus margin | Set tolerances before comparing methods. Since C depends on position, if position error<=e and distance<=d, |error(C)|<=2de+e². For a .005 m² pair difference, use a per-action error budget below .0025 (preferably .00125) m²; set the corresponding e using each trajectory's distance bound. Do not rely only on a global pixel RMSE. Report abstention and unparseable fractions; if tolerance is not met, the independent ranking channel is inconclusive. | Criteria only; no tolerance achievement claimed. |
| Reliable trajectory reconstruction | Verify a single complete recovered trajectory matches one legal disturbance branch for the same initial state and actions, over aligned t=0..H; no per-frame switching between incompatible branches. Include orientation only if calibration makes it reliable; otherwise state that ambiguity. Retain reconstructed and true geometry, residuals, event timing and failed parses. | Not executed. |
| Score/noise/sample alignment | An external wrapper must capture score, noise and returned latent from the same iterate, independently rescore selected samples, and preserve an unmodified-release comparison. Distinguish bookkeeping-only fixes from momentum or penalty changes; do not edit the frozen checkout. | Static association issue documented. |
| Runtime measurement | On permitted hardware/dtype/batch size, measure warm complete decision time and peak memory, with cold load separate. Count denoiser forwards, backwards, recomputation, head evaluation, VAE decode, noise regularizers, extra best-sample generation and transfers. CPU oracle timing says nothing about WM cost. | No WM timing/memory measurement. |
| Matched-compute baseline | Start with paper nominal and BoN baselines. Calibrate BoN N on calibration contexts only, enforce identical per-action/decision wall-time caps, serialize actions and paired noise arrays, separate regularizer RNG, log timeouts. Include fixed A0 so the decision metric's simplicity remains visible. | No baseline run. |
| Provenance / stopping | Preserve revision b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d, config/source/checkpoint hashes and all 24 state IDs. No cherry-picking or post-hoc H=16 run after the H=12 trigger was false. Proceed to a larger experiment only under separate explicit scope. | Gate 0 hashes present; future execution prohibited. |

## Minimum additional evidence before interpreting a learned-model result

1. A compatibility record establishing actually loaded trained weights and valid input/output shapes.
2. A held-out independent-readout error/coverage record, with geometry uncertainty demonstrably below the decision margin for the pairs being interpreted.
3. An aligned score/noise/video record that resolves the release bookkeeping issue without silently changing the scientific method.
4. A measured cost calibration including BoN and constant A0; equal sample count alone is insufficient.
5. A decision about scope: the current frozen pool supports rank/error diagnostics, while meaningful state-dependent action selection remains weak because A0 is near-optimal everywhere. No hypothetical future result can retrospectively repair that design.

These requirements are plans, not measured achievements. **No Gate 1 work was executed. Stop and wait for explicit authorization.**
