import pytest
from click.testing import CliRunner
from shuffler.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SPOTIPY_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("SPOTIPY_CLIENT_SECRET", "test_client_secret")


def test_list_playlist_urls(runner, mock_env_vars, mocker):
    # mock the Spotify class
    mock_spotify = mocker.patch("shuffler.modules.spotify.Spotify")
    mock_spotify_instance = mock_spotify.return_value
    mock_spotify_instance.list_playlist_urls.return_value = [
        "https://open.spotify.com/track/testtrack1",
        "https://open.spotify.com/track/testtrack2",
    ]

    result = runner.invoke(
        cli,
        [
            "list-urls",
            "https://open.spotify.com/playlist/test_playlist_id?si=2483b4d013b442ca",
        ],
    )

    assert result.exit_code == 0
    assert "https://open.spotify.com/track/testtrack1" in result.output
    assert "https://open.spotify.com/track/testtrack2" in result.output
