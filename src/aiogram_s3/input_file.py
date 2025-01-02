from collections.abc import AsyncGenerator

import aioboto3
from aiogram import Bot
from aiogram.types.input_file import DEFAULT_CHUNK_SIZE, InputFile

from aiogram_s3.config import S3Config
from aiogram_s3.session import create_session


class S3InputFile(InputFile):
    def __init__(
        self,
        s3_key: str,
        s3_config: S3Config,
        s3_session: aioboto3.Session | None = None,
        filename: str | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        if filename is None:
            filename = s3_key
        super().__init__(filename, chunk_size)

        self.s3_config = s3_config
        if s3_session is None:
            s3_session = create_session(s3_config)
        self.s3_session = s3_session
        self.s3_key = s3_key

    async def read(self, bot: Bot) -> AsyncGenerator[bytes, None]:  # noqa: ARG002
        async with self.s3_session.client(
            "s3",
            endpoint_url=self.s3_config.endpoint_url,
        ) as s3:
            obj = await s3.get_object(
                Bucket=self.s3_config.bucket,
                Key=self.s3_key,
            )
            while file_data := await obj["Body"].read(self.chunk_size):
                yield file_data
