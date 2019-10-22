from os import path
import boto3
import argparse

ALLOWED_VISIBILITIES = ['private', 'public-read']

client = None


def init_arguments(args_parser=None):
    if not args_parser:
        return

    args_parser.add_argument('s3_access_key', help='S3 storage access key.', type=str)
    args_parser.add_argument('s3_secret', help='S3 storage secret key.', type=str)
    args_parser.add_argument('s3_endpoint', help='Endpoint of s3 storage.', type=str)
    args_parser.add_argument('s3_region', help='Region of s3 storage.', type=str)
    args_parser.add_argument('s3_bucket', help='Name of a bucket.', type=str)
    args_parser.add_argument(
        's3_visibility',
        help='Either private or public visibility. Available values: {}.'.format('/'.join(ALLOWED_VISIBILITIES)),
        type=str
    )
    args_parser.add_argument('s3_path', help='Path to store file at.', type=str)
    args_parser.add_argument('path', help='Path to file to upload.', type=str)

    args_parser.add_argument('--s3_root', help='Root s3 bucket directory.', type=str, required=False)


def upload_file(input_arguments):
    with open(input_arguments.path) as file:
        store_at = input_arguments.s3_path.strip('/')

        prefix = input_arguments.s3_root
        if prefix:
            store_at = "{}/{}".format(prefix, store_at)

        store_at = "{}/{}".format(store_at, path.basename(input_arguments.path))

        client.put_object(
            Bucket=input_arguments.s3_bucket,
            Key=store_at,
            ACL=input_arguments.s3_visibility,
            Body=file.read(),
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_arguments(args_parser=parser)

    args = parser.parse_args()

    if not path.isfile(args.path):
        print('Path argument must be a valid path to a file.')
        exit(0)

    if args.s3_visibility not in ALLOWED_VISIBILITIES:
        print('Visibility should be one of: {}.'.format(','.join(ALLOWED_VISIBILITIES)))
        exit(0)

    client = boto3.client(
        's3',
        region_name=args.s3_region,
        endpoint_url=args.s3_endpoint,
        aws_access_key_id=args.s3_access_key,
        aws_secret_access_key=args.s3_secret
    )

    upload_file(args)

    print('Successful file "{}" upload.'.format(path.basename(args.path)))
