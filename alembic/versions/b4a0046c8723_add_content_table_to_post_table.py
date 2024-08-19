"""add content table to post table

Revision ID: b4a0046c8723
Revises: 6ecc5920d4f8
Create Date: 2024-08-19 13:29:51.895620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4a0046c8723'
down_revision: Union[str, None] = '6ecc5920d4f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass