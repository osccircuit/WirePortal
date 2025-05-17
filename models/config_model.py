import os
import subprocess

class ConfigModel:
    
    def __init__(self):
        self.path = '/etc/wireguard'
        self.configs = self.detect_configs()
        self.current_use_config = None

    def detect_configs(self):
        return list(map(lambda file: file.removesuffix('.conf'),
                        os.listdir(self.path)))

    def run_connect_command(self, config_file):
        result = subprocess.run(
            ['pkexec', 'ls', '/home/osc_circuit/Documents/CodeProjects'],
            # check=True,
            stderr=subprocess.DEVNULL,  # Полное игнорирование stderr
            stdout=subprocess.PIPE,     # Если нужно перехватить stdout
            # capture_output=True,
            text=True
        )
        # print(result.stdout)
        self.current_use_config = config_file
        response = {'status': 'connect',
                    'message': f'Connection has been created by {config_file}'}
        return response

    def run_disconnect_command(self):
        response = {'status': 'disconnect',
                    'message': 'Connection has been closed by ' \
                               f'{self.current_use_config}',
                   }
        self.current_use_config = None
        return response

    def get_preety_configs(self):
        return self.configs

    def get_full_path_configs(self):
        return list(map(lambda x: f'{self.path}/{x}', self.configs))
