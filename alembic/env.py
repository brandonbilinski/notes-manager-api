from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from alembic import context
import asyncio

# Your async database URL
DATABASE_URL = "postgresql+asyncpg://testuser:testpass@localhost/dbname"

# Create an async engine for other operations in your app
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sync engine for Alembic migrations
sync_engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))

# Create the sessionmaker for async and sync if necessary
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Alembic's target_metadata for autogeneration
from app.models import Base
target_metadata = Base.metadata

def run_migrations_online() -> None:
    """Run migrations in 'online' mode with a sync engine."""
    # Instead of using async engine directly, use a sync engine
    connectable = sync_engine

    with connectable.connect() as connection:
        # Configure Alembic context to use the sync connection
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

def do_migrations_async():
    """Asynchronous migrations - not used in Alembic directly but here for clarity."""
    pass

# Wrap Alembic's sync migration runner with a synchronous function
def run_migrations():
    run_migrations_online()