from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    db_url: str = Field(alias="DATABASE_URL")
    model_uri: str = Field(
        "runs:/c518611fef064b2ea8fc3c4e3e011a51/getaround",
        alias="MODEL_URI",
    )


settings = Settings()
