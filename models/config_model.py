import os
import subprocess

class ConfigModel:
    
    def __init__(self):
        self.path = '/etc/wireguard'
        self.configs = self.detect_configs()

    def detect_configs(self):
        return os.listdir(self.path)

    def run_connect_command(self):
        result = subprocess.run(
            ['pkexec', 'ls', '/home/osc_circuit/Documents/CodeProjects'],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)

    def get_preety_configs(self):
        return self.configs

    def get_full_path_configs(self):
        return list(map(lambda x: f'{self.path}/{x}', self.configs))
