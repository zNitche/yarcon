import random
from enum import Enum


class PacketType(Enum):
    SERVERDATA_RESPONSE_VALUE = 0
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_AUTH = 3


class Packet:
    def __init__(self, type: PacketType, body: str, id: int | None = None):
        self.id = id if id is not None else self.__generate_id()
        self.type = type
        self.body = body

    def __generate_id(self):
        # 32 bit int
        int_max = 2147483647
        return random.randint(1, int_max)

    def __int_to_bytes(self, val: int, length=4):
        return val.to_bytes(length, byteorder="little")

    def to_bytes(self):
        id = self.__int_to_bytes(self.id)
        type = self.__int_to_bytes(self.type.value)
        body = self.body.encode("utf-8") + b"\x00"

        content = id + type + body + b"\x00"
        size = self.__int_to_bytes(len(content))

        return size + content

    @staticmethod
    def from_bytes(buff: bytes):
        id = int.from_bytes(buff[0:4], byteorder="little")
        type = PacketType(int.from_bytes(buff[4:8], byteorder="little"))
        body = buff[8:-2].decode("utf-8")

        return Packet(id=id, type=type, body=body)

    def __str__(self):
        return f"id: {self.id} type: {self.type.value} body: {self.body}"
