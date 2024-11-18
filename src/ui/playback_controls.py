# src/ui/playback_controls.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PlaybackControlPanel(BoxLayout):
    def __init__(self, spotify_client, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spotify_client = spotify_client
        self.main_screen = main_screen  # Store the main_screen reference

        play_button = Button(text="Play")
        play_button.bind(on_press=self.play)

        pause_button = Button(text="Pause")
        pause_button.bind(on_press=self.pause)

        next_button = Button(text="Next")
        next_button.bind(on_press=self.next_track)

        prev_button = Button(text="Previous")
        prev_button.bind(on_press=self.previous_track)

        self.add_widget(prev_button)
        self.add_widget(play_button)
        self.add_widget(pause_button)
        self.add_widget(next_button)

    def play(self, instance):
        self.spotify_client.play()
        print("Play button clicked")
        self.main_screen.start_update_track_info()  # Start updating track info after clicking play

    def pause(self, instance):
        self.spotify_client.pause()
        print("Pause button clicked")
        self.main_screen.stop_update_track_info()  # Stop updating track info after clicking pause

    def next_track(self, instance):
        self.spotify_client.next_track()
        print("Next button clicked")
        self.main_screen.update_track_info(0)  # Update track info after clicking next

    def previous_track(self, instance):
        self.spotify_client.previous_track()
        print("Previous button clicked")
        self.main_screen.update_track_info(0)  # Update track info after clicking previous