from abc import ABC, abstractmethod
from typing import Optional
import socketserver
import socket
import logging

class ROARServer(ABC):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server: Optional[socketserver.UDPServer] = None
        self.socket: Optional[socket.socket] = socket.socket(socket.AF_INET,  # Internet
                                                             socket.SOCK_DGRAM)  # UDP
        self.logger = logging.getLogger("ROAR Server")
    @abstractmethod
    def run(self):
        pass
