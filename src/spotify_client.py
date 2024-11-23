# src/spotify_client.py

import requests
import json
import os

class SpotifyClient:
    def __init__(self):
        if not os.path.exists("spotify_tokens.json"):
            raise FileNotFoundError("Token file not found. Please log in to Spotify.")
        self.access_token = self.load_tokens()
        self.device_id = None

    def load_tokens(self):
        with open("spotify_tokens.json", "r") as f:
            tokens = json.load(f)
        return tokens.get("access_token")

    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def register_device(self):
        """Register the application as a Spotify Connect device."""
        url = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            devices = response.json().get("devices", [])
            print("Devices:", devices)
            for device in devices:
                if device["name"] == "DeskController":
                    self.device_id = device["id"]
                    break
            if not self.device_id:
                print("Device not found. Please ensure your device is registered in Spotify Connect.")
        else:
            print("Failed to get devices:", response.json())

    def transfer_playback(self, device_id, force_play=True):
        """Transfer playback to a specific device."""
        url = "https://api.spotify.com/v1/me/player"
        data = {
            "device_ids": [device_id],
            "play": force_play
        }
        response = requests.put(url, headers=self.get_headers(), json=data)
        if response.status_code == 204:
            print("Playback transferred successfully.")
        else:
            print("Failed to transfer playback:", response.json())

    def get_current_playback(self):
        url = "https://api.spotify.com/v1/me/player"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()
        return {}

    def play(self):
        # url = f"https://api.spotify.com/v1/me/player/play?device_id={self.device_id}"
        url = f"https://api.spotify.com/v1/me/player/play"
        requests.put(url, headers=self.get_headers())

    def pause(self):
        url = f"https://api.spotify.com/v1/me/player/pause"
        requests.put(url, headers=self.get_headers())

    def next_track(self):
        url = f"https://api.spotify.com/v1/me/player/next"
        requests.post(url, headers=self.get_headers())

    def previous_track(self):
        url = f"https://api.spotify.com/v1/me/player/previous"
        requests.post(url, headers=self.get_headers())

    def set_volume(self, volume_percent):
        # url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percent}&device_id={self.device_id}"
        url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percent}"
        requests.put(url, headers=self.get_headers())

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

    def get_album_art_url(self):
        playback_info = self.get_current_playback()
        if playback_info and playback_info.get("item"):
            return playback_info["item"]["album"]["images"][0]["url"]
        return ""