"""Add user_id column to blocks table

Revision ID: 96d358f09f76
Revises: 68146e7c0fa9
Create Date: 2024-12-02 23:36:48.625884

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "96d358f09f76"
down_revision: Union[str, None] = "68146e7c0fa9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "blocks", "content", type_=sa.JSON(), postgresql_using="content::json"
    )


def downgrade():
    op.alter_column(
        "blocks", "content", type_=sa.String(), postgresql_using="content::text"
    )
