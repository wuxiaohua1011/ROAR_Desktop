from abc import ABC, abstractmethod
from typing import Optional
import socketserver
import socket
import logging


class ROARServer(ABC):
    def __init__(self):
        self.socket: Optional[socket.socket] = socket.socket(socket.AF_INET,  # Internet
                                                             socket.SOCK_DGRAM)  # UDP
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.logger = logging.getLogger("Base Server")

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def initialize_socket() -> socket.socket:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.settimeout(3)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass  # Some systems don't support SO_REUSEPORT
        soc.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
        soc.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        return soc