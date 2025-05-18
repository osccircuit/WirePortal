import psutil
import subprocess
from time import sleep


class ConfigSetException(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class ConnectionModel:

    def __init__(self):
        self.config_file = None

        self.general_connection_command = ["pkexec", "wg-quick"]
        self.open_command = "up"
        self.close_command = "down"

    def set_config_file(self, config_file):
        self.config_file = config_file

    def check_config_file(self):
        if self.config_file is None or "":
            raise ConfigSetException("Config file not found")
        return True

    def open_connection(self):
        try:
            self.check_config_file()
            command = self.general_connection_command.copy()
            command.extend(["up", self.config_file])
            result = subprocess.run(
                command,
                stderr=subprocess.DEVNULL,  # Полное игнорирование stderr
                stdout=subprocess.PIPE,  # Если нужно перехватить stdout
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
            command = self.general_connection_command.copy()
            command.extend(["down", self.config_file])
            result = subprocess.run(
                command,
                stderr=subprocess.DEVNULL,  # Полное игнорирование stderr
                stdout=subprocess.PIPE,  # Если нужно перехватить stdout
                text=True,
            )
            response = {
                "status": "disconnect",
                "message": "Connection has been closed by " f"{self.config_file}",
            }
        except ConfigSetException as e:
            response = {"status": "connect", "message": f"{e}"}
        return response

    def speed_check(self):
        net1 = psutil.net_io_counters()
        sleep(1)
        net2 = psutil.net_io_counters()

        bytes_sent = net2.bytes_sent - net1.bytes_sent
        bytes_recv = net2.bytes_recv - net1.bytes_recv

        return [
            f"TX - {bytes_sent / 1024:.2f} KB/s",
            f"RX - {bytes_recv / 1024:.2f} KB/s",
        ]
