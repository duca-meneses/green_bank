from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    API_DOC_URL: str
    SWAGGER_UI_URL: str
    API_TITLE: str

