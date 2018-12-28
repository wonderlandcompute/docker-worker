build-image:
	 docker build -t registry.gitlab.com/lambda-hse/registry/dockerworker .

push-image:
	#docker tag dockerworker registry.gitlab.com/lambda-hse/registry/dockerworker
	docker push registry.gitlab.com/lambda-hse/registry/dockerworker

run-image:
	docker run  -v /var/run/docker.sock:/var/run/docker.sock -it registry.gitlab.com/lambda-hse/registry/dockerworker
