from synfy.models.AppDataHandler import AppDataHandler
from synfy.models.PropertiesBuilder import PropertiesBuilder
from synfy.models.SpotDlWrapper import SpotDlWrapper
from synfy.models.SpotifyDataAccess import SpotifyDataAccess


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m synfy` and `$ synfy `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    propertiesBuilder = PropertiesBuilder()
    appDataHandler = AppDataHandler(propertiesBuilder)
    spotDlWrapper = SpotDlWrapper(propertiesBuilder)
    spotifyDataAccess = SpotifyDataAccess(propertiesBuilder)
    spotifyDataAccess.create_playlist_from_uri_list(spotifyDataAccess.get_liked_songs(), propertiesBuilder.playlist_liked_songs)
    spotifyDataAccess.create_playlist_from_uri_list(spotifyDataAccess.get_liked_albums(), propertiesBuilder.playlist_liked_albums)
    print(propertiesBuilder.playlists_to_download)
    for playlist_name, playlists_config in zip(propertiesBuilder.playlists_to_download, propertiesBuilder.playlists_config):
        spotDlWrapper.download_playlist(spotifyDataAccess.get_playlist_link(playlist_name), propertiesBuilder.download_path + "\\" + playlist_name, playlists_config)
    print("This will do something")
