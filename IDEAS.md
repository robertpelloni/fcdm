# Ideas & Brainstorming

- **Go Port**: A clean-room implementation of a rhythm engine in Go could provide better concurrency handling and easier deployment as a single binary.
- **Web-based Kiosk**: Could the UI be React/Next.js communicating with a Go backend?
- **VR Integration**: For even more immersive cardio.
- **Heart Rate Sync**: Dynamically adjust difficulty or visual feedback based on real-time heart rate data.
- **Global Leaderboards**: Competitive fitness tracking.
- **ML Refinement**: Train a model specifically on psytrance "fitness" charts rather than just post-processing human charts.
- **Audio-to-Chart End-to-End**: Combine `audio_processor.py` with an ML generator to produce fully-synced, sanitized fitness charts from any raw MP3.
- **DDC ONNX Port**: Port the DDC model weights to ONNX format to remove the heavy `tensorflow` dependency and improve inference speed on edge hardware.
- **Web-based Calibration Dashboard**: A React-based interface for the FSR calibration utility, communicating with the Teensy over WebSerial.
