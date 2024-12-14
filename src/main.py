import os
from kivy.lang import Builder
from kivy.app import App
from ui.app_ui import AudioControllerApp
from kivy.clock import Clock
from datetime import datetime, timedelta
from src.utils.update_manager import check_for_updates, apply_update

# Load the style.kv file
stylesPath = os.path.join(os.path.dirname(__file__), "../../styles/style.kv")
Builder.load_file(stylesPath)

class AudioApp(App):
    def build(self):
        self.run_update_check(0)
        return AudioControllerApp()

    def schedule_update_checks(self):
        """Schedule daily update checks."""
        now = datetime.now()
        next_check = (now + timedelta(days=1)).replace(hour=3, minute=0, second=0, microsecond=0)
        delay = (next_check - now).total_seconds()

        # Schedule the first update check
        Clock.schedule_once(self.run_update_check, delay)

    def run_update_check(self, dt):
        """Check for updates and re-schedule the next daily check."""
        is_available, version = check_for_updates()
        if is_available:
            print(f"New update available: {version}. Applying...")
            apply_update()

        # Schedule the next check 24 hours later
        Clock.schedule_once(self.run_update_check, 86400)

if __name__ == "__main__":
    AudioApp().run()