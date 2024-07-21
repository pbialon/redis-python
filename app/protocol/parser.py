import re
from typing import List


CRLF = "\r\n"


class ParsingError(Exception):
    pass


class Encoder:
    @classmethod
    def encode(cls, data):
        pass


class Decoder:
    @classmethod
    def decode(cls, data):
        pass


class RESP(Encoder, Decoder):
    FIRST_BYTE = None


class Array(RESP):
    FIRST_BYTE = "*"

    @classmethod
    def encode(cls, data: List):
        if len(data) == 0:
            return f"{cls.FIRST_BYTE}0{CRLF}"

        length = len(data)
        encoded_data = f"{cls.FIRST_BYTE}{length}{CRLF}"

        for item in data:
            encoder = cls._get_encoder(item)
            encoded_data += encoder.encode(item)

        return encoded_data

    @classmethod
    def decode(cls, data):
        if not data.startswith(cls.FIRST_BYTE):
            raise ParsingError(f"No {cls.FIRST_BYTE} at the beginning")

        array_elements_starting_position = data.find(CRLF) + len(CRLF)

        full_array = []
        array_elements = cls._split_array_elements(
            data[array_elements_starting_position:]
        )

        for element in array_elements:
            if not element:
                continue
            decoder = DecoderManager.get_decoder(element)
            decoded_object = decoder.decode(element)
            full_array.append(decoded_object)

        return full_array

    @classmethod
    def _split_array_elements(cls, data):
        first_bytes = "".join(DecoderManager.all_first_bytes())
        first_bytes_regex = f"(?=[{first_bytes}])"
        array_elements = re.split(first_bytes_regex, data)
        return array_elements

    @classmethod
    def _get_encoder(cls, data_to_encode):
        if isinstance(data_to_encode, str):
            return BulkString
        if isinstance(data_to_encode, list):
            return Array


class BulkString(RESP):
    FIRST_BYTE = "$"

    @classmethod
    def encode(cls, data):
        if data is None:
            return f"{cls.FIRST_BYTE}-1{CRLF}"
        return f"{cls.FIRST_BYTE}{len(data)}{CRLF}{data}{CRLF}"

    @classmethod
    def decode(self, data):
        length, data = self._parse(data)
        return data

    @classmethod
    def _parse(cls, data):
        if not data.startswith(cls.FIRST_BYTE):
            raise ParsingError(f"No {cls.FIRST_BYTE} at the beginning")

        if data == f"{cls.FIRST_BYTE}-1{CRLF}":
            return 0, None

        parts = data.split(CRLF)
        if len(parts) != 3:
            raise ParsingError("Invalid number of \\r\\n symbols")

        length, data, _ = parts

        try:
            length = int(length[1:])
        except ValueError:
            raise ParsingError("Invalid length format")

        if len(data) != int(length):
            raise ParsingError("Length does not match data length")

        return length, data


class DecoderManager:
    ALL_FIRST_BYTES = {BulkString.FIRST_BYTE, Array.FIRST_BYTE}
    FIRST_BYTES_TO_RESP = {BulkString.FIRST_BYTE: BulkString, Array.FIRST_BYTE: Array}

    @classmethod
    def decode(cls, data):
        resp = cls.get_decoder(data)
        if resp is None:
            raise ParsingError(f"Invalid first byte {cls._first_byte(data)}")
        return resp.decode(data)

    @classmethod
    def get_decoder(cls, data):
        first_byte = cls._first_byte(data)
        return cls.FIRST_BYTES_TO_RESP.get(first_byte)

    @classmethod
    def all_first_bytes(cls):
        return cls.ALL_FIRST_BYTES

    @classmethod
    def _first_byte(cls, data):
        return data[0]


class EncoderManager:

    @classmethod
    def encode(cls, data):
        if isinstance(data, str):
            return BulkString.encode(data)
        if isinstance(data, list):
            return Array.encode(data)
