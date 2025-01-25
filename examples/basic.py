import asyncio
import logging
import os

from aioboto3 import Session
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart

from aiogram_s3 import S3Config
from aiogram_s3.input_file import S3InputFile
from aiogram_s3.types import S3Bucket, S3Key

router = Router()


@router.message(CommandStart())
async def process_photo(
    m: types.Message,
    s3_config: S3Config,
    s3_session: Session,
    s3_key: S3Key,
    s3_bucket: S3Bucket,
) -> None:
    async with s3_session.client(
        "s3",
        endpoint_url=s3_config.endpoint_url,
    ) as s3_client:
        await m.answer_document(S3InputFile(s3_key, s3_bucket, s3_client))


def get_s3_config() -> S3Config:
    return S3Config(
        aws_access_key_id=get_required_env_variable("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_required_env_variable(
            "AWS_SECRET_ACCESS_KEY",
        ),
        region=get_required_env_variable("S3_REGION"),
        endpoint_url=get_required_env_variable("S3_URL"),
    )


def get_required_env_variable(key: str) -> str:
    if (value := os.getenv(key)) is None:
        msg = f"{key} environment variable is required"
        raise RuntimeError(msg)
    return value


async def main() -> None:
    bot = Bot(token=get_required_env_variable("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()

    s3_config = get_s3_config()

    dp["s3_config"] = s3_config
    dp["s3_session"] = Session(
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.region,
    )

    dp["s3_key"] = get_required_env_variable("S3_KEY")
    dp["s3_bucket"] = get_required_env_variable("S3_BUCKET_NAME")

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception:
        await bot.session.close()
        await dp.storage.close()
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
