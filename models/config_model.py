from pathlib import Path

class ConfigModel:
    
    def __init__(self):
        self.path = '/etc/wireguard'
        self.extension = '.conf'
        self.configs = self.detect_configs()
        self.current_use_config = None

    def detect_configs(self):
        files = [str(file.name) \
                 for file in Path(self.path).glob(f'*{self.extension}') \
                 if file.is_file()]
        return list(map(lambda file: file.removesuffix(self.extension),
                        files))

    def get_preety_configs(self):
        return self.configs

    def get_full_path_configs(self):
        return list(map(lambda x: f'{self.path}/{x}', self.configs))
