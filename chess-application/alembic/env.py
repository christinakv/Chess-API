from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from core.config import settings  # Update this path if necessary
from core.models import Base

if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

target_metadata = Base.metadata
config = context.config

config.set_main_option("sqlalchemy.url", settings.url)