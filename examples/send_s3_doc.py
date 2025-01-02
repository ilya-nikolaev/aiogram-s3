# noqa: INP001
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart

from aiogram_s3 import S3Config
from aiogram_s3.input_file import S3InputFile

router = Router()


@router.message(CommandStart())
async def process_photo(
    m: types.Message,
    s3_config: S3Config,
    s3_key: str,
) -> None:
    await m.answer_document(
        S3InputFile(s3_key, s3_config),
        caption="Document got from S3",
    )


def get_required_env_variable(key: str) -> str:
    if (value := os.getenv(key)) is None:
        msg = f"{key} environment variable is required"
        raise RuntimeError(msg)
    return value


async def main() -> None:
    bot = Bot(token=get_required_env_variable("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()

    dp["s3_config"] = S3Config(
        aws_access_key_id=get_required_env_variable("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_required_env_variable(
            "AWS_SECRET_ACCESS_KEY",
        ),
        region=get_required_env_variable("S3_REGION"),
        endpoint_url=get_required_env_variable("S3_URL"),
        bucket=get_required_env_variable("S3_BUCKET_NAME"),
    )
    dp["s3_key"] = get_required_env_variable("S3_KEY")

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
