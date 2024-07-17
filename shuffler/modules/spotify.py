import requests
import re
from pydantic import BaseModel
from typing import List


class ExternalUrls(BaseModel):
    spotify: str


class Track(BaseModel):
    id: str
    name: str
    external_urls: ExternalUrls


class PlaylistItem(BaseModel):
    track: Track


class Playlist(BaseModel):
    items: List[PlaylistItem]


class Spotify:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_token()

    def _get_token(self) -> str:
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(
            auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        auth_response_data = auth_response.json()
        return auth_response_data["access_token"]

    def list_playlist_urls(self, playlist_url: str) -> List[str]:
        playlist_id = self._extract_playlist_id(playlist_url)
        headers = {"Authorization": f"Bearer {self.token}"}

        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(playlist_url, headers=headers)
        playlist_data = response.json()

        playlist = Playlist(**playlist_data)
        track_urls = [item.track.external_urls.spotify for item in playlist.items]
        return track_urls

    def _extract_playlist_id(self, playlist_url: str) -> str:
        match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
        if not match:
            raise ValueError("Invalid playlist URL")
        return match.group(1)
