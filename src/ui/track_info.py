# src/ui/track_info.py

import requests
import os

from kivy.lang import Builder
from kivy.lib.ddsfile import align_value
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

Builder.load_file('../styles/style.kv')  # Adjust the path as needed
placeholder = os.path.join(os.path.dirname(__file__), "../assets/images/placeholder.png")

class TrackInfoPanel(BoxLayout):
    def __init__(self, spotify_client, **kwargs):
        super().__init__(**kwargs)
        self.spotify_client = spotify_client
        self.current_album_art_path = None

        # Add album art and track info
        self.album_art = Image(source=placeholder, size=(300, 300), size_hint=(None, None))
        self.track_label = Label(text="Track Title - Artist", font_size=20, halign="center")

        # Center the album art
        self.album_art_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=300, padding=10)
        self.album_art_layout.add_widget(self.album_art)

        # Add progress bar and time labels
        self.progress_bar = ProgressBar(max=1000)
        self.time_left_label = Label(text="0:00", size_hint_x=0.1)
        self.total_time_label = Label(text="0:00", size_hint_x=0.1)

        # Layout for progress bar and time labels
        self.progress_layout = BoxLayout(orientation='horizontal')
        self.progress_layout.add_widget(self.time_left_label)
        self.progress_layout.add_widget(self.progress_bar)
        self.progress_layout.add_widget(self.total_time_label)

        # Add widgets to the Main Screen layout for proper display
        # self.add_widget(self.album_art_layout)
        # self.add_widget(self.track_label)
        # self.add_widget(self.progress_layout)

        # Schedule updates
        self.update_event = None
        self.schedule_update()

    def schedule_update(self):
        """Schedule the update if a track is playing."""
        if self.update_event:
            Clock.unschedule(self.update_event)
        self.update_event = Clock.schedule_interval(self.update_track_info, 1)

    def update_track_info(self, dt):
        """Update displayed track info."""
        playback_info = self.spotify_client.get_current_playback()
        if playback_info and playback_info.get("item"):
            track = playback_info["item"]
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            track_name = track["name"]
            self.track_label.text = f"{track_name} - {artist_names}"
            album_art_url = self.spotify_client.get_album_art_url()
            self.download_album_art(album_art_url)

            # Update progress bar and time labels
            track_duration_ms = track["duration_ms"]
            track_progress_ms = playback_info["progress_ms"]
            self.progress_bar.value = (track_progress_ms / track_duration_ms) * 1000
            self.time_left_label.text = self.format_time(track_progress_ms + 750) # +750 to fix appearance of delay
            self.total_time_label.text = self.format_time(track_duration_ms)
        else:
            self.track_label.text = "No track playing"
            self.album_art.source = placeholder
            self.progress_bar.value = 0
            self.time_left_label.text = "0:00"
            self.total_time_label.text = "0:00"
            self.delete_album_art()

    def download_album_art(self, url):
        """Download the album art image from the given URL."""
        if self.current_album_art_path:
            self.delete_album_art()
        response = requests.get(url)
        if response.status_code == 200:
            self.current_album_art_path = os.path.join(os.path.dirname(__file__), "../../assets/images/current_album_art.png")
            print(self.current_album_art_path)
            with open(self.current_album_art_path, "wb") as f:
                f.write(response.content)
            self.album_art.source = self.current_album_art_path
            self.album_art.reload()

    def delete_album_art(self):
        """Delete the current album art image."""
        if self.current_album_art_path and os.path.exists(self.current_album_art_path):
            os.remove(self.current_album_art_path)
            self.current_album_art_path = None

    def format_time(self, milliseconds):
        """Format time from milliseconds to MM:SS."""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"