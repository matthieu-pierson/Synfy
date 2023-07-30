import os
import platform


class AppDataHandler:
    def __init__(self, propertiesBuilder):
        self.app_name = propertiesBuilder.app_name
        self.appdata_folder = self.get_appdata_folder()

    def get_appdata_folder(self):
        system = platform.system()
        if system == 'Windows':
            appdata_folder = os.path.join(os.getenv('APPDATA'), self.app_name)
        elif system == 'Linux':
            appdata_folder = os.path.join(os.path.expanduser('~'), '.config', self.app_name)
        elif system == 'Darwin':
            appdata_folder = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', self.app_name)
        else:
            raise Exception('Unsupported operating system: {}'.format(system))

        os.makedirs(appdata_folder, exist_ok=True)
        return appdata_folder

    def get_file_path(self, filename):
        return os.path.join(self.appdata_folder, filename)
