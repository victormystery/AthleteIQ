"""Add OAuth fields to users table

Revision ID: add_oauth_fields
Revises: 
Create Date: 2026-03-12 10:50:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_oauth_fields'
down_revision = None  # Update this with the latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    """Add OAuth fields to users table"""
    # Make hashed_password nullable for OAuth users
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('hashed_password',
                              existing_type=sa.String(),
                              nullable=True)
        
        # Add OAuth provider fields
        batch_op.add_column(sa.Column('oauth_provider', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('oauth_user_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), default=False))
        batch_op.add_column(sa.Column('avatar_url', sa.String(), nullable=True))
        
        # Add index on oauth_user_id for faster lookups
        batch_op.create_index('ix_users_oauth_user_id', ['oauth_user_id'])


def downgrade():
    """Remove OAuth fields from users table"""
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('ix_users_oauth_user_id')
        batch_op.drop_column('avatar_url')
        batch_op.drop_column('email_verified')
        batch_op.drop_column('oauth_user_id')
        batch_op.drop_column('oauth_provider')
        
        # Restore hashed_password as non-nullable
        batch_op.alter_column('hashed_password',
                              existing_type=sa.String(),
                              nullable=False)
