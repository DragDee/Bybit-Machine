"""empty message

Revision ID: b8535a0c534f
Revises: 74f8821c755b
Create Date: 2024-12-09 13:00:19.823572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8535a0c534f'
down_revision: Union[str, None] = '74f8821c755b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ts_accounts', sa.Column('cookie', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ts_accounts', 'cookie')
    # ### end Alembic commands ###