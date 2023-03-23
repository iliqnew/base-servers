import socket
import pickle
import threading
from typing import Literal, Tuple

from base import BaseServer


class InvalidIPv4Address(Exception):
    def __init__(self, ip, *args: object) -> None:
        __args = args if args else (f"'{ip}' is an invalid IP version 4 address",)
        super().__init__(*__args)

class Gameplay:
    def start(self):
        ...

class EventHandler:
    def __init__(self, gameplay: Gameplay, server: BaseServer) -> None:
        self.gameplay = gameplay
        self.server = server
    
    def handle(self):
        ...

class BaseTCPServer(BaseServer):
    addr: Tuple[str, int] = ("localhost", 5000)
    buffer: int = 1024
    ipv: Literal[4, 6] = 4
    max_connections: int = 1
    gameplay: Gameplay = Gameplay()
    # event_handler: EventHandler = EventHandler()

    clients = []

    def __init__(self) -> None:
        self.__address_family = self.set_address_family(self.ipv)
        self.__socket = socket.socket(self.__address_family, socket.SOCK_STREAM) 
        self.__socket.bind(self.addr)
    
    def run(self):
        self.__listen()
        threading.Thread(target=self.gameplay.start).start()

    def __listen(self):
        self.__socket.listen(self.max_connections)
        threading.Thread(target=self.__accept).start()
    
    def __accept(self):
        while True:
            conn, addr = self.__socket.accept()
            print(f"Connection from '{addr}'")
            encoded_client = conn.recv(self.buffer)
            if not encoded_client:
                continue
            print(f"Received: {encoded_client}")
            client = pickle.loads(encoded_client)
            client_dict = {
                "client": client,
                "connection": conn,
                "address": addr
            }
            self.__handle_client(client_dict)

    def __handle_client(self, client_dict):
        self.clients.append(client_dict)
        pass


if __name__=="__main__":
    server = BaseTCPServer()
    server.run()