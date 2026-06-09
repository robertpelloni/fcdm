# Follow-up Actions & Technical Debt (v2.0.0)

## High Priority
- **Hardware Integration**: Conduct first live user tests on the physical 9-panel platform.
- **ML Optimization**: Port the SymNet (Selection) model to ONNX to replace the current ergonomic state machine.

## Technical Debt
- **Dependency Management**: Monitor `librosa` and `numba` for compatibility with future Python versions.
- **Bobcoin Node**: Implement a robust error-handling layer for cases where the local supernode is offline.
