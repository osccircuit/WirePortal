import os

class ConfModel:
    
    def __init__(self):
        self.path = '/etc/wireguard'
        self.confs = self.detect_confs()

    def detect_confs(self):
        return os.listdir(self.path)

    def get_preety_confs(self):
        return self.confs

    def get_full_path_confs(self):
        return list(map(lambda x: f'{self.path}/{x}', self.confs))