from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command

from settings import settings

engine = create_engine(
    f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}",
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)


def run_migrations() -> None:
    """Apply all pending Alembic migrations on startup."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def ping_db() -> bool:
    """Return True if the database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def close_db() -> None:
    engine.dispose()
