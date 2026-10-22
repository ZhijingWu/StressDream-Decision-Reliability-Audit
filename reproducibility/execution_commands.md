# Execution commands and scope

## Portable independent CPU oracle

From the repository root, with existing Python/NumPy:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -B oracle/ORACLE_UNIT_TESTS.py
python -B oracle/ORACLE_IMPLEMENTATION.py --config oracle/CONFIG.json --output-dir reproduced/gate0
```

The test uses a separate scalar reference. The CLI itself creates `raw/` under its new output directory. Do not refreeze an existing config or replace retained results. `requirements-oracle.txt` records NumPy 2.1.3. This publication did not rerun the tests or physical oracle; 16/16 is the retained historical result.

## Retained-data verification

```sh
python -B reproducibility/verify_retained_results.py
```

This checks hashes and aggregates saved data only. It is safe to run without torch or checkpoints.

## Historical stages (not turnkey public commands)

The original Gate 0B orchestration ran init → design → amend_design → freeze_seed_correction → unit tests on design data → one held-out test → report validation. Final held-out specification is V3, seed 202610299; earlier seed collision was corrected before test generation. The omitted machine-specific orchestration hashed its source checkout and original layout. Do not substitute a different script while presenting its new hash as that historical script.

The Gate 1A historical sequence was checkpoint preflight → same-URL transfer recovery/restricted checks → one bounded nominal pilot → offline retained-artifact reporting. Neural phases were not replayed after the final export exception. Original wrappers require the upstream source and weights and are excluded; their names in reports describe past execution, not currently executable public commands. No automatic model-download command is provided.

The note compiles with the commands in `../note/README.md`. Its optional plot script redraws retained numeric values only.
