import os
import subprocess

class ConfModel:
    
    def __init__(self):
        self.path = '/etc/wireguard'
        self.confs = self.detect_confs()

    def detect_confs(self):
        return os.listdir(self.path)

    def run_wg_command(self):
        result = subprocess.run(
            ['pkexec', 'ls', '/home/circuit/code_projects'],
            capture_output=True,
            text=True
        )
        print(result.stdout)

    def get_preety_confs(self):
        return self.confs

    def get_full_path_confs(self):
        return list(map(lambda x: f'{self.path}/{x}', self.confs))