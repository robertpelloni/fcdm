1. **Understand Task**: "implement the FitnessKiosk minimal UI layer as a concrete module with basic screen flow and input handling, then wire it to a stubbed version of the ITGMania engine interface so we can validate the kiosk loop end-to-end."
2. **Interpretation**: The user wants a Python mock/stub of the ITGMania engine (`itgmania_stub.py`) and a concrete `kiosk_ui.py` module that models the specific screen transitions (Title -> SelectMusic -> Gameplay -> WorkoutSummary -> Feedback -> Title). This allows unit testing the state machine loop of the kiosk without booting the heavy C++ engine.
3. **Execution**:
   - Create `scripts/kiosk_ui.py`: A class `FitnessKioskUI` with states (`SCREEN_TITLE_MENU`, `SCREEN_SELECT_MUSIC`, `SCREEN_GAMEPLAY`, `SCREEN_WORKOUT_SUMMARY`, `SCREEN_FEEDBACK`). Handle input methods like `handle_input(button)`.
   - Create `scripts/itgmania_stub.py`: A stub representing the engine that initializes the UI module, pushes dummy inputs ("Start", "Left", "Right") periodically to prove the end-to-end loop transitions back to the start.
4. **Validation**: Run the stub script and assert it successfully completes a full loop cycle.
5. **Submit**: Pre-commit and submit.
