> Public archival copy. Local absolute paths are redacted; this is not represented as byte-identical to the frozen original. Source/public SHA-256 mappings are in `reproducibility/evidence_manifest.json`. Measured Gate 1A record; no later steering/ranking experiment is implied.

# Gate 1A measured checkpoint verification

The two explicitly approved payloads were retrieved from the exact raw.githubusercontent.com URLs pinned to b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d. Content sizes and Git blob SHA-1 match the prior official tree; SHA-256 was computed locally. Actual checkpoint origins/URLs/response headers and timings remain in raw/CHECKPOINT_DOWNLOADS.json.

| Checkpoint | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| vae_final.pt | 49,507,403 | `c63fa2482a4ecdb85a0d65e47570a21c3bcbc6a83928d27e3a96e3f58f1b4620` | `5855742d76dafbfed0664c502cd64fefd590307b` |
| world_model_latest.pt | 27,393,162 | `d7b2866d6fb1009b86ce19d362d9fb742221a8e9a70ec8fe1a6fac6627565b12` | `23881b0fb251d14c6f1234551e761f5ac1d1202c` |

The first VAE response ended at 48,800,500 bytes. No loading occurred. A Range request to the same approved URL returned 206 and the remaining 706,903 bytes; the complete file then matched its pinned blob hash. The failed attempt, partial hash and recovery headers are retained. The WM arrived in one complete approved transfer. No alternate origin or checkpoint was used.

Both files are torch ZIP containers. Archive paths, members, uncompressed sizes and CRCs were inspected before loading. Static unsafe-global scans returned empty lists. Both were loaded with weights_only=True, mmap=True and map_location='cpu'; no allowlists, unsafe fallback, optimizer restoration or training ran. Restricted loading is a mitigation, not a general guarantee against every resource attack; the watchdog enforced the independent limits.

VAE, denoiser, margin head and done head strictly matched frozen architecture tensor keys/shapes. No missing/unexpected required keys were accepted. The WM's embedded VAE tensors exactly equal the separate VAE, and its duplicate denoiser dictionary matches. VAE epoch 30 and nonempty prediction_heads_state_dict establish structural presence of saved heads, not their fitting quality. The source's latent_spatial_size=8 metadata discrepancy remains; actual latent is 4x16x16 and adaptive pooling accepts it. Parameter count: 5,075,917.

Embedded configurations narrow some provenance gaps: VAE data.sequence_length=1, WM sequence_length=16; VAE global_step is present. These are compatible with image VAE training and one-step WM fitting. The stored dataset path contains 'naughty' but provides no numeric flip probability, dataset content hash or complete lineage. Architectural sections match the pinned config; run-specific data paths/training fields are retained verbatim in raw/RESTRICTED_LOAD_REPORT.json. No exact training torch lock, original renderer fingerprint or reliable p=.2/.4 training attribution was found.

Compatibility verdict: PASS for structural frozen-weight CPU loading; probability fidelity and measurement readiness are separate questions. See raw/CHECKPOINT_TENSOR_INVENTORY.json, SERIALIZATION_ARCHIVES.json, WEIGHT_CORRESPONDENCE.json and COMPATIBILITY_PASS.json.
