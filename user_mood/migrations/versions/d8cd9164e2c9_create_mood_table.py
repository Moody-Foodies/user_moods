"""Create mood table

Revision ID: d8cd9164e2c9
Revises: 
Create Date: 2024-05-14 13:06:30.655251

"""

from alembic import op
import sqlalchemy as sa

# Define initial data to insert into the mood table
initial_data = [
    {'mood': 4, 'user_id': 1, 'date': '2024-05-01'},
    {'mood': 3, 'user_id': 1, 'date': '2024-05-02'},
    {'mood': 5, 'user_id': 2, 'date': '2024-05-03'},
]

# revision identifiers, used by Alembic.
revision = 'd8cd9164e2c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mood',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mood', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert initial data into the mood table
    for data in initial_data:
        op.execute(
            sa.text(
                "INSERT INTO mood (mood, user_id, date) VALUES (:mood, :user_id, :date)"
            ).bindparams(
                mood=data['mood'],
                user_id=data['user_id'],
                date=data['date']
            )
        )


def downgrade():
    op.drop_table('mood')
