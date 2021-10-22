# ARTigo Search


## Miscellaneous

### Compile Protocol buffers
```sh
python3 -m grpc_tools.protoc --proto_path=./src/artigo_search/proto --python_out=./src/artigo_search --grpc_python_out=./src/artigo_search index.proto
```

Change line `import index_pb2 as index__pb2` to `from . import index_pb2 as index__pb2` in `index_pb2_grpc.py`.

### Increase virtual memory
```sh
sudo sysctl -w vm.max_map_count=262144
```

### Data import
To import data, `.jsonl` files must be stored in the `./dump` folder. Only the latest file is processed. The following command must be executed while the application is running:
```sh
sudo docker-compose exec search python3 -m artigo_search --mode client --task insert
```

### Run tests
```sh
sudo docker-compose exec search pytest --verbose
```
