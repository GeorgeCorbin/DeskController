# src/ui/track_info.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

class TrackInfoPanel(BoxLayout):
    def __init__(self, spotify_client, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spotify_client = spotify_client

        # Display elements
        self.track_label = Label(text="Track Title - Artist", font_size=24)
        self.album_art = Image(source="assets/images/placeholder.png")

        # Add elements to layout
        self.add_widget(self.album_art)
        self.add_widget(self.track_label)

    def update_track_info(self):
        """Fetch and display current track info."""
        playback_info = self.spotify_client.get_current_playback()
        if playback_info and playback_info.get("item"):
            track = playback_info["item"]
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            track_name = track["name"]
            self.track_label.text = f"{track_name} - {artist_names}"

            # Update album art
            album_art_url = track["album"]["images"][0]["url"]
            self.album_art.source = album_art_url
            self.album_art.reload()
