import os
import click
from dotenv import load_dotenv
from shuffler.modules import spotify


@click.group()
def cli():
    pass


@cli.command()
@click.argument("playlist_url")
def list_urls(playlist_url: str):
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    spotify_client = spotify.Spotify(client_id, client_secret)
    track_urls = spotify_client.list_playlist_urls(playlist_url)
    for url in track_urls:
        click.echo(url)


if __name__ == "__main__":
    cli()
