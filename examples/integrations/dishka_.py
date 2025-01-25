import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from dishka import make_async_container
from dishka.integrations.aiogram import FromDishka, setup_dishka
from types_aiobotocore_s3 import S3Client

from aiogram_s3.input_file import S3InputFile
from aiogram_s3.integrations.dishka import AiogramS3Provider
from aiogram_s3.types import S3Bucket, S3Key
from aiogram_s3.types.config import S3Config

router = Router()


@router.message(CommandStart())
async def process_photo(
    m: types.Message,
    s3_client: FromDishka[S3Client],
    s3_key: S3Key,
    s3_bucket: S3Bucket,
) -> None:
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
    s3_config = get_s3_config()

    dp = Dispatcher()
    dp.include_router(router)

    dp["s3_key"] = get_required_env_variable("S3_KEY")
    dp["s3_bucket"] = get_required_env_variable("S3_BUCKET_NAME")

    bot = Bot(token=get_required_env_variable("TELEGRAM_BOT_TOKEN"))

    container = make_async_container(AiogramS3Provider(s3_config))
    setup_dishka(container, dp, auto_inject=True)

    try:
        await dp.start_polling(bot)
    except Exception:
        await bot.session.close()
        await dp.storage.close()
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
