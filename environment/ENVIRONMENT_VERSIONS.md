# Environment versions

Analyses reported in the manuscript were run with:

| Component | Version |
|---|---|
| Python | 3.10.14 |
| PyTorch | 2.5.1+cu121 |
| NumPy | 2.2.6 |
| pandas | 2.3.3 |
| scikit-learn | 1.7.2 |
| SciPy | 1.15.3 |
| ESM / fair-esm | 2.0.0 |

Frozen ESM-2 embedding generation used `esm2_t33_650M_UR50D`, representation layer 33, mean pooling over non-special tokens, float32 outputs, and batch size 8. The server-side run used CUDA-enabled PyTorch on an NVIDIA RTX 2080 Ti GPU, but downstream table tracing can be performed from the stored CSV/JSON outputs without GPU access.
