"""empty message

Revision ID: 515bc2b61454
Revises: aebd3574fa0e
Create Date: 2016-06-27 15:52:51.625122

"""

# revision identifiers, used by Alembic.
revision = '515bc2b61454'
down_revision = 'aebd3574fa0e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    ### end Alembic commands ###
