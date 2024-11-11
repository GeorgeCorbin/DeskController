from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label

class VolumeControlPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Change orientation to vertical

        self.volume_slider = Slider(min=0, max=100, value=50)
        self.volume_slider.bind(value=self.on_volume_change)

        self.volume_label = Label(text="Volume Level: " + str(self.volume_slider.value))

        self.add_widget(self.volume_slider)
        self.add_widget(self.volume_label)  # Add label below the slider

    def on_volume_change(self, instance, value):
        self.volume_label.text = "Volume Level: " + str(int(value))