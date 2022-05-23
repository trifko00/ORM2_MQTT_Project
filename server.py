from threading import Thread
import socket
import json
from discovery_message import DiscoveryMessage
import time


class Server():
    def __init__(self):
        self.connection = None
        self.harvesters = []
        self.threads = []
        self.ip = self.get_ip()
        self.alive = {'alive': True, 'ip': self.ip}
        self.threads = []
        self.threads.append(Thread(
            target=self._broadcast_alive, args=(), daemon=True))

    def run(self):
        self._init_socket()
        self.threads[0].start()
        self._read_stream()

    def _init_socket(self):
        """Initialize the communication socket server.
        """
        self.port = 45000
        self.serverIp = '0.0.0.0'
        # self.broadcast = '192.168.252.255'

        self.server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.bind((self.serverIp, self.port))
        # self.server_socket.settimeout(1)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception as e:
            print(e)
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def _broadcast_alive(self):
        bits = self.ip.split('.')
        addr_bit = bits[0] + '.' + bits[1] + '.' + bits[2] + '.'
        allips = [addr_bit + str(i) for i in range(0, 255)]
        while True:
            for ip in allips:
                try:
                    # print(ip)
                    self.server_socket.sendto(json.dumps(self.alive).encode(),
                                              (ip, self.port))
                    time.sleep(0.1)
                except BaseException:
                    time.sleep(0.1)
                    pass
                # print(self.alive)

    def _read_stream(self):
        while True:
            try:
                bts, addr = self.server_socket.recvfrom(1024)

                msg = bts.decode()
                discovery_message = DiscoveryMessage(json.loads(msg))
                print(discovery_message)
                # detach thread to work with the new harvesters
                self.harvesters.append(discovery_message)

            except BaseException:
                self.server_socket.close()
                pass


if __name__ == "__main__":
    s = Server()
    s.run()
