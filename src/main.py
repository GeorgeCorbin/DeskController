from kivy.lang import Builder
from kivy.app import App
from ui.app_ui import AudioControllerApp

# Load the style.kv file
Builder.load_file('../styles/style.kv')

class AudioApp(App):
    def build(self):
        return AudioControllerApp()

if __name__ == "__main__":
    AudioApp().run()