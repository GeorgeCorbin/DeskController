# config/settings.py

import json
import os

# Load secrets from secrets.json
secrets_path = os.path.join(os.path.dirname(__file__), "secrets.json")
with open(secrets_path) as f:
    secrets = json.load(f)

# Spotify OAuth Credentials
SPOTIFY_CLIENT_ID = secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = secrets["SPOTIFY_REDIRECT_URI"]
SPOTIFY_SCOPES = secrets["SPOTIFY_SCOPES"]

# Default Volume Settings
DEFAULT_VOLUME = 100  # Default volume level on startup (range: 0 to 100)

# Playback Settings
AUTO_PLAY_ON_STARTUP = False  # Set to True to auto-play music when the app starts

# Debug Mode
DEBUG_MODE = True  # Set to False to disable console logging
