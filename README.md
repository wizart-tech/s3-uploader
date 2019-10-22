# s3-uploader

Requirements:

 - python 3
 - virtualenv
 
This package is using boto3 to work with S3-like storage.

```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Usage:

```bash
python uploader.py S3_ACCESS_KEY \
    S3_SECRET \
    S3_ENDPOINT \
    S3_REGION \
    S3_BUCKET \
    S3_VISIBILITY \
    S3_PATH \
    SOURCE_FILE_PATH \
    --s3_root="S3_ROOT_PATH"
```

Positional arguments:
 - S3_ACCESS_KEY - S3 storage access key.
 - S3_SECRET - S3 storage secret key.
 - S3_ENDPOINT - Endpoint of s3 storage.
 - S3_REGION - Region of s3 storage.
 - S3_BUCKET -  Name of a bucket.
 - S3_VISIBILITY - Either private or public visibility. Available values: private/public-read.
 - S3_PATH - Path to store file at.
 - SOURCE_FILE_PATH - Path to file to upload.
 
Optional arguments:
 - --s3_root - Root s3 bucket directory.
