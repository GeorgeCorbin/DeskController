class AudioClient:
    def __init__(self):
        self.is_playing = False
        self.current_track = "Sample Track"

    def play(self):
        self.is_playing = True
        print(f"Playing: {self.current_track}")

    def pause(self):
        self.is_playing = False
        print("Playback paused")

    def next_track(self):
        print("Next track")

    def previous_track(self):
        print("Previous track")
