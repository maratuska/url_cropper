from pydantic import BaseSettings as PydanticBaseSettings, BaseModel, Field, PostgresDsn


__all__ = [
    'conf',
    'AppConfig',
]


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    debug: bool = Field(default=False, env='debug_mode')
    short_base_url: str = Field(..., env='short_base_url')


class DatabaseSettings(BaseSettings):
    postgres_url: PostgresDsn = Field(..., env='postgres_url')


class AppConfig(BaseModel):
    api_settings: ApiSettings = ApiSettings()
    db_settings: DatabaseSettings = DatabaseSettings()

    class Config:
        allow_mutation = False


conf = AppConfig()
