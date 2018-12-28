build-image:
	 docker build -t registry.gitlab.com/lambda-hse/registry/dockerworker .

test-image:
	echo "No tests ;("

run-image:
	docker run  -v /var/run/docker.sock:/var/run/docker.sock -v /data:/data -it registry.gitlab.com/lambda-hse/registry/dockerworker

debug-container:
	docker run  -v /var/run/docker.sock:/var/run/docker.sock -v /data:/data -it --entrypoint='' registry.gitlab.com/lambda-hse/registry/dockerworker /bin/bash

push-image: build-image test-image
	#docker tag dockerworker registry.gitlab.com/lambda-hse/registry/dockerworker
	docker push registry.gitlab.com/lambda-hse/registry/dockerworker



