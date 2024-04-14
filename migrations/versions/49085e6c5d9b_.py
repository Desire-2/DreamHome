"""empty message

Revision ID: 49085e6c5d9b
Revises: 6f1471774fdd
Create Date: 2024-04-14 23:13:26.440674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49085e6c5d9b'
down_revision = '6f1471774fdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('num_bedrooms', sa.Integer(), nullable=True),
    sa.Column('num_bathrooms', sa.Integer(), nullable=True),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('year_built', sa.Integer(), nullable=True),
    sa.Column('property_type', sa.String(length=50), nullable=True),
    sa.Column('amenities', sa.String(length=255), nullable=True),
    sa.Column('is_featured', sa.Boolean(), nullable=True),
    sa.Column('is_for_sale', sa.Boolean(), nullable=True),
    sa.Column('is_for_rent', sa.Boolean(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=100), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('_url', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    op.drop_table('properties')
    op.drop_table('users')
    # ### end Alembic commands ###
