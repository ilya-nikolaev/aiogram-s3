from __future__ import annotations

from collections.abc import AsyncIterator

from aioboto3.session import Session
from dishka import Provider, Scope, provide
from dishka.entities.scope import BaseScope
from types_aiobotocore_s3 import S3Client

from aiogram_s3.types import S3Config


class AiogramS3Provider(Provider):
    def __init__(
        self,
        s3_config: S3Config,
        scope: BaseScope | None = None,
        component: str | None = None,
    ) -> None:
        super().__init__(scope, component)
        self.s3_config = s3_config

    @provide(scope=Scope.APP)
    def get_config(self) -> S3Config:
        return self.s3_config

    @provide(scope=Scope.APP)
    def get_session(self, s3_config: S3Config) -> Session:
        return Session(
            aws_access_key_id=s3_config.aws_access_key_id,
            aws_secret_access_key=s3_config.aws_secret_access_key,
            region_name=s3_config.region,
        )

    @provide(scope=Scope.APP)
    async def get_client(
        self,
        s3_config: S3Config,
        s3_session: Session,
    ) -> AsyncIterator[S3Client]:
        async with s3_session.client(
            "s3",
            endpoint_url=s3_config.endpoint_url,
        ) as s3_client:
            yield s3_client
