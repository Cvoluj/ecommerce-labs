from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
