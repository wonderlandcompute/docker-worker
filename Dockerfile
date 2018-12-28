FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y --allow-unauthenticated docker-ce
RUN apt-get install -y python3 
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

COPY . /docker-worker
COPY /certs/ /certs/
COPY config.yml /config.yml
COPY docker-worker.config /docker-worker.config
RUN cp -R /docker-worker/.aws $HOME/.aws

RUN pip install -r /docker-worker/requirements.txt && pip install /docker-worker
ENV DOCKER_WORKER_CONFIG=/docker-worker.config \
	WONDERLAND_CLIENT_CONFIG=/config.yml

ENTRYPOINT python3 /docker-worker/run.py



