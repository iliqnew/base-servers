import socket
from typing import Literal

class InvalidAddressFamily(Exception):
    def __init__(self, *args: object) -> None:
        __args = args if args else ("AddressFamily should be either 4 or 6, depending on the desired ip version",)
        super().__init__(*__args)


class BaseServer:
    @staticmethod
    def set_address_family(ipv: Literal[4, 6]) -> socket.AddressFamily:
        if ipv not in (4, 6):
            raise InvalidAddressFamily()
        return socket.AF_INET if ipv == 4 else socket.AF_INET6