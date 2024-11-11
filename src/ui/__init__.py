# src/ui/__init__.py

# Import core UI components for easier access
from .playback_controls import PlaybackControlPanel
from .track_info import TrackInfoPanel
from .volume_control import VolumeControlPanel
from .app_ui import AudioControllerUI

# List exports for cleaner imports elsewhere in the project
__all__ = [
    "PlaybackControlPanel",
    "TrackInfoPanel",
    "VolumeControlPanel",
    "AudioControllerUI"
]
