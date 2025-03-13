"""Changed Houses table

Revision ID: 9ea457c3a8e1
Revises: ec8ba392db67
Create Date: 2025-03-13 23:04:36.987658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ea457c3a8e1'
down_revision: Union[str, None] = 'ec8ba392db67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавляем колонку как nullable сначала
    op.add_column('houses', sa.Column('type', sa.String(), nullable=True))
    
    # Заполняем существующие записи значением по умолчанию
    op.execute("UPDATE houses SET type = 'sell' WHERE type IS NULL")
    
    # Меняем колонку на NOT NULL
    op.alter_column('houses', 'type', nullable=False)

def downgrade():
    op.drop_column('houses', 'type')
