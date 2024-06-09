import socket

PONG = b"+PONG\r\n"

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn, addr = server_socket.accept()
    print("Connection from: ", addr)
    conn.sendall(PONG)


if __name__ == "__main__":
    main()
