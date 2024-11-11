from kivy.lang import Builder
from kivy.app import App
from src.ui.app_ui import AudioControllerUI

# Load the style.kv file
Builder.load_file('../styles/style.kv')

class AudioApp(App):
    def build(self):
        return AudioControllerUI()

if __name__ == '__main__':
    AudioApp().run()