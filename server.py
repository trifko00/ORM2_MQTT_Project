
import socket
import json
from discovery_message import DiscoveryMessage


class Server():
    def __init__(self):
        self.connection = None

    def run(self):
        self.init_socket()
        self._read_stream()

    def init_socket(self):
        """Initialize the communication socket server.
        """
        self.port = 45000
        self.serverIp = '0.0.0.0'

        self.server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )
        self.server_socket.bind((self.serverIp, self.port))
        # self.server_socket.settimeout(1)

    def _read_stream(self):
        while True:
            try:
                bts, addr = self.server_socket.recvfrom(1024)

                msg = bts.decode()
                discovery_message = DiscoveryMessage(json.loads(msg))
                print(discovery_message)
            except BaseException:
                self.server_socket.close()
                pass


if __name__ == "__main__":
    s = Server()
    s.run()
