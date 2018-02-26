"""v3

Revision ID: 37f589091066
Revises: 
Create Date: 2017-11-23 11:18:45.271676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '37f589091066'
down_revision = "94e3c72a3fbc"
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file_resource', 'content',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('file_resource_version', 'content',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('return_material_order', 'returnReason',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('return_material_order_version', 'returnReason',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('train_record', 'trainRecordContent',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('train_record_version', 'trainRecordContent',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('train_file_resource', 'trainFileResourceContent',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('train_file_resource_version', 'trainFileResourceContent',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)

    op.alter_column('trouble_shooting', 'maintainStep',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('trouble_shooting_version', 'maintainStep',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('trouble_shooting', 'description',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('trouble_shooting_version', 'description',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)

    op.alter_column('examine_repair_record', 'maintainStep',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('examine_repair_record_version', 'maintainStep',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('examine_repair_record', 'description',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('examine_repair_record_version', 'description',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file_resource', 'content',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('file_resource_version', 'content',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('return_material_order', 'returnReason',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('return_material_order_version', 'returnReason',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('train_record', 'trainRecordContent',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('train_record_version', 'trainRecordContent',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('train_file_resource', 'trainFileResourceContent',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('train_file_resource_version', 'trainFileResourceContent',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)

    op.alter_column('trouble_shooting', 'maintainStep',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('trouble_shooting_version', 'maintainStep',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('trouble_shooting', 'description',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('trouble_shooting_version', 'description',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)

    op.alter_column('examine_repair_record', 'maintainStep',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('examine_repair_record_version', 'maintainStep',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    op.alter_column('examine_repair_record', 'description',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True)
    op.alter_column('examine_repair_record_version', 'description',
               type_=mysql.VARCHAR(length=255),
               existing_type=sa.Text(),
               existing_nullable=True,
               autoincrement=False)
    # ### end Alembic commands ###