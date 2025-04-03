import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Backend Path को Manually Add करो
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# ✅ अब सही तरीके से Backend Import करो
 

from app.models import Base 
# Alembic Config
config = context.config

# ✅ Python Logging सेटअप
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ MetaData सेटअप
target_metadata = Base.metadata

# ✅ SQLite Database Path सही सेट करो
db_path = os.path.join(os.path.dirname(__file__), "..", "database.db")
config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=f"sqlite:///{db_path}",
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
