import socket
import threading

from app.server.replication_manager import ReplicationManager


class Role:
    MASTER = "master"
    SLAVE = "slave"


class ReplicaOf:
    def __init__(self, host_port_str):
        host, port = host_port_str.split(" ")
        self.host = host
        self.port = int(port)


class Server:
    def __init__(self, command_handler, metadata_store, decoder, encoder):
        self._command_handler = command_handler
        self._metadata_store = metadata_store
        self._decoder = decoder
        self._encoder = encoder

    def start(self, host, port, replicaof):
        self._server_socket = socket.create_server((host, port), reuse_port=True)

        if self._role() == Role.SLAVE:
            replica_of = ReplicaOf(replicaof)
            self._replication_manager = ReplicationManager(self._encoder, self._decoder, replica_of.host, replica_of.port)
            self._replication_manager.start()
            self._replication_manager.handshake()

    def accept_connections(self):
        threads = []
        while True:
            conn, addr = self._server_socket.accept()
            thread = threading.Thread(target=self._handle_connection, args=(conn, addr))
            threads.append(thread)
            thread.start()

    def _handle_connection(self, conn, addr):
        with conn:
            disconneted = False
            while not disconneted:
                received = conn.recv(1024)
                if not received:
                    disconneted = True
                    break

                response = self._prepare_response(received)

                conn.sendall(response)

    def _prepare_response(self, received):
        data = received.decode()
        command = self._decoder.decode(data)
        response = self._command_handler.response(command)
        return response.encode()

    def _role(self):
        return self._metadata_store.role()
