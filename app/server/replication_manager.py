

import socket


class ReplicationManager:
    def __init__(self, encoder, decoder, master_host, master_port):
        self._encoder = encoder
        self._decoder = decoder
        self._master_host = master_host
        self._master_port = master_port
        
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master_socket.connect((self._master_host, int(self._master_port)))

        
    def handshake(self):
        self._master_socket.connect((self._master_host, int(self._master_port)))

        self._send(['PING'])
        # response = self._receive()
        # response should be PONG
        
        self._send(['REPLCONF', 'listening-port', self._master_port])
        self._send(['REPLCONF', 'capa', 'psync2'])
        
    def _send(self, message):
        message_encoded_in_redis_protocol = self._encoder.encode(message)
        self._master_socket.send(message_encoded_in_redis_protocol.encode())
    
    def _receive(self):
        received = self._master_socket.recv(1024)
        if not received:
            return None

        message = self.received.decode()
        self._decoder.decode(message)