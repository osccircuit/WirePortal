from models.config_model import ConfigModel
from models.connection_model import ConnectionModel
from models.thread_model import ThreadWorker


class Model:
    def __init__(self):
        self.config_model = ConfigModel()
        self.connection_model = ConnectionModel()
        self.thread_worker = ThreadWorker()
