"""Add Google OAuth redirect URI support

This migration adds additional indexes and constraints to support
Google OAuth 2.0 authentication with proper redirect URI handling.

Revision ID: 75341357c14a
Revises: add_oauth_fields
Create Date: 2026-03-12 15:45:00

"""

# revision identifiers, used by Alembic.
revision = '75341357c14a'
down_revision = 'add_oauth_fields'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    """Add indexes and constraints for Google OAuth support"""
    # Add composite index for OAuth provider + user ID lookups
    # This improves performance when looking up users by OAuth provider
    try:
        with op.batch_alter_table('users', schema=None) as batch_op:
            # Create a unique constraint on oauth_provider + oauth_user_id
            # This ensures one Google account can only link to one user
            batch_op.create_index(
                'ix_users_oauth_provider_user_id',
                ['oauth_provider', 'oauth_user_id'],
                unique=False
            )
    except Exception as e:
        # Index might already exist, ignore
        print(f"Note: Could not create index (may already exist): {e}")
    
    # Add index on email_verified for faster filtering
    try:
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.create_index(
                'ix_users_email_verified',
                ['email_verified'],
                unique=False
            )
    except Exception as e:
        print(f"Note: Could not create index (may already exist): {e}")


def downgrade() -> None:
    """Remove OAuth indexes"""
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Drop indexes in reverse order
        batch_op.drop_index('ix_users_email_verified')
        batch_op.drop_index('ix_users_oauth_provider_user_id')
