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


def get_value_from_dict(data_dict, key):
    keys = key.split('.')
    value = data_dict

    try:
        for k in keys:
            value = value[k]
        return value
    except KeyError:
        return None


class PropertiesBuilder:

    def __init__(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.config_file_path = os.path.join(my_path, "..\config\settings.yaml")
        self.settings_dict = read_yaml_file(self.config_file_path)
        self.client_id = get_value_from_dict(self.settings_dict, "client_id")
        self.client_secret = get_value_from_dict(self.settings_dict, "client_secret")
        self.redirect_uri = get_value_from_dict(self.settings_dict, "redirect_uri")
        self.scope = get_value_from_dict(self.settings_dict, "scope")


if __name__ == "__main__":
    propertiesBuilder = PropertiesBuilder()
    print(propertiesBuilder.settings_dict)
