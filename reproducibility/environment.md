# Recorded environments

Gate 0/0B: Windows 11, Python 3.13.5 (Anaconda), NumPy 2.1.3, float64 independent physical oracle; one OpenBLAS/OpenMP thread. No torch or renderer import in these numerical gates. Frozen source revision: b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d. Gate 0 recorded H12 aggregation time .254790 s; Gate 0B held-out phase 1.140006 s. These are historical single-run timings, not new publication measurements.

Gate 1A: Intel Core Ultra 7 155H CPU; existing Python 3.11.16, torch 2.13.0+cpu (compiled CUDA=None), NumPy 1.23.5, Pillow 12.3.0, Matplotlib 3.7.2. CPU float32, batch one, four intra-op and one inter-op threads. No installs, training or GPU. Worker wall time 37.9847562 s; broad pilot clock ~12.05 min including transfer/recovery/preparation. Sampled aggregate peak RSS 341,688,320 bytes, monitor interval .1 s; transient peaks may be missed. No steering runtime is measured.

Training-time package lock, dataset hash/lineage, training renderer fingerprint and checkpoint flip probability remain unavailable. A structurally compatible current environment is not proof of an exact training-environment match. Machine executable paths were redacted; version metadata and numerical values were retained. See the measured report and actual environment/sampler JSON files.

Document build: MiKTeX pdfTeX 1.40.28, no shell escape. Figure rendering uses retained values and Matplotlib. Document build tools are not oracle dependencies. No new scientific experiment was run for publication.
