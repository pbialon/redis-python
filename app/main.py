import socket
import sys
import threading
from .parser import DecoderManager
from .commands import CommandHandler
from .store import Store

def handle_connection(conn, addr, store):
    print(f"Connection from {addr} in thread {threading.current_thread().name}")
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
    print("Logs from your program will appear here!")

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
    args = sys.argv[2:]
    if len(args) == 0:
        return 6379
    if args[0] == "--port":
        return int(args[1])
    return 6379


if __name__ == "__main__":
    main()
