from pydantic import BaseModel


class S3Config(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str

    region: str = "us-east-1"

    endpoint_url: str
    bucket: str
