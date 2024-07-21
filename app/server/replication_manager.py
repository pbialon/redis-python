import socket


class ReplicationManager:
    def __init__(self, encoder, decoder):
        self._encoder = encoder
        self._decoder = decoder

    def start(self, master_info):
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master_socket.connect((master_info.host, master_info.port))

    def handshake(self, self_info):
        self._send(["PING"])
        self._receive()

        self._send(["REPLCONF", "listening-port", f"{self_info.port}"])
        self._receive()

        self._send(["REPLCONF", "capa", "psync2"])
        self._receive()
        
        self._send(["PSYNC", "?", "-1"])
        self._receive()

    def _send(self, message):
        message_encoded_in_redis_protocol = self._encoder.encode(message)
        self._master_socket.send(message_encoded_in_redis_protocol.encode())

    def _receive(self):
        received = self._master_socket.recv(1024)
        if not received:
            return None

        message = received.decode()
        self._decoder.decode(message)
