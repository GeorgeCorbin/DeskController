# src/spotify_client.py

import requests
import json

def load_tokens():
    with open("spotify_tokens.json", "r") as f:
        tokens = json.load(f)
    return tokens["access_token"]

class SpotifyClient:
    def __init__(self):
        self.access_token = load_tokens()

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
        requests.post(url, headers=self.get_headers())
