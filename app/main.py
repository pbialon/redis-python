import signal
import socket
import sys
import threading
import argparse

from app.store.kv_store import KVStore
from app.store.metadata_store import MetadataStore
from .protocol.parser import DecoderManager
from .commands.handler import CommandHandler
from app.server import Server


def signal_handler(sig, frame):
    print("\nServer is shutting down...")
    sys.exit(0)


def create_server(role):
    kv_store = KVStore()
    metadata_store = MetadataStore(role)
    command_handler = CommandHandler(kv_store, metadata_store)

    return Server(command_handler, DecoderManager)


def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple Redis-like server")
    parser.add_argument("--host", type=str, default="localhost", help="Host to listen on")
    parser.add_argument("--port", type=int, default=6379, help="Port to listen on")
    parser.add_argument("--replicaof", type=str, help="Replicate another server")
    return parser.parse_args()


def get_role(args):
    if args.replicaof is None:
        return "master"
    return "slave"


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = parse_arguments()
    role = get_role(args)

    server = create_server(role)

    server.start(args.host, args.port)
    server.accept_connections()


if __name__ == "__main__":
    main()
