import socket
from yarcon.logger import Logger
from yarcon.packet import Packet, PacketType


class Connection:
    def __init__(self, addr: str, port=25575, timeout=5, debug=False):
        self.addr = addr
        self.port = port

        self.__logger = Logger(debug_enabled=debug)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(timeout)

    def __enter__(self):
        self.__socket.connect((self.addr, self.port))
        self.__logger.debug(f"connected to {self.addr}:{self.port}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__socket.close()
        self.__logger.debug("connection has been closed successfully")

    def login(self, password: str) -> bool:
        packet = Packet(type=PacketType.SERVERDATA_AUTH, body=password)
        self.__logger.debug(f"login attempt has started: {packet}")

        self.__send(packet)
        response = self.__get_response()

        self.__logger.debug(f"login response: {response}")

        return False if response.id != packet.id else True

    def command(self, command: str) -> str | None:
        packet = Packet(body=command, type=PacketType.SERVERDATA_EXECCOMMAND)

        self.__send(packet)
        response = self.__get_response()

        return None if response is None else response.body

    def __get_response(self) -> Packet | None:
        size = int.from_bytes(self.__receive(4), byteorder="little")

        if size == 0:
            return None

        packet_data = self.__receive(size)
        return Packet.from_bytes(packet_data)

    def __send(self, packet: Packet):
        buff = packet.to_bytes()

        self.__logger.debug(f"sending buff: {buff}")
        self.__logger.debug(f"sending packet: {packet}")

        self.__socket.sendall(buff)

    def __receive(self, length: int) -> bytes:
        data = self.__socket.recv(length)

        if len(data) < length:
            raise Exception(f"receive length missmatch, requested {length}, got {len(data)}")

        return data
