import subprocess

from synfy.models.PropertiesBuilder import PropertiesBuilder
from synfy.models.SpotifyDataAccess import SpotifyDataAccess


class SpotDlWrapper:
    def __init__(self, propertiesBuilder, spotifyDataAccess):
        self.client_id = propertiesBuilder.client_id
        self.client_secret = propertiesBuilder.client_secret
        self.spotifyDataAccess = spotifyDataAccess

    def download_playlist(self, playlist_url, output_path, filename="\{year}\{artists} - {title}", generate_m3u=False):
        try:
            spotdl_command = "spotdl"
            args = [spotdl_command, "--playlist", playlist_url, "--output", output_path + filename]
            subprocess.run(args, check=True)
            print("Playlist downloaded successfully.")
            if bool(generate_m3u):
                playlist_name = self.spotifyDataAccess.get_playlist_name(playlist_url)
                args = [spotdl_command, playlist_url, "--m3u", playlist_name]
                subprocess.run(args, cwd=output_path, check=True)
                print("Playlist created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading the playlist: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    spotifyDataAccess = SpotifyDataAccess(propertiesBuilder)
    spotDlWrapper = SpotDlWrapper(propertiesBuilder, spotifyDataAccess)
    spotDlWrapper.download_playlist("https://open.spotify.com/playlist/7uke38Rvg8HpYLbzxc1rog?si=ba12e579fc7e4f29",
                                    r"C:\Users\Matthieu\Downloads\Music")
