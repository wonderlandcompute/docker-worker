Skygrid docker-worker
---
To run worker - point `DOCKER_WORKER_CONFIG` to [config file](example.cfg)
```
export DOCKER_WORKER_CONFIG=path/to/docker-worker/example.cfg
```
Test with
```
cd scripts/ && test-descriptor descriptor.json 
```
