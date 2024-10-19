import os
import yaml


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.config = {}
        self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../', 'config.yaml')
        with open(config_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_nested(self, *keys, default=None):
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value
