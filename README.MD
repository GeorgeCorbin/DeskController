# DeskController
## Description
A Raspberry Pi based Music Controller for your desk. This project is a simple music controller that can be used to play music from Spotify and other music services. The controller will have basic playback controls (Play, Pause, Next, Previous, Volume Control) and will display track information (Artist, Title, Album Picture). The controller will also have a settings menu for connecting to WiFi and bluetooth devices. The controller will be built using a Raspberry Pi and a touchscreen display.

## Purpose
No more looking at your phone to change the music and losing your focus. No more putting your speaker system in pairing mode to have your friend connect. The DeskController will already be connected and easy to log into your music services. No more giving your phone to someone to queue songs or change the volume. The DeskController has a touchscreen to do it all on the interface. The DeskController will be easy to use and make listening to music alone or with friends more seamless than ever.

## General Features:
- Basic UI with Play/Pause, Next, Previous, Volume Control
- Basic Audio Playback with Spotify
- Login with Spotify OAuth
- Settings menu for connecting to WiFi and bluetooth devices

## Progress List:
#### Complete:
- Basic UI with Play/Pause, Next, Previous, Volume Control
- Basic Audio Playback with Spotify
- Progress Bar for song progress
- Fixed Volume Control
- Basic Track Info (Artist, Title, Album Picture)
- Fixed Album Art

#### In Progress:
- Change Buttons to alternate for play/pause
- Add playlist section to select songs from user's library
- Add search functionality to search for songs

#### To Do:
- Fix wifi and bluetooth section to find correct devices
- Working on adding Spotify Connect ability (raspotify)
- Change Buttons to alternate for play/pause
- Add playlist section to select songs from user's library
- Add search functionality to search for songs
- Add other music services (Apple Music, Amazon Music, etc.) for playback using respective OAuths
- Make it so the application does not continuously update when the play bar is not being used/shown

#### Ideas:
- Add a settings menu for changing the theme of the UI
- Create log in page for personal account that is connected with all services already
- NFC reader to touch phone to player to automatically login with account to connect music services

## Important Notes
- After cloning repo you must run `install.sh` to install dependencies and setup the project
- In order to run install.sh you must have read, write, execute permissions on the DeskController directory
  - Run `chmod u+wrx` to give the directory permissions (may have to run as sudo)
- You must have a Spotify Developer account to use the Spotify API
  - Create a new app in the Spotify Developer Dashboard
  - Add `http://localhost:8080` as a Redirect URI in the app settings
  - Copy the Client ID and Client Secret into to your `.env` file
- Updates are set to pull from /usr/local so make sure that is where the repository is located

```
AudioController/
├── src/
│   ├── main.py                 # Main entry point to launch the Kivy app
│   ├── audio_client.py         # Core logic for audio playback actions
│   ├── spotify_auth.py         # Core logic for Spotify OAuth
│   ├── spotify_client.py       # Core logic for Spotify API requests
│   ├── ui/
│   │   ├── __init__.py         # Makes `ui` a package
│   │   ├── app_ui.py           # Main Kivy App class and UI setup
│   │   ├── login_screen.py     # Kivy Widget for music service login
│   │   ├── playback_controls.py # Kivy Widget for playback controls (Play, Pause, etc.)
│   │   ├── settings_screen.py  # Kivy Widget for settings menu
│   │   ├── track_info.py       # Kivy Widget to display track information (title, artist, etc.)
│   │   └── volume_control.py   # Kivy Widget for volume control
│   │
├── assets/
│   ├── images/                 # Images such as album art, icons, or backgrounds
│   │   └── placeholder.png     # Placeholder image for testing
│   └── sounds/                 # Audio files for testing (if needed)
│
├── config/
│   ├── settings.py             # Configuration settings like default volume, theme colors
│
├── styles/
│   ├── style.kv                # Kivy style file for defining global UI styling
│
├── requirements.txt            # Python dependencies for the project
├── install.sh                  # Script to install dependencies and setup the project
└── README.md                   # Project overview and setup instructions
```