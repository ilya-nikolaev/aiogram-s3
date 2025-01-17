# noqa: INP001
import asyncio
import logging
import os

from aioboto3 import Session
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart

from aiogram_s3 import S3Config
from aiogram_s3.input_file import S3InputFile

router = Router()
main_menu_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="By config",
                callback_data="config",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="By session",
                callback_data="session",
            ),
        ],
    ],
)


@router.message(CommandStart())
async def process_photo(m: types.Message) -> None:
    await m.answer("Hello!", reply_markup=main_menu_keyboard)


@router.callback_query(F.data == "config")
async def process_config_button(
    cq: types.CallbackQuery,
    bot: Bot,
    s3_config: S3Config,
    s3_key: str,
    s3_bucket: str,
) -> None:
    if cq.message is None:
        raise RuntimeError
    await cq.answer()
    await bot.send_document(
        cq.message.chat.id,
        S3InputFile(s3_key, s3_bucket, s3_config=s3_config),
        caption="Document got from S3 (by config)",
    )


@router.callback_query(F.data == "session")
async def process_session_button(
    cq: types.CallbackQuery,
    bot: Bot,
    s3_session: Session,
    s3_key: str,
    s3_bucket: str,
) -> None:
    if cq.message is None:
        raise RuntimeError
    await cq.answer()
    await bot.send_document(
        cq.message.chat.id,
        S3InputFile(s3_key, s3_bucket, s3_session=s3_session),
        caption="Document got from S3 (by session)",
    )


def get_required_env_variable(key: str) -> str:
    if (value := os.getenv(key)) is None:
        msg = f"{key} environment variable is required"
        raise RuntimeError(msg)
    return value


async def main() -> None:
    bot = Bot(token=get_required_env_variable("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()

    s3_config = S3Config(
        aws_access_key_id=get_required_env_variable("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_required_env_variable(
            "AWS_SECRET_ACCESS_KEY",
        ),
        region=get_required_env_variable("S3_REGION"),
        endpoint_url=get_required_env_variable("S3_URL"),
    )

    s3_session = Session(
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.region,
    )

    dp["s3_config"] = s3_config
    dp["s3_session"] = s3_session

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
