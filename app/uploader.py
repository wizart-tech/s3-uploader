import re
import os
import mimetypes
from os import path
import boto3
import argparse
from glob import glob

ALLOWED_VISIBILITIES = ['private', 'public-read']

client = None

arguments = {
    'S3_ACCESS_KEY': os.getenv('S3_ACCESS_KEY'),
    'S3_SECRET': os.getenv('S3_SECRET'),
    'S3_ENDPOINT': os.getenv('S3_ENDPOINT'),
    'S3_REGION': os.getenv('S3_REGION'),
    'S3_BUCKET': os.getenv('S3_BUCKET'),
    'S3_VISIBILITY': os.getenv('S3_VISIBILITY'),
    'S3_CONTENT_TYPE': os.getenv('S3_CONTENT_TYPE'),
    'S3_CONTENT_ENCODING': os.getenv('S3_CONTENT_ENCODING'),
    'S3_CACHE_CONTROL': os.getenv('S3_CACHE_CONTROL'),
    'S3_PATH': os.getenv('S3_PATH'),
    'S3_ROOT': os.getenv('S3_ROOT'),
    'PATH': '',
}


def init_arguments(args_parser=None):
    if not args_parser:
        return

    args_parser.add_argument('--s3_access_key', help='S3 storage access key.', type=str, required=False, default=None)
    args_parser.add_argument('--s3_secret', help='S3 storage secret key.', type=str, required=False, default=None)
    args_parser.add_argument('--s3_endpoint', help='Endpoint of s3 storage.', type=str, required=False, default=None)
    args_parser.add_argument('--s3_region', help='Region of s3 storage.', type=str, required=False, default=None)
    args_parser.add_argument('--s3_bucket', help='Name of a bucket.', type=str, required=False, default=None)
    args_parser.add_argument(
        '--s3_visibility',
        help='Either private or public visibility. Available values: {}.'.format('/'.join(ALLOWED_VISIBILITIES)),
        type=str,
        required=False,
        default=None
    )
    args_parser.add_argument('--s3_content_type', help='S3 content type.', type=str, required=False,
                             default=None)
    args_parser.add_argument('--s3_content_encoding', help='S3 content encoding.', type=str, required=False,
                             default=None)
    args_parser.add_argument('--s3_cache_control', help='S3 cache control.', type=str, required=False,
                             default=None)
    args_parser.add_argument('--s3_root', help='Root s3 bucket directory.', type=str, required=False, default=None)

    args_parser.add_argument('--s3_path', help='Path to store file at.', type=str)
    args_parser.add_argument('--path', help='Path to file to upload.', type=str)


def upload_files():
    filepath = arguments.get('PATH')

    if not glob(filepath):
        print('No files to upload, please select correct filepath. Current is: "{}"'.format(filepath))

    if path.isfile(filepath):
        upload_file(filepath)
    else:
        for file in glob(filepath):
            upload_file(file)


def upload_file(filepath):
    global client

    store_at = arguments.get('S3_PATH').strip('/')

    prefix = arguments.get('S3_ROOT')
    if prefix:
        store_at = "{}/{}".format(prefix, store_at)

    store_at = "{}/{}".format(store_at, path.basename(filepath))

    extra_args = {'ACL': arguments.get('S3_VISIBILITY', 'public-read')}

    content_type = arguments.get('S3_CONTENT_TYPE')
    mimetype, _ = mimetypes.guess_type(filepath)
    content_type = content_type if content_type is not None else mimetype
    content_encoding = arguments.get('S3_CONTENT_ENCODING')
    cache_control = arguments.get('S3_CACHE_CONTROL')

    if content_type is not None:
        extra_args.update({'ContentType': content_type})
    if content_encoding is not None:
        extra_args.update({'ContentEncoding': content_encoding})
    if cache_control is not None:
        extra_args.update({'CacheControl': cache_control})

    client.upload_file(
        str(filepath),
        arguments.get('S3_BUCKET'),
        store_at,
        ExtraArgs=extra_args
    )

    print('Successful file "{}" upload.'.format(path.basename(filepath)))


def set_variables_from_args(args):
    for arg in arguments:
        lower_arg = arg.lower()

        if getattr(args, lower_arg):
            arguments[arg] = getattr(args, lower_arg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_arguments(args_parser=parser)

    set_variables_from_args(parser.parse_args())

    is_regex = False
    file_path = arguments.get('PATH')

    try:
        re.compile(file_path)
        is_regex = True
    except re.error:
        is_regex = False

    if not path.isfile(file_path) and not is_regex:
        print('Path argument must be a valid path to a file Or a regex expression.')
        exit(0)

    if arguments.get('S3_VISIBILITY') not in ALLOWED_VISIBILITIES:
        print('Visibility should be one of: {}.'.format(','.join(ALLOWED_VISIBILITIES)))
        exit(0)

    client = boto3.client(
        's3',
        region_name=arguments.get('S3_REGION'),
        endpoint_url=arguments.get('S3_ENDPOINT'),
        aws_access_key_id=arguments.get('S3_ACCESS_KEY'),
        aws_secret_access_key=arguments.get('S3_SECRET')
    )

    upload_files()
