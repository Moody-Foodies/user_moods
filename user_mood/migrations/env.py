import logging
from logging.config import fileConfig

from alembic import context
from flask import current_app

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

config = context.config

def get_engine_url():
    with current_app.app_context():
        return current_app.config["SQLALCHEMY_DATABASE_URI"]

config.set_main_option('sqlalchemy.url', get_engine_url())

# Access the metadata from the Flask app's SQLAlchemy extension
with current_app.app_context():
    target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    with current_app.app_context():
        run_migrations_online()
