import os
import json

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data

def get_value_from_dict(data_dict, key, default='Not Found'):
    keys = key.split('.')
    value = data_dict

    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default

class PropertiesBuilder:
    def __init__(self):
        self.config_file_path = r"C:\Users\Matthieu\.spotdl\config.json"  # Updated to JSON file
        self.settings_dict = read_json_file(self.config_file_path)
        self.client_id = get_value_from_dict(self.settings_dict, "client_id")
        self.client_secret = get_value_from_dict(self.settings_dict, "client_secret")
        self.redirect_uri = "http://localhost:8800/"
        self.playlist_liked_songs = get_value_from_dict(self.settings_dict, "playlist_liked_songs")
        self.playlist_liked_albums = get_value_from_dict(self.settings_dict, "playlist_liked_albums")
        self.download_path = get_value_from_dict(self.settings_dict, "download_path")
        self.playlists_to_download = get_value_from_dict(self.settings_dict, "playlists_to_download").split("~")
        self.playlists_m3u = str(get_value_from_dict(self.settings_dict, "playlists_m3u")).split("~")
        self.scope = get_value_from_dict(self.settings_dict, "scope")
        self.app_name = get_value_from_dict(self.settings_dict, "app_name")

if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    print(propertiesBuilder.settings_dict)
    print(propertiesBuilder.client_id)
    print(propertiesBuilder.client_secret)
    print(propertiesBuilder.redirect_uri)
    print(propertiesBuilder.playlist_liked_songs)
    print(propertiesBuilder.playlist_liked_albums)
    print(propertiesBuilder.download_path)
    print(propertiesBuilder.playlists_to_download)
    print(propertiesBuilder.playlists_m3u)
    print(propertiesBuilder.scope)
    print(propertiesBuilder.app_name)
