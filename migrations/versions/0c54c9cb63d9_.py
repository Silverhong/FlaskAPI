"""empty message

Revision ID: 0c54c9cb63d9
Revises: 304d0e5bdbe3
Create Date: 2019-07-23 18:48:35.134831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c54c9cb63d9'
down_revision = '304d0e5bdbe3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Office_DeptId_fkey', 'Office', type_='foreignkey')
    op.create_foreign_key(None, 'Office', 'Department', ['DeptId'], ['DeptId'], ondelete='CASCADE')
    op.drop_constraint('Staff_DeptID_fkey', 'Staff', type_='foreignkey')
    op.drop_constraint('Staff_OfficeId_fkey', 'Staff', type_='foreignkey')
    op.create_foreign_key(None, 'Staff', 'Department', ['DeptID'], ['DeptId'], ondelete='CASCADE')
    op.create_foreign_key(None, 'Staff', 'Office', ['OfficeId'], ['OfficeId'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Staff', type_='foreignkey')
    op.drop_constraint(None, 'Staff', type_='foreignkey')
    op.create_foreign_key('Staff_OfficeId_fkey', 'Staff', 'Office', ['OfficeId'], ['OfficeId'])
    op.create_foreign_key('Staff_DeptID_fkey', 'Staff', 'Department', ['DeptID'], ['DeptId'])
    op.drop_constraint(None, 'Office', type_='foreignkey')
    op.create_foreign_key('Office_DeptId_fkey', 'Office', 'Department', ['DeptId'], ['DeptId'])
    # ### end Alembic commands ###
