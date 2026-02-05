from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Config
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # App Bootstrap / Initialization Config
    init_superadmin_username: Optional[str] = Field(default=None, validation_alias="INIT_SUPERADMIN_USERNAME")
    init_superadmin_email: Optional[str] = Field(default=None, validation_alias="INIT_SUPERADMIN_EMAIL")
    init_superadmin_password: Optional[str] = Field(default=None, validation_alias="INIT_SUPERADMIN_PASSWORD")
    init_superadmin_full_name: str = Field(default="Super Admin", validation_alias="INIT_SUPERADMIN_FULL_NAME")

    init_default_categories: str = Field(default="", validation_alias="INIT_DEFAULT_CATEGORIES")

    class Config:
        env_file = ".env"


settings = Settings()
