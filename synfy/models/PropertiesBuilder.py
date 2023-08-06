import os

import yaml


def read_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        return process_yaml(data)


def process_yaml(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = process_yaml(value)
        return result
    elif isinstance(data, list):
        return [process_yaml(item) for item in data]
    else:
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
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.config_file_path = os.path.join(my_path, "..\config\settings.yaml")
        self.settings_dict = read_yaml_file(self.config_file_path)
        self.client_id = get_value_from_dict(self.settings_dict, "spotify.client_id")
        self.client_secret = get_value_from_dict(self.settings_dict, "spotify.client_secret")
        self.redirect_uri = get_value_from_dict(self.settings_dict, "spotify.redirect_uri")
        self.playlist_liked_songs = get_value_from_dict(self.settings_dict, "spotify.playlist_liked_songs")
        self.playlist_liked_albums = get_value_from_dict(self.settings_dict, "spotify.playlist_liked_albums")
        self.download_path = get_value_from_dict(self.settings_dict, "config.download_path")
        self.playlists_to_download = get_value_from_dict(self.settings_dict, "config.playlists_to_download").split("~")
        self.playlists_config = get_value_from_dict(self.settings_dict, "config.playlists_config").split("~")
        self.scope = get_value_from_dict(self.settings_dict, "spotify.scope")
        self.app_name = get_value_from_dict(self.settings_dict, "app_name")


if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    print(propertiesBuilder.settings_dict)
