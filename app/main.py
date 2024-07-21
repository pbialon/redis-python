import signal
import socket
import sys
import threading
from .parser import DecoderManager
from .commands import CommandHandler
from .store import Store


def signal_handler(sig, frame):
    print('\nServer is shutting down...')
    sys.exit(0)

def handle_connection(conn, addr, store):
    with conn:
        disconneted = False
        while not disconneted:
            received = conn.recv(1024)
            if not received:
                disconneted = True
                break
            
            data = received.decode()
            command = DecoderManager.decode(data)
            response = CommandHandler.response(store, command)
            
            conn.sendall(response.encode())

def main():
    signal.signal(signal.SIGINT, signal_handler)

    server_socket = socket.create_server(("localhost", port()), reuse_port=True)
    
    store = Store()

    threads = []
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr, store))
        threads.append(thread)
        thread.start()
    
    # for thread in threads:
    #     thread.join()

def port():
    args = sys.argv[1:]
    if len(args) == 0:
        return 6379
    if args[0] == "--port":
        return int(args[1])
    return 6379


if __name__ == "__main__":
    main()
