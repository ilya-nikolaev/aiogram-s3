# Aiogram S3

A lightweight library for seamless integration of Amazon S3 with aiogram. Simplify file uploads and downloads directly within your Telegram bots.


## Features

+ Effortless integration with Amazon S3.
+ Simplifies file uploads and downloads for aiogram Telegram bots.
+ Lightweight and easy to use


## Installation

You can install the library directly from the repository:
```shell
python -m pip install git+https://github.com/ilya-nikolaev/aiogram-s3.git
```

### Optional dependencies

Specify optional dependencies to tailor the installation to your needs:
+ `dev` - Includes development tools (`ruff`, `mypy` and `pre-commit`)
+ `di` - Includes `dishka`

#### Example with Optional Dependencies:

```shell
python -m pip install "aiogram-s3[dev] @ git+https://github.com/ilya-nikolaev/aiogram-s3.git"
```


## Running the Example Script

The example script (examples/send_s3_doc.py) demonstrates how to use the library. Follow these steps to set up and run it:

1. Clone the code:

    ```shell
    git clone https://github.com/ilya-nikolaev/aiogram-s3.git
    cd aiogram-s3
    ```

1. Create and activate a virtual environment:

    ```shell
    python -m venv .venv
    source .venv/bin/activate
    ```

1. Install the library

    ```shell
    python -m pip install .
    ```

1. Set the required environment variables:

    ```shell
    export TELEGRAM_BOT_TOKEN=...
    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...
    export S3_REGION=...
    export S3_URL=...
    export S3_BUCKET_NAME=...
    export S3_KEY=...
    ```

1. Run the example script:

    ```shell
    python examples/send_s3_doc.py
    ```

1. Interact with your bot

    Send the `/start` command to begin interaction.
