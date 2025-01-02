# Aiogram S3
A lightweight library for seamless integration of Amazon S3 with aiogram. Simplify file uploads and downloads directly within your Telegram bots.

## Run example (`examples/send_s3_doc.py`)
```bash
python -m venv .venv
python -m pip install .

export TELEGRAM_BOT_TOKEN=...
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export S3_REGION=...
export S3_URL=...
export S3_BUCKET_NAME=...
export S3_KEY=...

python examples/send_s3_doc.py
```