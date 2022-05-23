
import socket
import time
from discovery_message import DiscoveryMessage


class Client():
    def __init__(self):
        self.connection = None

    def run(self):
        self.init_socket()
        self._streams()

    def init_socket(self):
        """Initialize the socket client.
        """

        self.serverIp = '192.168.252.22'   # PC ip
        self.port = 45000            # com port
        self.client_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )

    def _streams(self):
        discovery_message = {}
        while True:
            try:
                # discovery_message['Type'] = "SENZOR"
                # discovery_message['ID'] = 5
                # discovery_message['value'] = 24
                discovery_message = DiscoveryMessage().toJSON()
                # print(discovery_message)
                data = discovery_message.encode()
                self.client_socket.sendto(data, (self.serverIp, self.port))
                time.sleep(1)

            except Exception as e:
                # Reinitialize the socket for reconnecting to client.
                print(e)
                self.connection = None
                self.init_socket()
                pass


if __name__ == "__main__":
    c = Client()
    c.run()
