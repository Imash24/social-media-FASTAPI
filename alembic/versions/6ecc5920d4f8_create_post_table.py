"""create post table

Revision ID: 6ecc5920d4f8
Revises: 
Create Date: 2024-08-11 19:48:39.071098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ecc5920d4f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
