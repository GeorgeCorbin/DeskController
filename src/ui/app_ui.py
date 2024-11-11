# src/ui/app_ui.py

from kivy.uix.boxlayout import BoxLayout
from src.spotify_client import SpotifyClient
from src.ui.track_info import TrackInfoPanel
from src.ui.playback_controls import PlaybackControlPanel

class AudioControllerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spotify_client = SpotifyClient()

        # Track info panel
        self.track_info_panel = TrackInfoPanel(self.spotify_client)
        self.add_widget(self.track_info_panel)

        # Playback control panel
        self.playback_panel = PlaybackControlPanel(self.spotify_client)
        self.add_widget(self.playback_panel)

        # Initial update of track info
        self.update_track_info()

    def update_track_info(self):
        """Fetch and update track information every 10 seconds."""
        self.track_info_panel.update_track_info()
        self.schedule_update()

    def schedule_update(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.update_track_info(), 10)
