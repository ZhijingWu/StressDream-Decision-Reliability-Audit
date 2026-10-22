> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. Measured Gate 1A record; no later steering/ranking experiment is implied.

# Gate 1A measured input/output contract

CPU neural work completed once: 43 future latents,32 paired VAE reconstructions,36 encodes,75 decodes,78 composite head calls and 215 denoiser UNet forwards. There were 35 clean-renderer calls. No backward pass, optimizer, training, GPU execution, steering or full benchmark sweep occurred.

Actual tensors satisfied shape, dtype, device and finite-value assertions: input [1,3,128,128] RGB float32 in[-1,1]; mode latent [1,4,16,16]; history [1,1,4,16,16]; raw signed action [1,1,1] rad/s; noise and next latent [1,4,16,16]; decoded float tensor [1,3,128,128]; margin/done [1,1]. Raw saved latent/noise/action arrays were independently rechecked after execution (allow_pickle=False). All 110 stored PNGs are 128x128 RGB. Future latent arrays are finite float32. Uint8 output is the release clamp-and-cast convention; no crop, resize or goal glyph was introduced.

The repeated C01 posterior-mode encoding had maximum absolute difference 0, passing atol 1e-6/rtol 1e-5. Actual CPU sigmas: 79.99998474121094,17.527830123901367,2.5152194499969482,.16975267231464386,.0019999996293336153,0. The external wrapper passed immutable saved per-step noise arrays directly to sampler.sample, avoiding the source rollout's ignored initial_noise parameter. Commands conditioned image_t to image_(t+1) without dt scaling or sign inversion; positions in the physical reference use old heading. Positive/negative commanded turns were each exercised at all three pilot contexts. This exercises the interface; it does not establish perfect learned action fidelity.

The reader parsed 43/43 future frames. A single consistent physical sign branch was matched to each complete path; scalar replay agreed with the vector reference within 1e-12. No frame-by-frame oracle branch switching was permitted.

| Pilot trajectory | Max position residual (m) | Max heading residual (rad) | Coarse full-path tube pass |
|---|---:|---:|---|
| H12_C01_A0 | 0.0698885 | 0.309427 | False |
| H12_Dm000_positive | 0.0163036 | 0.147237 | False |

The coarse tube uses max positional residual<=.01m and max circular heading residual<=.15rad. Matching chooses the most favorable complete legal branch and therefore is a consistency diagnostic, not paired predictive error, branch-frequency calibration or an action-ranking result. Reader uncertainty confounds these residuals. See all 12 jobs in TRAJECTORY_SUPPORT_RESULTS.csv and full matched paths in MATCHED_SUPPORT_PATHS.csv.

Final export encountered a scalar-statistics bug after all approved model calls: torch.std's default sample correction yields NaN for single-element head/action tensors. Finite assertions on the actual tensors had already passed; the NaN was diagnostic metadata. The exception and original worker logs remain untouched. No inference/head/encode/decode was replayed. Saved images, latents, noises, actions, per-operation timings, calibration head values and pixel readouts were recovered. The complete tensor-stat event log, decoded pre-clamp float arrays/ranges, future head numeric outputs and inference OS peak-working-set value were lost. Those quantities are explicitly unavailable, never reconstructed or replaced with invented values.

raw/OUTPUT_ARTIFACT_VALIDATION.json records independently checked artifacts and these omissions. This telemetry failure limits completeness but does not change the frozen calibration or consume extra neural samples.
