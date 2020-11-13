from abc import ABC, abstractmethod
from typing import Optional
import socketserver


class ROARServer(ABC):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server: Optional[socketserver.UDPServer] = None

    @abstractmethod
    def run(self):
        pass
