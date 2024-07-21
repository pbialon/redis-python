import socket
import threading



class Server:
    def __init__(self, command_handler, decoder):
        self._command_handler = command_handler
        self._decoder = decoder

    def start(self, host, port):
        self._server_socket = socket.create_server((host, port), reuse_port=True)

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

                data = received.decode()
                command = self._decoder.decode(data)
                response = self._command_handler.response(command)

                conn.sendall(response.encode())

    def _role(self):
        return self._metadata_store.role()
