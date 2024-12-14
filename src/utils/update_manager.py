import os
import requests
import tarfile
import tempfile
from datetime import datetime
from packaging.version import parse  # For robust version comparison

UPDATE_URL = "https://raw.githubusercontent.com/georgecorbin/DeskController/updates"
UPDATE_LOG = "update_log.txt"
INSTALLATION_PATH = os.path.join(os.path.dirname(__file__), "../../")

def check_for_updates():
    """Check if a new update is available."""
    try:
        response = requests.get(f"{UPDATE_URL}/version.txt")
        response.raise_for_status()
        latest_version = response.text.strip()
        current_version = get_current_version()

        if parse(latest_version) > parse(current_version):
            print(f"New version available: {latest_version}")
            return True, latest_version
        return False, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False, None

def apply_update():
    """Download and apply the latest update."""
    try:
        response = requests.get(f"{UPDATE_URL}/DeskController.tar.gz", stream=True)
        response.raise_for_status()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tar_path = os.path.join(tmp_dir, "update.tar.gz")
            with open(tar_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(tmp_dir)

            # Move files from temporary directory to the installation path
            for item in os.listdir(tmp_dir):
                src = os.path.join(tmp_dir, item)
                dst = os.path.join(INSTALLATION_PATH, item)
                if os.path.isdir(src):
                    os.rename(src, dst)
                else:
                    os.replace(src, dst)

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