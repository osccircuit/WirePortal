import asyncio
import subprocess

class ConfigSetException(Exception):
    def __init__(self, message=None):
        super().__init__(message)

class ConnectionModel:

    def __init__(self):
        self.config_file = None

    def set_config_file(self, config_file):
        self.config_file = config_file

    def check_config_file(self):
        if self.config_file is None or "":
            raise ConfigSetException('Config file not found')
        return True

    def open_connection(self):
        try:
            self.check_config_file()
            result = subprocess.run(
                ["pkexec", "wg-quick", "up", self.config_file],
                # check=True,
                stderr=subprocess.DEVNULL,  # Полное игнорирование stderr
                stdout=subprocess.PIPE,  # Если нужно перехватить stdout
                # capture_output=True,
                text=True,
            )
            # print(result.stdout)
            response = {
                "status": "connect",
                "message": "Connection has been " f"created by {self.config_file}",
            }
        except ConfigSetException as e:
            response = {"status": "disconnect", "message": f"{e}"}
        return response

    def close_connection(self):
        try:
            self.check_config_file()
            response = {
                "status": "disconnect",
                "message": "Connection has been closed by " f"{self.config_file}",
            }
        except ConfigSetException as e:
            response = {"status": "connect", "message": f"{e}"}
        return response
