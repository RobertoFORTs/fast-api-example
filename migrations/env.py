import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool, text
from alembic import context
from simple_api.infra.db import Base
from simple_api.infra.models.booking import Booking
from simple_api.infra.models.property import Property
from simple_api.infra.models.db_meta import DBMeta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL não encontrado no .env ou nas variáveis de ambiente.")

config.set_main_option("sqlalchemy.url", database_url)

sync_engine = create_engine(
    database_url.replace("+asyncpg", ""),
    poolclass=pool.NullPool,
    connect_args={"options": "-c search_path=public"}
)

def run_migrations_offline() -> None:
    url = database_url.replace("+asyncpg", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
