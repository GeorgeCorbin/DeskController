import os
import requests
import tarfile
import tempfile
from datetime import datetime
from packaging.version import parse  # For robust version comparison
import shutil  # For directory and file operations

UPDATE_URL = "https://raw.githubusercontent.com/georgecorbin/DeskController/updates"
UPDATE_LOG = "update_log.txt"
INSTALLATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

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
        print("No updates available.")
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

            # Safely move or merge files
            merge_directories(tmp_dir, INSTALLATION_PATH)

        log_update()
        print("Update applied successfully.")
    except Exception as e:
        print(f"Error applying update: {e}")

def merge_directories(src_dir, dst_dir):
    """Recursively merge directories and replace files."""
    for item in os.listdir(src_dir):
        if item == ".git":  # Skip the .git directory
            continue

        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path)
            else:
                merge_directories(src_path, dst_path)  # Recursively merge subdirectories
        else:
            shutil.copy2(src_path, dst_path)  # Replace file if it exists

def log_update():
    """Log the update details."""
    with open(os.path.join(INSTALLATION_PATH, UPDATE_LOG), "a") as log:
        log.write(f"Update applied on {datetime.now()}\n")

def get_current_version():
    """Get the current version of the application."""
    try:
        version_path = os.path.join(INSTALLATION_PATH, "version.txt")
        with open(version_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"