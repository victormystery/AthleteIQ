"""Enforce single questionnaire response per user

Revision ID: 1b7c9f2f4d11
Revises: a8dcbc00d364
Create Date: 2026-03-17 19:35:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b7c9f2f4d11"
down_revision = "a8dcbc00d364"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Keep only the newest questionnaire row per user before adding uniqueness.
    op.execute(
        """
        DELETE FROM questionnaire_responses q
        USING (
            SELECT id
            FROM (
                SELECT
                    id,
                    ROW_NUMBER() OVER (
                        PARTITION BY user_id
                        ORDER BY COALESCE(updated_at, created_at) DESC, created_at DESC, id DESC
                    ) AS rn
                FROM questionnaire_responses
            ) ranked
            WHERE ranked.rn > 1
        ) duplicates
        WHERE q.id = duplicates.id;
        """
    )

    with op.batch_alter_table("questionnaire_responses", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "uq_questionnaire_responses_user_id",
            ["user_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("questionnaire_responses", schema=None) as batch_op:
        batch_op.drop_constraint("uq_questionnaire_responses_user_id", type_="unique")
