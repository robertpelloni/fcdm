import time
from kiosk_ui import FitnessKioskUI

def simulate_engine_loop():
    print("=== ITGMania Engine Stub ===")
    print("Booting minimal UI module...\n")

    ui = FitnessKioskUI()

    # Define a sequence of inputs to simulate a user session
    input_sequence = [
        ("Start", 1.0),   # Jump past Title Menu
        ("Right", 0.5),   # Scroll
        ("Right", 0.5),   # Scroll
        ("Start", 1.0),   # Select Song -> Gameplay
        ("Start", 2.0),   # Fast forward gameplay to completion -> Workout Summary
        ("Start", 1.0),   # Skip summary -> Feedback
        ("Left", 0.5),    # Select rating
        ("Start", 1.0),   # Submit feedback -> Back to Title
    ]

    for button, delay in input_sequence:
        time.sleep(delay)
        ui.handle_input(button)

    # Verify the loop completes successfully
    assert ui.current_state == "SCREEN_TITLE_MENU", "State machine failed to return to Title Menu"
    print("\n[EngineStub] Validation Complete: End-to-end Kiosk loop is functional.")

if __name__ == "__main__":
    simulate_engine_loop()
