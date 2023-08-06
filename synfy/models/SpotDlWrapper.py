import subprocess

from synfy.models.PropertiesBuilder import PropertiesBuilder


class SpotDlWrapper:
    def __init__(self, propertiesBuilder):
        self.client_id = propertiesBuilder.client_id
        self.client_secret = propertiesBuilder.client_secret

    def download_playlist(self, playlist_url, output_path, filename="\{year}\{artists} - {title}", generate_m3u=False):
        try:
            spotdl_command = "spotdl"
            args = [spotdl_command, "--playlist", playlist_url, "--output", output_path + filename]
            subprocess.run(args, check=True)
            print("Playlist downloaded successfully.")
            if generate_m3u:
                args = [spotdl_command, "--playlist", playlist_url, "--m3u", "--output", output_path]
                subprocess.run(args, check=True)
                print("Playlist created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading the playlist: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    spotDlWrapper = SpotDlWrapper(propertiesBuilder)
    spotDlWrapper.download_playlist("https://open.spotify.com/playlist/7uke38Rvg8HpYLbzxc1rog?si=ba12e579fc7e4f29",
                                    r"C:\Users\Matthieu\Downloads\Music")
