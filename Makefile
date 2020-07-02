build:
	docker build --pull --file=Dockerfile --tag=${REGISTRY_PATH}:${IMAGE_TAG} .

push:
	docker push ${REGISTRY_PATH}:${IMAGE_TAG}
