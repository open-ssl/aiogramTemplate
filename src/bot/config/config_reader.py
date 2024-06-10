from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

CONFIG_FILE_NAME = ".env"
CONFIG_FILE_ENCODING = "utf-8"


class BotConfig(BaseSettings):
    bot_token: SecretStr
    tg_user_id: int
    model_config = SettingsConfigDict(
        env_file=CONFIG_FILE_NAME, env_file_encoding=CONFIG_FILE_ENCODING
    )


def get_config_reader() -> BotConfig:
    return BotConfig()
