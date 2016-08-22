"""empty message

Revision ID: 7a87619b9688
Revises: 5116b7edc6a7
Create Date: 2016-08-22 15:12:42.101484

"""

# revision identifiers, used by Alembic.
revision = '7a87619b9688'
down_revision = '5116b7edc6a7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'areas', 'districts', ['district_id'], ['id'])
    op.create_foreign_key(None, 'communities', 'areas', ['area_id'], ['id'])
    op.create_foreign_key(None, 'houses', 'users', ['author_id'], ['id'])
    op.create_foreign_key(None, 'houses', 'communities', ['community_id'], ['id'])
    op.create_foreign_key(None, 'images', 'houses', ['house_id'], ['id'])
    op.create_foreign_key(None, 'images', 'users', ['author_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.drop_constraint(None, 'houses', type_='foreignkey')
    op.drop_constraint(None, 'houses', type_='foreignkey')
    op.drop_constraint(None, 'communities', type_='foreignkey')
    op.drop_constraint(None, 'areas', type_='foreignkey')
    ### end Alembic commands ###
