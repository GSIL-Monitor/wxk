"""8925505_14

Revision ID: 580b0cf21e1c
Revises: fa55194eda35
Create Date: 2017-12-14 09:29:23.382799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '580b0cf21e1c'
down_revision = '7a5b0dcc0ea8'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('air_lxgz', 'relateDoc',
           existing_type=mysql.VARCHAR(length=1000),
           type_=sa.Text(),
           existing_nullable=True)

    op.alter_column('air_lxgz_version', 'relateDoc',
           existing_type=mysql.VARCHAR(length=1000),
           type_=sa.Text(),
           existing_nullable=True)


def downgrade():
    op.alter_column('air_lxgz', 'relateDoc',
           type_=mysql.VARCHAR(length=1000),
           existing_type=sa.Text(),
           existing_nullable=True)

    op.alter_column('air_lxgz_version', 'relateDoc',
           type_=mysql.VARCHAR(length=1000),
           existing_type=sa.Text(),
           existing_nullable=True)
