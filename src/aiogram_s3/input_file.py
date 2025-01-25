from __future__ import annotations

from collections.abc import AsyncGenerator

from aiobotocore.response import StreamingBody
from aiogram import Bot
from aiogram.types.input_file import DEFAULT_CHUNK_SIZE, InputFile
from types_aiobotocore_s3 import S3Client

from aiogram_s3.types import S3Bucket, S3Key


class S3InputFile(InputFile):
    def __init__(
        self,
        s3_key: S3Key,
        s3_bucket: S3Bucket,
        s3_client: S3Client,
        filename: str | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        if filename is None:
            filename = s3_key
        super().__init__(filename, chunk_size)
        self.s3_key = s3_key
        self.s3_bucket = s3_bucket
        self.s3_client = s3_client

    async def read(self, bot: Bot) -> AsyncGenerator[bytes, None]:  # noqa: ARG002
        obj = await self.s3_client.get_object(
            Bucket=self.s3_bucket,
            Key=self.s3_key,
        )
        body: StreamingBody = obj["Body"]
        async for chunk in body.iter_chunks(self.chunk_size):
            yield chunk
