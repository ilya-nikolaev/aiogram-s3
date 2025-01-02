import aioboto3

from aiogram_s3.config import S3Config


def create_session(config: S3Config) -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.region,
    )
