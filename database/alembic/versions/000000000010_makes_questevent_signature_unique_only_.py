"""Makes QuestEvent signature unique only if not null or empty

Revision ID: 000000000010
Revises: 000000000009
Create Date: 2024-05-13 13:35:08.248429

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '000000000010'
down_revision = '000000000009'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing index if it exists; adjust if your environment might not have it
    op.execute("ALTER TABLE quest_event DROP CONSTRAINT quest_event_signature_key;")

    # Create a new partial unique index that excludes empty strings
    op.create_index('idx_unique_signature', 'quest_event', ['signature'],
                    unique=True, postgresql_where=sa.text(
            "signature IS NOT NULL AND signature != ''"))


def downgrade():
    # Remove the new index
    op.drop_index('idx_unique_signature', table_name='quest_event')

    # Optionally recreate the old index if needed; remove if not applicable
    op.create_unique_constraint('quest_event_signature_key', 'quest_event', ['signature'])

