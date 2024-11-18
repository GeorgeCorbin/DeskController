# src/ui/login_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import webbrowser
from kivy.clock import Clock
from src.spotify_auth import get_spotify_auth_url, run_flask_server, is_authenticated

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Start the Flask server for OAuth
        run_flask_server()

        # Add a welcome message
        self.add_widget(Label(text="Welcome to the DeskController", font_size=24))
        self.add_widget(Label(text="Please log in to Spotify to continue", font_size=18))

        # Add the login button
        login_button = Button(text="Log in with Spotify", font_size=20, size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        login_button.bind(on_press=self.open_spotify_login)
        self.add_widget(login_button)

    def open_spotify_login(self, instance):
        # Open the Spotify authentication URL in the default web browser
        webbrowser.open(get_spotify_auth_url())

    def check_authentication_status(self, dt):
        """Check if user is authenticated and switch to main screen if true."""
        if is_authenticated():
            self.parent.current = "main"
            return False  # Stop the Clock when authenticated