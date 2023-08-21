import json


class ConfigManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.add_value("download_path", r"C:\Users\Matthieu\Music")
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
            if key not in data:
                data[key] = value
                with open(self.json_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                    print(f"Added {key}: {value} to {self.json_file_path}")
            else:
                print(f"The key {key} already exists in {self.json_file_path}")
        except FileNotFoundError:
            print(f"File not found: {self.json_file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
