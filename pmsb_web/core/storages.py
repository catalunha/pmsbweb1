from storages.backends.s3boto3 import S3Boto3Storage


def MediaStorage():
    return S3Boto3Storage(location='media')
