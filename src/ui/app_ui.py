# src/ui/app_ui.py
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
import os
from kivy.lang import Builder

from src.ui.login_screen import LoginScreen
from src.spotify_client import SpotifyClient
from src.ui.settings_screen import SettingsScreen
from src.ui.track_info import TrackInfoPanel
from src.ui.volume_control import VolumeControlPanel
from src.ui.playback_controls import PlaybackControlPanel

Builder.load_file('../styles/style.kv')  # Adjust the path as needed

class MainScreen(Screen):
    def __init__(self, app_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.app_manager = app_manager
        self.spotify_client = None
        # self.spotify_client.register_device()  # Register the device
        # self.spotify_client.transfer_playback(device_id="a535e4387c29e4c2b6f1f1e11bc93f4f39a2645a")

        # Main layout
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.add_widget(self.layout)
        print("MainScreen layout added to screen.")

        # Add settings and logout buttons in the top right corner
        self.button_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), size=(200, 50))
        self.settings_button = Button(text="Settings", size_hint=(None, None), size=(100, 50))
        self.settings_button.bind(on_press=self.go_to_settings_screen)
        self.logout_button = Button(text="Logout", size_hint=(None, None), size=(100, 50))
        self.logout_button.bind(on_press=self.logout)
        self.button_layout.add_widget(self.settings_button)
        self.button_layout.add_widget(self.logout_button)

        self.anchor_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        self.anchor_layout.add_widget(self.button_layout)
        self.layout.add_widget(self.anchor_layout)

    def initialize_spotify_client(self):
        """Initialize the Spotify client after successful login."""
        self.spotify_client = SpotifyClient()

        # Only add the panels if they are not already in the layout
        if 'track_info_panel' not in self.ids:
            self.track_info_panel = TrackInfoPanel(self.spotify_client)
            self.layout.add_widget(self.track_info_panel)
            self.ids['track_info_panel'] = self.track_info_panel
            print("TrackInfoPanel added.")

        # Add Album Art and Track Info
        self.album_art_layout = self.track_info_panel.album_art_layout
        self.track_label = self.track_info_panel.track_label
        self.layout.add_widget(self.album_art_layout)
        self.layout.add_widget(self.track_label)
        print("Album Art and Track Info added.")

        # Add playback control panel
        if 'playback_panel' not in self.ids:
            self.playback_panel = PlaybackControlPanel(self.spotify_client, self)
            self.layout.add_widget(self.playback_panel)
            self.ids['playback_panel'] = self.playback_panel
            print("PlaybackControlPanel added.")

        # Add progress bar and time labels
        self.progress_layout = self.track_info_panel.progress_layout
        self.layout.add_widget(self.progress_layout)
        print("Progress bar and time labels added.")

        if 'volume_control' not in self.ids:
            self.volume_control = VolumeControlPanel(self.spotify_client)
            self.layout.add_widget(self.volume_control)
            self.ids['volume_control'] = self.volume_control
            print("VolumeControl added.")


        # Schedule initial track info update
        self.update_track_info(0)

    def go_to_settings_screen(self, instance):
        self.manager.current = "settings_screen"

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
            token_file_path = "spotify_tokens.json"
            if os.path.exists(token_file_path):
                os.remove(token_file_path)
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
        self.settings_screen = SettingsScreen()

        self.add_widget(self.login_screen)
        self.add_widget(self.main_screen)
        self.add_widget(self.settings_screen)

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
            self.main_screen.initialize_spotify_client()  # Initialize Spotify client after login
            os.remove("auth_complete.flag")  # Remove the flag file after detection
            Clock.unschedule(self.auth_check_event)  # Stop further checks

    def on_stop(self):
        """Clean up any resources, such as the auth check event."""
        Clock.unschedule(self.auth_check_event)