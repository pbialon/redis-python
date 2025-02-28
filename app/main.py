import signal
import sys
import argparse

from app.server.server_info import ServerInfo
from app.store.kv_store import KVStore
from app.store.metadata_store import MetadataStore
from app.protocol.parser import DecoderManager, EncoderManager
from app.commands.handler import CommandHandler
from app.server.server import Server


def signal_handler(sig, frame):
    print("\nServer is shutting down...")
    sys.exit(0)


def create_server(role):
    kv_store = KVStore()
    metadata_store = MetadataStore(role)
    command_handler = CommandHandler(kv_store, metadata_store)

    return Server(command_handler, metadata_store, DecoderManager, EncoderManager)


def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple Redis-like server")
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host to listen on"
    )
    parser.add_argument("--port", type=int, default=6379, help="Port to listen on")
    parser.add_argument("--replicaof", type=str, help="Replicate another server")
    return parser.parse_args()


def get_role(args):
    if args.replicaof is None:
        return "master"
    return "slave"


def get_replica_of(replicaof):
    if replicaof is None:
        return None

    host, port = replicaof.split(" ")
    return ServerInfo(host, int(port))


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = parse_arguments()
    role = get_role(args)

    server = create_server(role)

    server_info = ServerInfo(args.host, args.port)
    replica_of = get_replica_of(args.replicaof)
    server.start(server_info, replica_of)
    server.accept_connections()


if __name__ == "__main__":
    main()
