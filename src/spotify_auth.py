# src/spotify_auth.py

import requests
import base64
from urllib.parse import urlencode
from flask import Flask, request, redirect
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPES

app = Flask(__name__)

# Step 1: Authorization URL
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

# Step 2: Exchange Code for Token
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
    return response.json()

# Step 3: Spotify Login and Callback Routes
@app.route("/login")
def login():
    return redirect(get_spotify_auth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = get_spotify_token(code)
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # Save tokens for future use
    with open("spotify_tokens.json", "w") as f:
        f.write(f'{{"access_token": "{access_token}", "refresh_token": "{refresh_token}"}}')
    return "Spotify authentication successful. You can close this window."

if __name__ == "__main__":
    app.run(port=8888)
