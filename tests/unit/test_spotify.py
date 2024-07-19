import pytest
from shuffler.modules.spotify import (
    Spotify,
)


@pytest.fixture
def mock_spotify(mocker):
    client_id = "test_client_id"
    client_secret = "test_client_secret"
    mocker.patch.object(Spotify, "_get_token", return_value="test_access_token")
    spotify = Spotify(client_id, client_secret)

    return spotify


def test_get_access_token(mocker):
    auth_response = {
        "access_token": "test_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
    }

    mocker.patch("requests.post", return_value=mocker.Mock(json=lambda: auth_response))

    client_id = "test_client_id"
    client_secret = "test_client_secret"
    spotify = Spotify(client_id, client_secret)

    access_token = spotify._get_token()

    assert access_token == "test_access_token"


def test_list_playlist_urls(mock_spotify, mocker):
    playlist_data = {
        "items": [
            {
                "track": {
                    "id": "testtrack1",
                    "name": "Test Track",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/testtrack1"
                    },
                }
            },
            {
                "track": {
                    "id": "testtrack2",
                    "name": "Another Test Track",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/testtrack2"
                    },
                }
            },
        ]
    }

    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: playlist_data))

    playlist_url = (
        "https://open.spotify.com/playlist/test_playlist_id?si=2483b4d013b442ca"
    )
    urls = mock_spotify.list_playlist_urls(playlist_url)

    assert urls == [
        "https://open.spotify.com/track/testtrack1",
        "https://open.spotify.com/track/testtrack2",
    ]

    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: playlist_data))

    playlist_url = (
        "https://open.spotify.com/playlist/test_playlist_id?si=2483b4d013b442ca"
    )
    urls = mock_spotify.list_playlist_urls(playlist_url)

    assert urls == [
        "https://open.spotify.com/track/testtrack1",
        "https://open.spotify.com/track/testtrack2",
    ]


def test_extract_playlist_id(mock_spotify):
    playlist_url = (
        "https://open.spotify.com/playlist/6r7wJMd1a9DmfueAHmWVZv?si=2483b4d013b442ca"
    )
    playlist_id = mock_spotify._extract_playlist_id(playlist_url)
    assert playlist_id == "6r7wJMd1a9DmfueAHmWVZv"

    with pytest.raises(ValueError):
        invalid_url = "https://open.spotify.com/invalid/6r7wJMd1a9DmfueAHmWVZv?si=2483b4d013b442ca"
        mock_spotify._extract_playlist_id(invalid_url)
