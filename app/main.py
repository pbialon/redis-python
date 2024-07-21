import signal
import socket
import sys
import threading
import argparse

from app.store.kv_store import KVStore
from app.store.metadata_store import MetadataStore
from .protocol.parser import DecoderManager
from .commands.handler import CommandHandler


def signal_handler(sig, frame):
    print("\nServer is shutting down...")
    sys.exit(0)


def handle_connection(conn, addr, kv_store, metadata_store):
    handler = CommandHandler(kv_store, metadata_store)
    with conn:
        disconneted = False
        while not disconneted:
            received = conn.recv(1024)
            if not received:
                disconneted = True
                break

            data = received.decode()
            command = DecoderManager.decode(data)
            response = handler.response(command)

            conn.sendall(response.encode())


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = parse_arguments()

    server_socket = socket.create_server(("localhost", args.port), reuse_port=True)

    role = get_role(args)
    kv_store = KVStore()
    metadata_store = MetadataStore(role, '')

    threads = []
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr, kv_store, metadata_store))
        threads.append(thread)
        thread.start()

    # for thread in threads:
    #     thread.join()



def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple Redis-like server")
    parser.add_argument("--port", type=int, default=6379, help="Port to listen on")
    parser.add_argument("--replicaof", type=str, help="Replicate another server")
    return parser.parse_args()


def get_role(args):
    if args.replicaof is None:
        return "master"
    return "slave"


if __name__ == "__main__":
    main()
