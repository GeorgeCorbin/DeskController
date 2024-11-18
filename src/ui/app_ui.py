# src/ui/app_ui.py

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os
from kivy.lang import Builder

from src.ui.login_screen import LoginScreen
from src.spotify_client import SpotifyClient
from src.ui.track_info import TrackInfoPanel
from src.ui.volume_control import VolumeControlPanel
from src.ui.playback_controls import PlaybackControlPanel

Builder.load_file('../styles/style.kv')  # Adjust the path as needed

class MainScreen(Screen):
    def __init__(self, app_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.app_manager = app_manager
        self.spotify_client = SpotifyClient()

        # Main layout
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.add_widget(self.layout)
        print("MainScreen layout added to screen.")

        # Only add the panels if they are not already in the layout
        if 'track_info_panel' not in self.ids:
            self.track_info_panel = TrackInfoPanel(self.spotify_client)
            self.layout.add_widget(self.track_info_panel)
            self.ids['track_info_panel'] = self.track_info_panel
            print("TrackInfoPanel added.")

        if 'playback_panel' not in self.ids:
            self.playback_panel = PlaybackControlPanel(self.spotify_client, self)
            self.layout.add_widget(self.playback_panel)
            self.ids['playback_panel'] = self.playback_panel
            print("PlaybackControlPanel added.")

        if 'volume_control' not in self.ids:
            self.volume_control = VolumeControlPanel(self.spotify_client)
            self.layout.add_widget(self.volume_control)
            self.ids['volume_control'] = self.volume_control
            print("VolumeControl added.")


        # Schedule initial track info update
        self.update_track_info(0)

    def update_track_info(self, dt):
        self.track_info_panel.update_track_info(dt)
        track_duration_ms = self.spotify_client.get_current_track_time_left()
        if track_duration_ms > 0:
            # Schedule the next update 1 second after the track ends
            Clock.schedule_once(self.update_track_info, (track_duration_ms / 1000) + 1)

    def start_update_track_info(self):
        """Start updating track info."""
        self.update_track_info(0)

    def stop_update_track_info(self):
        """Stop updating track info."""
        if hasattr(self, 'update_event'):
            Clock.unschedule(self.update_event)

    def logout(self, instance):
        """Handle logout by deleting the token file and resetting to the login screen."""
        try:
            # Delete the token file and the flag file to effectively log out
            if os.path.exists("spotify_tokens.json"):
                os.remove("spotify_tokens.json")
            if os.path.exists("auth_complete.flag"):
                os.remove("auth_complete.flag")
        except Exception as e:
            print(f"Error during logout: {e}")

        # Switch back to the login screen and restart the authentication check
        self.app_manager.current = "login"
        self.app_manager.start_auth_check()  # Restart flag check in AudioControllerApp

class LoginScreenWrapper(Screen):
    def __init__(self, app_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        self.app_manager = app_manager
        self.add_widget(LoginScreen())
        print("LoginScreenWrapper initialized.")

class AudioControllerApp(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize login and main screens
        self.login_screen = LoginScreenWrapper(app_manager=self)
        self.main_screen = MainScreen(app_manager=self)

        self.add_widget(self.login_screen)
        self.add_widget(self.main_screen)

        # Set initial screen to login and start authentication check
        self.current = "login"
        self.start_auth_check()

    def start_auth_check(self):
        """Start or restart the periodic check for the authentication flag."""
        self.auth_check_event = Clock.schedule_interval(self.check_authentication_complete, 1)
        print("Authentication check scheduled.")

    def check_authentication_complete(self, dt):
        """Check if the authentication flag file exists and switch to the main screen if found."""
        if os.path.exists("auth_complete.flag"):
            print("Authentication flag detected. Switching to main screen.")
            self.current = "main"
            # os.remove("auth_complete.flag")  # Remove the flag file after detection
            Clock.unschedule(self.auth_check_event)  # Stop further checks

    def on_stop(self):
        """Clean up any resources, such as the auth check event."""
        Clock.unschedule(self.auth_check_event)