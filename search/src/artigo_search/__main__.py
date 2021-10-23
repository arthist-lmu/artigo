import sys
import json
import logging
import argparse
import faulthandler

from artigo_search.client import Client
from artigo_search.server import Server

faulthandler.enable()
PYTHONFAULTHANDLER = 1


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config')

    parser.add_argument('--host')
    parser.add_argument('--port', type=int)

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    parser.add_argument('-m', '--mode', choices=['client', 'server'])

    parser.add_argument('--task', choices=[
        'get', 'insert', 'delete', 'search'
    ])

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
        format='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%d-%m-%Y %H:%M:%S', level=level
    )

    if args.config is not None:
        config = read_config(args.config)
    else:
        config = {}

    if args.mode == 'client':
        if args.host is not None:
            config['host'] = args.host

        if args.port is not None:
            config['port'] = args.port

        client = Client(config)

        if args.task == 'get':
            query = json.loads(args.query)
            client.get(query)
        elif args.task == 'insert':
            client.insert()
        elif args.task == 'delete':
            query = json.loads(args.query)
            client.delete(query)
        elif args.task == 'search':
            query = json.loads(args.query)
            client.search(query)
    elif args.mode == 'server':
        server = Server(config)
        server.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
