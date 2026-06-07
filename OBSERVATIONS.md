# Observations & Final Report (v1.3.0)

## System Performance
- **Music Ingestion**: The initial ingestion of raw audio is resource-intensive due to `librosa` analysis. However, the implemented "skip logic" in `scripts/ingest_music.py` ensures that subsequent boots are near-instantaneous.
- **Audio Analysis**: `librosa` version 0.11.0 is sensitive to audio length. Synthetic samples shorter than 5 seconds may yield erratic BPM results (e.g., BPM=0.0). Real-world psycho-trance sets (60+ minutes) are expected to be highly stable.
- **Deprecation Warnings**: Several `DeprecationWarning` messages are emitted by `audioread` (an internal dependency of `librosa`) regarding Python 3.13. These are non-blocking and will need to be addressed when the system migrates to Python 3.13+.

## Known Issues & Limitations
- **BPM Injection**: The `stream_sanitizer.py` uses a simple regex to replace the first `#BPMS` tag it finds. This is ideal for single-BPM cardio tracks but may fail for complex charts with multi-BPM changes.
- **Outdated Artifacts**: The file `fitness-center-dance-machine-v1.0.0.zip` in the root is now outdated. It should be regenerated to include the v1.3.0 changes before a physical kiosk deployment.
- **Theme Constraints**: The `FitnessKiosk` theme depends on `_fallback`. If ITGMania's internal `_fallback` structure changes significantly, the `StepsDisplayList` override may require adjustments.

## Verification Summary
- **CI Pipeline**: GitHub Actions workflow established and verified.
- **Submodules**: `bobmania` and `itgmania` synced and tested.
- **Integration**: End-to-end flow from raw audio to "Fitness Verified" UI badge is confirmed.
