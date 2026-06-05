# User Experience Analysis (Internal/Initial)

## Current Implementation State
- **Theme**: Minimalist Kiosk mode, bypasses title screen.
- **Difficulty**: 1-10 fitness scale implemented and visible in Music Wheel and Steps Display.
- **Flow**: Direct to Select Music -> Gameplay -> Evaluation -> Feedback (New) -> Profile Save.
- **Sanitization**: Automatic removal of hands/jacks for cardio flow.

## Predicted User Feedback & Areas for Improvement
1. **Visual Polish**: The current `FitnessKiosk` UI is extremely functional but lacks visual flair. While "stripped down" is the goal, it should still feel high-quality.
2. **Music Selection**: With long sets (60+ min), the standard Music Wheel might be cumbersome. A "Set List" or "Marathon" focused selection UI might be better.
3. **Real-time Stats**: Users likely want to see "Time to Goal", "Estimated Calories", or "Heart Rate Zone" during gameplay.
4. **Input Sensitivity**: FSR sensors are highly sensitive; the feedback mechanism (1, 2, 3) currently uses keyboard/button input, but could be wired to specific pad panels (e.g. Up=Perfect, Left=Easy, Right=Hard).
5. **Chart Flow**: ML-generated charts are good, but the sanitizer is a "dumb" filter. A more "flow-aware" generative model would be superior to a post-processor.

## Immediate Action Items
- [ ] Migrate Feedback screen input to Pad Panels for easier kiosk use.
- [ ] Implement "Workout Summary" overlay that replaces the complex Evaluation screen.
- [ ] Add "Psytrance Progressive" placeholder song pack to verify the ML pipeline.
