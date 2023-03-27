import sys
import json
import environ
import logging
import argparse
import faulthandler

from .client import Client
from .server import Server

faulthandler.enable()
PYTHONFAULTHANDLER = 1

env = environ.Env(
    GRPC_HOST=(str, 'localhost'),
    GRPC_PORT=(int, 50051),
    OPENSEARCH_HOST=(str, 'opensearch'),
    OPENSEARCH_PORT=(int, 9200),
    OPENSEARCH_INDEX=(str, 'artigo'),
)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config')

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    parser.add_argument('-m', '--mode', choices=['client', 'server'])
    parser.add_argument('--task', choices=['get', 'insert', 'delete'])

    parser.add_argument('--query')
    
    return parser.parse_args()


def read_config(file_path):
    with open(file_path, 'r') as file_obj:
        return json.load(file_obj)

    return {}


def main():
    args = parse_args()

    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.ERROR

    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s', 
        datefmt='%Y-%m-%dT%H:%M:%S',
        level=level
    )

    if args.config is not None:
        config = read_config(args.config)
    else:
        config = {}

    config['grpc'] = {
        'host': env('GRPC_HOST'),
        'port': env('GRPC_PORT'),
    }

    config['opensearch'] = {
        'host': env('OPENSEARCH_HOST'),
        'port': env('OPENSEARCH_PORT'),
        'index': env('OPENSEARCH_INDEX'),
    }

    if args.mode == 'client':
        client = Client(config)

        if args.task == 'get':
            query = json.loads(args.query)
            client.get(query)
        elif args.task == 'insert':
            client.insert()
        elif args.task == 'delete':
            client.delete()
    elif args.mode == 'server':
        server = Server(config)
        server.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
