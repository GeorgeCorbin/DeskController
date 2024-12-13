# config/settings.py

from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Spotify OAuth Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPES = os.getenv("SPOTIFY_SCOPES")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET or not SPOTIFY_REDIRECT_URI or not SPOTIFY_SCOPES:
    raise EnvironmentError("Missing required environment variables.")

# Default Volume Settings
DEFAULT_VOLUME = 100  # Default volume level on startup (range: 0 to 100)

# Playback Settings
AUTO_PLAY_ON_STARTUP = False  # Set to True to auto-play music when the app starts

# Debug Mode
DEBUG_MODE = True  # Set to False to disable console logging
