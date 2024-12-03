from alembic import op
import sqlalchemy as sa

revision = '<timestamp>'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'passengers',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FL_DATE', sa.Date, nullable=False),
        sa.Column('OP_CARRIER', sa.String(5), nullable=False),
        sa.Column('OP_CARRIER_FL_NUM', sa.String(10), nullable=False),
        sa.Column('ORIGIN', sa.String(3), nullable=False),
        sa.Column('DEST', sa.String(3), nullable=False),
        sa.Column('CRS_DEP_TIME', sa.Integer, nullable=False),
        sa.Column('DEP_TIME', sa.Integer, default=0),
        sa.Column('DEP_DELAY', sa.Float, default=0),
        sa.Column('TAXI_OUT', sa.Float, default=0),
        sa.Column('WHEELS_OFF', sa.Float, default=0),
        sa.Column('WHEELS_ON', sa.Float, default=0),
        sa.Column('TAXI_IN', sa.Float, default=0),
        sa.Column('CRS_ARR_TIME', sa.Integer, nullable=False),
        sa.Column('ARR_TIME', sa.Integer, default=0),
        sa.Column('ARR_DELAY', sa.Float, default=0),
        sa.Column('CANCELLED', sa.Float, default=0),
        sa.Column('CANCELLATION_CODE', sa.String(1), nullable=True),
        sa.Column('DIVERTED', sa.Float, default=0),
        sa.Column('CRS_ELAPSED_TIME', sa.Float, nullable=False),
        sa.Column('ACTUAL_ELAPSED_TIME', sa.Float, default=0),
        sa.Column('AIR_TIME', sa.Float, default=0),
        sa.Column('DISTANCE', sa.Float, nullable=False),
        sa.Column('CARRIER_DELAY', sa.Float, default=0),
        sa.Column('WEATHER_DELAY', sa.Float, default=0),
        sa.Column('NAS_DELAY', sa.Float, default=0),
        sa.Column('SECURITY_DELAY', sa.Float, default=0),
        sa.Column('LATE_AIRCRAFT_DELAY', sa.Float, default=0),
        sa.Column('createdAt', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('passengers')
