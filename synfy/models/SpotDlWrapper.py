import subprocess

from synfy.models.PropertiesBuilder import PropertiesBuilder
from synfy.models.SpotifyDataAccess import SpotifyDataAccess


class SpotDlWrapper:
    def __init__(self, propertiesBuilder, spotifyDataAccess):
        self.client_id = propertiesBuilder.client_id
        self.client_secret = propertiesBuilder.client_secret
        self.spotifyDataAccess = spotifyDataAccess
        self.init_default_config()
        self.download_ffmpeg()

    def _run_spotdl_command(self, args, message_success):
        try:
            subprocess.run(args, input='y\n', text=True, shell=True)
            print(message_success)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def init_default_config(self):
        args = ["spotdl", "--generate-config"]
        self._run_spotdl_command(args, "Config file successfully initialized.\n")

    def download_ffmpeg(self):
        args = ["spotdl", "--download-ffmpeg"]
        self._run_spotdl_command(args, "FFmpeg successfully downloaded.\n")

    def download_playlist(self, playlist_url, output_path, generate_m3u=False):
        try:
            spotdl_command = "spotdl"
            if bool(generate_m3u):
                playlist_name = self.spotifyDataAccess.get_playlist_name(playlist_url)
                args = [spotdl_command, playlist_url, "--m3u", playlist_name]
                subprocess.run(args, cwd=output_path, check=True)
                print("Playlist downloaded successfully - m3u file created.\n")
            else:
                args = [spotdl_command, "--playlist", playlist_url]
                subprocess.run(args, check=True)
                print("Playlist downloaded successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading the playlist: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    spotifyDataAccess = SpotifyDataAccess(propertiesBuilder)
    spotDlWrapper = SpotDlWrapper(propertiesBuilder, spotifyDataAccess)
    # spotDlWrapper.download_playlist("https://open.spotify.com/playlist/7uke38Rvg8HpYLbzxc1rog?si=ba12e579fc7e4f29",
    #                                 r"C:\Users\Matthieu\Downloads\Music")
    spotDlWrapper.init_default_config()
    spotDlWrapper.download_ffmpeg()
