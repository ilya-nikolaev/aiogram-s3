from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from aioboto3.session import Session
from aiogram import Bot
from aiogram.types.input_file import DEFAULT_CHUNK_SIZE, InputFile

from aiogram_s3.types import S3Bucket, S3Config, S3Key

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class S3InputFile(InputFile):
    def __init__(  # noqa: PLR0913
        self,
        s3_key: S3Key,
        s3_bucket: S3Bucket,
        s3_config: S3Config | None = None,
        s3_session: Session | None = None,
        s3_client: "S3Client | None" = None,
        filename: str | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        if filename is None:
            filename = s3_key
        super().__init__(filename, chunk_size)

        self.s3_config = s3_config
        self.s3_session = s3_session
        self.s3_client = s3_client

        self.s3_key = s3_key
        self.s3_bucket = s3_bucket

    def _get_session(self) -> Session:
        if self.s3_session is not None:
            return self.s3_session

        if self.s3_config is not None:
            return Session(
                aws_access_key_id=self.s3_config.aws_access_key_id,
                aws_secret_access_key=self.s3_config.aws_secret_access_key,
                region_name=self.s3_config.region,
            )

        message = (
            "Cannot get S3 session, S3Config or S3Session must be provided"
        )
        raise ValueError(message)

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator["S3Client", None]:
        if self.s3_client is not None:
            yield self.s3_client
        else:
            s3_session = self._get_session()
            if self.s3_config is not None:
                async with s3_session.client(
                    "s3",
                    region_name=self.s3_config.region,
                    endpoint_url=self.s3_config.endpoint_url,
                    aws_access_key_id=self.s3_config.aws_access_key_id,
                    aws_secret_access_key=self.s3_config.aws_secret_access_key,
                ) as s3_client:
                    yield s3_client
            else:
                async with s3_session.client("s3") as s3_client:
                    yield s3_client

    async def read(self, bot: Bot) -> AsyncGenerator[bytes, None]:  # noqa: ARG002
        async with self._get_client() as s3:
            obj = await s3.get_object(
                Bucket=self.s3_bucket,
                Key=self.s3_key,
            )
            while data := await obj["Body"].read(self.chunk_size):
                yield data
