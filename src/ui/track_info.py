# src/ui/track_info.py

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

Builder.load_file('../styles/style.kv')  # Adjust the path as needed

class TrackInfoPanel(BoxLayout):
    def __init__(self, spotify_client, **kwargs):
        super().__init__(**kwargs)
        self.spotify_client = spotify_client

        # Add album art and track info
        self.album_art = Image(source="../assets/images/placeholder.png", size=(300, 300), size_hint=(None, None))
        self.track_label = Label(text="Track Title - Artist", font_size=20, halign="center")

        # Center the album art
        self.album_art_layout = BoxLayout(size_hint=(1, None), height=300)
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

        self.add_widget(self.album_art_layout)
        self.add_widget(self.track_label)
        self.add_widget(self.progress_layout)

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
            print("Art", album_art_url)
            # self.album_art = AsyncImage(source=album_art_url)
            # self.album_art.reload()

            # Update progress bar and time labels
            track_duration_ms = track["duration_ms"]
            track_progress_ms = playback_info["progress_ms"]
            self.progress_bar.value = (track_progress_ms / track_duration_ms) * 1000
            self.time_left_label.text = self.format_time(track_progress_ms)
            self.total_time_label.text = self.format_time(track_duration_ms)
        else:
            self.track_label.text = "No track playing"
            # self.album_art.source = "../assets/images/placeholder.png"
            self.progress_bar.value = 0
            self.time_left_label.text = "0:00"
            self.total_time_label.text = "0:00"

    def format_time(self, milliseconds):
        """Format time from milliseconds to MM:SS."""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"