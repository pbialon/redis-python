import socket
import threading

PONG = b"+PONG\r\n"

def handle_connection(conn, addr):
    print(f"Connection from {addr} in thread {threading.current_thread().name}")
    with conn:
        disconneted = False
        while not disconneted:
            received = conn.recv(1024)
            if not received:
                disconneted = True
                break
            conn.sendall(PONG)

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    threads = []
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        threads.append(thread)
        thread.start()
    
    # for thread in threads:
    #     thread.join()


if __name__ == "__main__":
    main()
