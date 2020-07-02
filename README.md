# s3-uploader

Requirements:
 - docker
 - docker-compose
 
### Usage

#### Local development:

Build:
```bash
docker-compose build
```

Run:
```bash
cp .env.example .env

docker-compose run app python3 uploader.py S3_REMOTE_PATH filename.txt
```
Note: `filename.txt` must be in `uploading` directory.

#### Building and pushing complete docker image:
```bash
REGISTRY_PATH=${REGISTRY_PATH} IMAGE_TAG=${IMAGE_TAG} make build
REGISTRY_PATH=${REGISTRY_PATH} IMAGE_TAG=${IMAGE_TAG} make push
```
