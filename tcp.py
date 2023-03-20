import socket
import pickle
import threading
from typing import Literal

from base import BaseServer


class InvalidIPv4Address(Exception):
    def __init__(self, ip, *args: object) -> None:
        __args = args if args else (f"'{ip}' is an invalid IP version 4 address",)
        super().__init__(*__args)


class BaseTCPServer(BaseServer):
    clients = []

    def __init__(
            self,
            ip_addr: str = "localhost",
            port: int = 5000,
            buffer: int = 1024,
            ipv: Literal[4, 6] = 4,
            max_connections: int = 1
    ) -> None:
        self.__addr = (ip_addr, port)
        self.__buffer = buffer
        self.__address_family = self.set_address_family(ipv)
        self.__socket = socket.socket(self.__address_family, socket.SOCK_STREAM)
        self.__max_connections = max_connections

        self.__setup()
        self.__run()
    
    def __setup(self):
        self.__socket.bind(self.__addr)
    
    def __run(self):
        self.__listen()
        self.__accept()

    def __listen(self):
        self.__socket.listen(self.__max_connections)
        threading.Thread(target=self.__accept).start()
    
    def __accept(self):
        while True:
            conn, addr = self.__socket.accept()
            print(f"Connection from '{addr}'")
            encoded_client = conn.recv(self.__buffer)
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