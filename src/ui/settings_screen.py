# src/ui/settings_screen.py

import subprocess
import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "wifi_settings"

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # WiFi settings
        self.ssid_input = TextInput(hint_text="Enter WiFi SSID", multiline=False)
        self.password_input = TextInput(hint_text="Enter WiFi Password", multiline=False, password=True)

        save_button = Button(text="Save", on_press=self.save_wifi_settings)
        back_button = Button(text="Back", on_press=self.go_back)

        layout.add_widget(Label(text="WiFi Settings", font_size=24))
        layout.add_widget(self.ssid_input)
        layout.add_widget(self.password_input)
        layout.add_widget(save_button)

        # Bluetooth settings
        self.bluetooth_spinner = Spinner(text="Select Bluetooth Device", values=[])
        scan_button = Button(text="Scan for Devices", on_press=self.scan_bluetooth_devices)
        connect_button = Button(text="Connect", on_press=self.connect_bluetooth_device)

        layout.add_widget(Label(text="Bluetooth Settings", font_size=24))
        layout.add_widget(self.bluetooth_spinner)
        layout.add_widget(scan_button)
        layout.add_widget(connect_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_wifi_settings(self, instance):
        ssid = self.ssid_input.text
        password = self.password_input.text
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["networksetup", "-setairportnetwork", "en0", ssid, password], check=True)
            elif platform.system() == "Linux":  # Raspberry Pi
                subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
            print(f"WiFi settings saved: SSID={ssid}, Password={password}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to WiFi: {e}")

    def scan_bluetooth_devices(self, instance):
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(["system_profiler", "SPBluetoothDataType"], capture_output=True, text=True)
                devices = self.parse_macos_bluetooth_devices(result.stdout)
            elif platform.system() == "Linux":  # Raspberry Pi
                result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True)
                devices = self.parse_linux_bluetooth_devices(result.stdout)
            self.bluetooth_spinner.values = devices
        except subprocess.CalledProcessError as e:
            print(f"Failed to scan Bluetooth devices: {e}")

    def connect_bluetooth_device(self, instance):
        device = self.bluetooth_spinner.text
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["blueutil", "--connect", device], check=True)
            elif platform.system() == "Linux":  # Raspberry Pi
                subprocess.run(["bluetoothctl", "connect", device], check=True)
            print(f"Connected to Bluetooth device: {device}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to Bluetooth device: {e}")

    def parse_macos_bluetooth_devices(self, output):
        devices = []
        current_device = None
        for line in output.split("\n"):
            if "Device Name:" in line:
                current_device = line.split(": ")[1].strip()
            elif "Address:" in line and current_device:
                devices.append(current_device)
                current_device = None
        return devices

    def parse_linux_bluetooth_devices(self, output):
        devices = []
        for line in output.split("\n"):
            if "Device" in line:
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    devices.append(parts[2].strip())
        return devices

    def go_back(self, instance):
        self.manager.current = "main"