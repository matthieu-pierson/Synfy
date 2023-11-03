import json
import os
import subprocess


class ConfigManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        print(os.path.isfile(self.json_file_path))
        print(not os.path.isfile(self.json_file_path))
        if not os.path.isfile(self.json_file_path):
            args = ["spotdl", "--generate-config"]
            try:
                subprocess.run(args, input='y\n', text=True, shell=True)
                print("Config file successfully initialized.\n")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        download_path = r"O:\Music"
        self.add_value("download_path", download_path)
        client_id = "2b7a812c80f34c3b8b37f7b1d46f2f46"
        client_secret = "2ff7254969d842f3855701e7960b7493"
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8800/"
        self.add_value("client_id", client_id)
        self.add_value("client_secret", client_secret)
        self.add_value("output", download_path + r"\{year}\{artists} - {title}.{output-ext}")
        self.add_value("cookie_file", r"C:\Users\Matthieu\.spotdl\music.youtube.com_cookies.txt")
        self.add_value("format", "mp3")
        self.add_value("bitrate", "0")
        self.add_value("threads", 8)
        self.add_value("playlists_to_download", "Liked Songs~Liked Albums~Mix 1")
        self.add_value("playlists_m3u", "True~True~True")
        self.add_value("scope", "user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative user-follow-read user-read-playback-state user-modify-playback-state user-read-private user-read-email")
        self.add_value("playlist_liked_songs", "Liked Songs")
        self.add_value("playlist_liked_albums", "Liked Albums")
        self.add_value("app_name", "Synfy")

    def add_value(self, key, value):
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)

            data[key] = value  # Overwrite the key if it exists or create it if it doesn't.

            with open(self.json_file_path, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"Updated {key}: {value} in {self.json_file_path}")

        except FileNotFoundError:
            print(f"File not found: {self.json_file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
