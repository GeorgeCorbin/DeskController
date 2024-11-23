# src/ui/playback_controls.py
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_file('../styles/style.kv')  # Adjust the path as needed

class PlaybackControlPanel(BoxLayout):
    def __init__(self, spotify_client, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spotify_client = spotify_client
        self.main_screen = main_screen  # Store the main_screen reference

        # Add control buttons
        self.previous_button = Button(text="Previous")
        self.previous_button.bind(on_press=self.previous_track)

        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.play)

        self.pause_button = Button(text="Pause")
        self.pause_button.bind(on_press=self.pause)

        self.next_button = Button(text="Next")
        self.next_button.bind(on_press=self.next_track)

        self.add_widget(self.previous_button)
        self.add_widget(self.play_button)
        self.add_widget(self.pause_button)
        self.add_widget(self.next_button)

    def play(self, instance):
        self.spotify_client.play()
        print("Play button clicked")
        self.main_screen.start_update_track_info()  # Start updating track info after clicking play

    def pause(self, instance):
        self.spotify_client.pause()
        print("Pause button clicked")
        self.main_screen.stop_update_track_info()  # Stop updating track info after clicking pause
        if self.main_screen.track_info_panel.update_event:
            Clock.unschedule(self.main_screen.track_info_panel.update_event)  # Stop updating track info after clicking pause
            self.main_screen.track_info_panel.update_event = None

    def next_track(self, instance):
        self.spotify_client.next_track()
        print("Next button clicked")
        self.main_screen.update_track_info(0)  # Update track info after clicking next

    def previous_track(self, instance):
        self.spotify_client.previous_track()
        print("Previous button clicked")
        self.main_screen.update_track_info(0)  # Update track info after clicking previous