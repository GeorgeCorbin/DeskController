# src/ui/playback_controls.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PlaybackControlPanel(BoxLayout):
    def __init__(self, spotify_client, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spotify_client = spotify_client

        play_button = Button(text="Play")
        play_button.bind(on_press=lambda x: self.spotify_client.play())

        pause_button = Button(text="Pause")
        pause_button.bind(on_press=lambda x: self.spotify_client.pause())

        next_button = Button(text="Next")
        next_button.bind(on_press=lambda x: self.spotify_client.next_track())

        prev_button = Button(text="Previous")
        prev_button.bind(on_press=lambda x: self.spotify_client.previous_track())


        self.add_widget(prev_button)
        self.add_widget(play_button)
        self.add_widget(pause_button)
        self.add_widget(next_button)
