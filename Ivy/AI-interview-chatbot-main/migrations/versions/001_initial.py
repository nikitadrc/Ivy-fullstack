"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create interviews table
    op.create_table('interviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('candidate_name', sa.String(), nullable=False),
        sa.Column('position', sa.String(), nullable=False),
        sa.Column('scheduled_time', sa.DateTime(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('interview_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('recording_url', sa.String(), nullable=True),
        sa.Column('feedback', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create interview_analyses table
    op.create_table('interview_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('emotion_data', postgresql.JSON(), nullable=False),
        sa.Column('speech_data', postgresql.JSON(), nullable=False),
        sa.Column('behavioral_metrics', postgresql.JSON(), nullable=False),
        sa.Column('technical_assessment', postgresql.JSON(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create analytics table
    op.create_table('analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('total_interviews', sa.Integer(), nullable=False),
        sa.Column('successful_hires', sa.Integer(), nullable=False),
        sa.Column('average_duration', sa.Float(), nullable=False),
        sa.Column('success_rate', sa.Float(), nullable=False),
        sa.Column('feedback_scores', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create oauth2_accounts table
    op.create_table('oauth2_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('provider_user_id', sa.String(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('oauth2_accounts')
    op.drop_table('analytics')
    op.drop_table('interview_analyses')
    op.drop_table('interviews')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users') 