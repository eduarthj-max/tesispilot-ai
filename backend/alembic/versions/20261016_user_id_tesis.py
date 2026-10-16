from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20261016_user_id_tesis'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add user_id to theses if it doesn't exist
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c['name'] for c in inspector.get_columns('theses')]
    if 'user_id' not in columns:
        op.add_column('theses', sa.Column('user_id', sa.String(), nullable=True))

    # Add password_hash to users if it doesn't exist
    columns = [c['name'] for c in inspector.get_columns('users')]
    if 'password_hash' not in columns:
        op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c['name'] for c in inspector.get_columns('theses')]
    if 'user_id' in columns:
        op.drop_column('theses', 'user_id')

    columns = [c['name'] for c in inspector.get_columns('users')]
    if 'password_hash' in columns:
        op.drop_column('users', 'password_hash')
