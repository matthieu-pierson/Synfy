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
    spotifyDataAccess.create_playlist_from_uri_list(spotifyDataAccess.get_liked_songs(), "Every songs liked")
    spotifyDataAccess.create_playlist_from_uri_list(spotifyDataAccess.get_liked_albums(), "Every albums liked")
    print("This will do something")
