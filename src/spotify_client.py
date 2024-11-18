# src/spotify_client.py

import requests
import json
import os

# def load_tokens():
#     with open("spotify_tokens.json", "r") as f:
#         tokens = json.load(f)
#     return tokens["access_token"]


class SpotifyClient:
    def __init__(self):
        # Load tokens only if the token file exists
        if not os.path.exists("spotify_tokens.json"):
            raise FileNotFoundError("Token file not found. Please log in to Spotify.")

        self.access_token = self.load_tokens()

    def load_tokens(self):
        """Load the access token from the token file."""
        with open("spotify_tokens.json", "r") as f:
            tokens = json.load(f)
        return tokens.get("access_token")

    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_current_playback(self):
        """Get the current track and playback status."""
        url = "https://api.spotify.com/v1/me/player"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()
        return {}

    def play(self):
        """Start or resume playback."""
        url = "https://api.spotify.com/v1/me/player/play"
        requests.put(url, headers=self.get_headers())

    def pause(self):
        """Pause playback."""
        url = "https://api.spotify.com/v1/me/player/pause"
        requests.put(url, headers=self.get_headers())

    def next_track(self):
        """Skip to the next track."""
        url = "https://api.spotify.com/v1/me/player/next"
        requests.post(url, headers=self.get_headers())

    def previous_track(self):
        """Go back to the previous track."""
        url = "https://api.spotify.com/v1/me/player/previous"
        # params = {"device_id": "your_device_id"}
        requests.post(url, headers=self.get_headers())

    def search_track(self, query):
        """Search for a track."""
        url = "https://api.spotify.com/v1/search"
        params = {"q": query, "type": "track"}
        requests.get(url, headers=self.get_headers(), params=params)

    def set_volume(self, volume_percent):
        """Set the volume of the playback."""
        url = "https://api.spotify.com/v1/me/player/volume"
        params = {"volume_percent": volume_percent}
        requests.put(url, headers=self.get_headers(), params=params)

    def get_current_track_duration(self):
        """Get the duration of the current track in milliseconds."""
        playback_info = self.get_current_playback()
        if playback_info and playback_info.get("item"):
            return playback_info["item"]["duration_ms"]
        return 0

    def get_current_track_time_left(self):
        """Get the duration of the current track in milliseconds."""
        playback_info = self.get_current_playback()
        if playback_info and playback_info.get("progress_ms"):
            print((playback_info["item"]["duration_ms"] - playback_info["progress_ms"]) / 1000, " seconds left in the song.")
            return playback_info["item"]["duration_ms"] - playback_info["progress_ms"]
        return 0


