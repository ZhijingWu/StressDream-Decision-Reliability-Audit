> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. Measured Gate 1A record; no later steering/ranking experiment is implied.

# Gate 1A measured independent readout

The deterministic pixel reader used dark-component segmentation, weighted principal-axis/skew orientation and a geometric position/heading correction. Only 16 tuning clean/reconstructed pairs selected threshold 160 and four translation/axis correction constants plus an angle offset. This is renderer/readout calibration, not learned-model training. The reader takes only RGB pixels and frozen constants; it does not receive a head, latent, true state or oracle branch. The code and constants were hashed before any validation image was read or future nominal prediction generated. Context seeds 2026102201/2026102202 and all 32 contexts remain in raw/FROZEN_PILOT_CONTEXTS.json.

Validation ran once on the 16 independent pairs. All cases are retained. No threshold, state, fit or exclusion was changed after validation. This table summarizes saved records, without rerunning the reader on validation:

| Domain | Parseable | Position MAE / p95 / max (m) | Heading MAE / p95 / max (rad) | abs C error MAE / p95 / max (m²) |
|---|---:|---|---|---|
| Clean validation | 16/16 | 0.00806933 / 0.013917 / 0.0142502 | 0.0750525 / 0.136126 / 0.179155 | 0.00378325 / 0.00738841 / 0.0119187 |
| VAE validation | 16/16 | 0.00820425 / 0.0139683 / 0.0155625 | 0.0769019 / 0.138445 / 0.175725 | 0.00412928 / 0.00989602 / 0.0116139 |

Position RMSE: clean 0.0086381m; VAE 0.00889789m. x/y bias, medians, heading circular bias, all per-frame values and tuning summaries are in READOUT_RESULTS.csv and raw/READOUT_SUMMARY.json. Validation safety-sign disagreements: clean 0/16, VAE 0/16. Coverage and heading p95 meet the coarse screen; **position p95 fails the prespecified .01m screen in both domains**. Coverage does not establish precision.

Sensitivity to the per-action score target margin/4:

| Margin (m²) | Per-action target (m²) | Clean within target /16 | VAE within target /16 |
|---:|---:|---:|---:|
| 0.0025 | 0.000625 | 0 | 0 |
| 0.005 | 0.00125 | 1 | 2 |
| 0.01 | 0.0025 | 6 | 7 |

These are empirical single-frame diagnostic counts, not numbers of identifiable action pairs. The .005m² primary margin needs per-action uncertainty around .00125m²; validation p95 absolute C errors exceed both that budget and the full .005m² margin. No certified interval bound for arbitrary WM outputs is available. The bound |C_hat-C|<=2||p_hat||e+e² explains the sensitivity to millimetre-scale position error; a low average pixel error or parse success cannot qualify a robust ranking. Neither frozen benchmark's margins were changed.

External goal g=(1,0) stayed outside the WM image. Goal squared-distance p95 absolute error: clean 0.0244826m²; VAE 0.0309998m². Endpoint progress combines initial and final errors and adds probability/sampling uncertainty. Each domain has 8 validation equal-radius pairs at different azimuths: ordering correct 8/8 clean and 8/8 VAE. This demonstrates access to angular position and external-goal geometry, which a radial head lacks, but does not validate expected progress at decision margins. See EXTERNAL_GOAL_ALIAS_CHECK.csv.

The independently scored validation margin head has MAE 0.0581228m², p95 0.131605m² and 3/16 sign errors. These are calibration diagnostics, not a safety-performance comparison or a substitute position reader. The same encoded latent's head score appears alongside its clean and reconstructed images; these are not two independent head tests.

All 43 nominal future frames were parseable under the unchanged reader. Heading validation p95~.14 rad is similar to or larger than the .125rad separation between the two ±.0625 one-step heading increments for |a|=1.25. Tiny-step sign/probability identification is therefore weak. Sixteen validation states cannot certify universal error tails; empirical maxima and p95 are descriptive, not guaranteed bounds. Input-renderer library versions are recorded, while training-time versions are undocumented; a version mismatch cannot be confirmed or excluded. Reader bias, decoded appearance and learned dynamics remain confounded in support residuals.

Figures/ALL_VALIDATION_PAIRS.png shows every validation pair, in index order; figures/BOTH_H12_ROLLOUTS.png shows every frame of both horizon checks. Actual source pixels are retained separately; figure labels were added only to contact sheets, never WM inputs.
