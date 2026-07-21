import time

class FitnessKioskUI:
    """
    A concrete python module representing the State Machine flow of the
    FitnessKiosk minimal UI theme. Used for logic validation.
    """
    STATES = [
        "SCREEN_TITLE_MENU",
        "SCREEN_SELECT_MUSIC",
        "SCREEN_GAMEPLAY",
        "SCREEN_WORKOUT_SUMMARY",
        "SCREEN_FEEDBACK"
    ]

    def __init__(self):
        self.current_state = "SCREEN_TITLE_MENU"
        self.session_active = False
        print(f"[KioskUI] Initialized. Current State: {self.current_state}")

    def handle_input(self, button):
        """Processes hardware pad inputs based on the current screen state."""
        print(f"[KioskUI] Received input: {button}")

        if self.current_state == "SCREEN_TITLE_MENU":
            # In FitnessKiosk, title menu instantly transitions or takes Start to jump into select music.
            if button == "Start":
                self._transition("SCREEN_SELECT_MUSIC")

        elif self.current_state == "SCREEN_SELECT_MUSIC":
            if button in ["Left", "Right"]:
                print("  [KioskUI] Scrolling music wheel...")
            elif button == "Start":
                print("  [KioskUI] Song selected. Entering gameplay.")
                self.session_active = True
                self._transition("SCREEN_GAMEPLAY")

        elif self.current_state == "SCREEN_GAMEPLAY":
            # Gameplay finishes automatically via engine, but for testing we use Start to simulate end of song
            if button == "Start":
                print("  [KioskUI] Song complete. Processing metrics.")
                self._transition("SCREEN_WORKOUT_SUMMARY")

        elif self.current_state == "SCREEN_WORKOUT_SUMMARY":
            # Auto-advances after 10 seconds or via Start
            if button == "Start":
                self._transition("SCREEN_FEEDBACK")

        elif self.current_state == "SCREEN_FEEDBACK":
            if button in ["Left", "Right"]:
                print("  [KioskUI] Selecting feedback rating...")
            elif button == "Start":
                print("  [KioskUI] Feedback submitted. Restarting loop.")
                self.session_active = False
                self._transition("SCREEN_TITLE_MENU")

    def _transition(self, new_state):
        if new_state in self.STATES:
            print(f"[KioskUI] Transition: {self.current_state} -> {new_state}")
            self.current_state = new_state
        else:
            print(f"[KioskUI] ERROR: Invalid state {new_state}")
