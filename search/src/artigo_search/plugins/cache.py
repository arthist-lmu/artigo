import os
import pickle
import logging

from multiprocessing import Lock

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache_dir, mode='a'):
        self.cache_dir = cache_dir

        os.makedirs(self.cache_dir, exist_ok=True)

        self.cache_data = {}
        self.length = 4096

        self.num_client = 0
        self.mutex = Lock()
        self.dirty = False
        self.mode = mode

    def __enter__(self):
        with self.mutex:
            if self.num_client == 0:
                if os.path.exists(os.path.join(self.cache_dir, 'data.pkl')):
                    with open(os.path.join(self.cache_dir, 'data.pkl'), 'rb') as file_obj:
                        self.cache_data = pickle.load(file_obj)

            self.num_client += 1

        return self

    def __exit__(self, type, value, tb):
        if self.mode == 'r':
            return

        with self.mutex:
            if self.num_client == 1 and self.dirty:
                with open(os.path.join(self.cache_dir, 'data.pkl'), 'wb') as file_obj:
                    pickle.dump(self.cache_data, file_obj)

            self.num_client -= 1

    def __getitem__(self, id):
        data_dict = {'id': id}

        return data_dict

    def write(self, entry):
        if self.mode == 'r':
            return

        with self.mutex:
            self.dirty = True
            id = entry['id']
