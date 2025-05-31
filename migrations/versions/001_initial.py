"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-19 10:00:00.000000

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
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create interviews table
    op.create_table(
        'interviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('candidate_id', sa.Integer(), nullable=False),
        sa.Column('interviewer_id', sa.Integer(), nullable=False),
        sa.Column('position', sa.String(), nullable=False),
        sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('status', sa.String(), nullable=False, server_default='scheduled'),
        sa.Column('feedback', sa.Text()),
        sa.Column('calendar_event_id', sa.String()),
        sa.Column('meeting_link', sa.String()),
        sa.Column('materials_url', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['candidate_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['interviewer_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create interview_questions table
    op.create_table(
        'interview_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create interview_responses table
    op.create_table(
        'interview_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column('score', sa.Integer()),
        sa.Column('feedback', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['interview_questions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create files table
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('upload_time', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer()),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('files')
    op.drop_table('interview_responses')
    op.drop_table('interview_questions')
    op.drop_table('interviews')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users') 