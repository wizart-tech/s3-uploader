build:
	docker build --pull --file=Dockerfile --tag=${REGISTRY_PATH}:${IMAGE_TAG} .

push:
	docker push ilyastasiukevich/s3-uploader:${IMAGE_TAG}
