# src/spotify_auth.py

import requests
import base64
import json
import os
import threading
from urllib.parse import urlencode
from flask import Flask, request, redirect
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPES

app = Flask(__name__)
server_thread = None

def get_spotify_auth_url():
    auth_url = "https://accounts.spotify.com/authorize"
    query_params = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": SPOTIFY_SCOPES,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    url = f"{auth_url}?{urlencode(query_params)}"
    return url

def get_spotify_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()

    token_data['status'] = 'authenticated'  # Add this flag

    # Save tokens
    with open("spotify_tokens.json", "w") as f:
        json.dump(token_data, f)

    return token_data

def is_authenticated():
    """Check if authentication tokens are present."""
    token_file = "spotify_tokens.json"
    if not os.path.exists(token_file):
        print("Token file not found.")
        return False
    with open(token_file, "r") as f:
        tokens = json.load(f)
    is_token_present = "access_token" in tokens
    print(f"Access token present: {is_token_present}")
    return is_token_present

@app.route("/login")
def login():
    return redirect(get_spotify_auth_url())


@app.route("/callback")
def callback():
    code = request.args.get("code")
    get_spotify_token(code)

    # Create the auth_complete.flag file to signal authentication completion
    with open("auth_complete.flag", "w") as flag_file:
        flag_file.write("Authenticated")
    print("Auth flag file created.")

    # Return HTML with JavaScript to close the window
    return """
    <html>
        <body>
            <script type="text/javascript">
                window.close();
            </script>
            Spotify authentication successful. You can close this window.
        </body>
    </html>
    """

def run_flask_server():
    """Run the Flask server in a background thread."""
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        server_thread = threading.Thread(target=lambda: app.run(port=8888))
        server_thread.start()

def shutdown_flask_server():
    """Shutdown the Flask server."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()

if __name__ == "__main__":
    app.run(port=8888)
