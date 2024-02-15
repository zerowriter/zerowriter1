
class MockKeyboard:
    def __init__(self):
        self.press_handlers = []
        self.release_handlers = []

    def on_press(self, callback, suppress=False):
        self.press_handlers.append(callback)

    def on_release(self, callback, suppress=False):
        self.release_handlers.append(callback)

    def simulate_key_press(self, key):
        for handler in self.press_handlers:
            handler(key)

    def simulate_key_release(self, key):
        for handler in self.release_handlers:
            handler(key)

    def unhook_all(self):
        self.press_handlers = []
        self.release_handlers = []

    def hook(self, callback):
        # This method is a placeholder to simulate hooking key events.
        # In a real scenario, this would hook into actual key events.
        pass

    def hook_key(self, key, callback_press, callback_release=None, suppress=False):
        # This method is a placeholder to simulate hooking specific key events.
        # In a real scenario, this would hook into actual key events for a specific key.
        pass

# Example usage:
# mock_keyboard = MockKeyboard()
# mock_keyboard.on_press(lambda e: print(f"Key pressed: {e.name}"))
# mock_keyboard.on_release(lambda e: print(f"Key released: {e.name}"))
# mock_keyboard.simulate_key_press('a')  # Simulate the 'a' key being pressed
# mock_keyboard.simulate_key_release('a')  # Simulate the 'a' key being released
