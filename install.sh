#!/bin/bash

echo "Starting DeskController installation..."

# 1. Update the system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install system dependencies
echo "Installing required system packages..."
sudo apt install -y python3 python3-pip python3-venv

# 3. Set up a virtual environment (optional but recommended)
echo "Setting up Python virtual environment..."
python3 -m venv deskcontroller_env
source deskcontroller_env/bin/activate

# 4. Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# 5. Optional: Create configuration files if needed
CONFIG_FILE="config/settings.py"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating default configuration file..."
    mkdir -p config
    cat <<EOL > $CONFIG_FILE
# Example configuration for DeskController
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
EOL
    echo "Please edit $CONFIG_FILE with your actual Spotify credentials."
fi

# 6. Set up autostart (optional)
echo "Would you like to enable DeskController to start on boot? (y/n)"
read enable_autostart
if [ "$enable_autostart" == "y" ]; then
    AUTOSTART_PATH="/etc/systemd/system/deskcontroller.service"
    echo "Creating systemd service file at $AUTOSTART_PATH"
    sudo tee $AUTOSTART_PATH > /dev/null <<EOL
[Unit]
Description=DeskController Application
After=network.target

[Service]
ExecStart=/path/to/deskcontroller_env/bin/python3 /path/to/DeskController/src/main.py
WorkingDirectory=/path/to/DeskController
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL
    sudo systemctl enable deskcontroller.service
    echo "DeskController set to autostart on boot."
else
    echo "Skipping autostart configuration."
fi

# 7. Add virtual environment activation and PYTHONPATH to shell profile
SHELL_PROFILE="$HOME/.bashrc"
if [ -n "$ZSH_VERSION" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
fi

echo "source $(pwd)/deskcontroller_env/bin/activate" >> $SHELL_PROFILE
echo "export PYTHONPATH=$(pwd)" >> $SHELL_PROFILE
echo "Virtual environment activation and PYTHONPATH added to $SHELL_PROFILE"

echo "Installation complete. To start DeskController manually, run:"
echo "source deskcontroller_env/bin/activate && python3 src/main.py"
