import settings
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# import your SQLAlchemy models here
import models

# target_metadata = mymodel.Base.metadata
target_metadata = models.Base.metadata


# this function should return the connection and metadata for your target database
def get_url():
    return "postgresql://postgres:passw0rd@localhost:5442/agent"


config = context.config

# configure your target database connection here
config.set_main_option('url', get_url())

# interpret the config file for Python logging
fileConfig(config.config_file_name)

# add your SQLAlchemy models to the context's metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    urls = get_urls()
    for url in urls:
        print("\nrun migrations offline for url:", url)
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    urls = get_urls()
    for url in urls:
        print("\nrun migrations online for url:", url)
        connectable = create_engine(url)

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                process_revision_directives=process_revision_directives,
            )
            with context.begin_transaction():
                context.run_migrations()



# customize the naming convention for version files
def my_naming_convention_function(rev, _):
    # format the revision number with leading zeros
    revision_number = str(rev).zfill(5)
    return revision_number


def process_revision_directives(context, _, directives):
    migration_script = directives[0]
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()
    try:
        head_revision_int = int(head_revision)
    except ValueError:
        new_rev_id = 1
    except TypeError:
        new_rev_id = 1
    else:
        new_rev_id = head_revision_int + 1

    migration_script.rev_id = '{0:012}'.format(new_rev_id)


def get_urls():
    url = "postgresql://{}:{}@{}:{}/{}"
    return [
        url.format(
            settings.DB_USER,
            settings.DB_PASSWORD,
            settings.DB_HOST,
            settings.DB_PORT,
            settings.DB_DATABASE
        )
    ]

if context.is_offline_mode():
    run_migrations_offline()
else:
    # configure the naming convention for version files
    context.configure(
        url=get_url(), target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )

    run_migrations_online()
