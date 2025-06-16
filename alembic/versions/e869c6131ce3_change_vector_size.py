"""Change vector size

Revision ID: e869c6131ce3
Revises: ee5bd3065bae
Create Date: 2025-06-10 17:04:07.526332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'e869c6131ce3'
down_revision: Union[str, None] = 'ee5bd3065bae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('notes', 'embedding',
               existing_type=pgvector.sqlalchemy.vector.VECTOR(dim=1536),
               type_=pgvector.sqlalchemy.vector.VECTOR(dim=384),
               existing_nullable=True)

def downgrade() -> None:
    return