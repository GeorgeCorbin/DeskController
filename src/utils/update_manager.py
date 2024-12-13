import os
import requests
from datetime import datetime

# GITHUB_TOKEN = os.getenv("GH_TOKEN")  # Load token from environment
UPDATE_URL = "https://raw.githubusercontent.com/georgecorbin/DeskController/main/updates"
UPDATE_LOG = "update_log.txt"
# HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def check_for_updates():
    """Check if a new update is available."""
    # response = requests.get(UPDATE_URL, headers=HEADERS)
    try:
        response = requests.get(f"{UPDATE_URL}/version.txt")
        response.raise_for_status()
        latest_version = response.text.strip()
        current_version = get_current_version()

        if latest_version != current_version:
            print(f"New version available: {latest_version}")
            return True, latest_version
        return False, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False, None

def apply_update():
    """Download and apply the latest update."""
    try:
        response = requests.get(f"{UPDATE_URL}/deskcontroller.tar.gz", stream=True)
        response.raise_for_status()

        with open("update.tar.gz", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        os.system("tar -xzf update.tar.gz -C /path/to/installation")
        log_update()
        print("Update applied successfully.")
    except Exception as e:
        print(f"Error applying update: {e}")

def log_update():
    """Log the update details."""
    with open(UPDATE_LOG, "a") as log:
        log.write(f"Update applied on {datetime.now()}\n")

def get_current_version():
    """Get the current version of the application."""
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"
