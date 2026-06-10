# Follow-up Actions & Technical Debt (v3.5.0)

## High Priority
- **Live Deployment**: Execute full 60-minute stress tests on physical 9-panel platforms to validate v3.5.0 ONNX inference stability.
- **ALSA Multi-Card**: Extend `scripts/check_system_health.sh` to support automated card index selection for systems with multiple audio devices.

## Technical Debt
- **Note Vocabulary**: Expand the SymNet vocab in `scripts/ddc_inference.py` to support `dance-double` and higher-difficulty patterns.
- **Node CLI**: Finalize CLI path discovery in `scripts/bobcoin_node_client.py` for standard Linux distributions.
