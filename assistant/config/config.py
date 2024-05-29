import configparser


class Config:
    """Config class for Assistant."""

    def __init__(self):
        self.config_file_path = "config/config.ini"
        self.gmail_config_bath_path = "config"
        self.fs_path = "fs"

        self.load_config_file()

    def load_config_file(self):
        """Load the config file."""
        if self.config_file_path is None:
            return None
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        for key, value in config.items("assistant"):
            setattr(self, key.lower(), value)
