from dataclasses import dataclass

__all__ = ["S3Config"]


@dataclass(frozen=True, slots=True, kw_only=True)
class S3Config:
    aws_access_key_id: str
    aws_secret_access_key: str

    region: str = "us-east-1"

    endpoint_url: str
