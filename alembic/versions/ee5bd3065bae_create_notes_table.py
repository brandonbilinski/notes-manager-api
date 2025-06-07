"""create notes table

Revision ID: ee5bd3065bae
Revises: 
Create Date: 2025-06-06 17:21:25.018240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = 'ee5bd3065bae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    op.create_table(
        'notes',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('embedding', Vector(1536)),
        sa.Column('created',sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('notes')