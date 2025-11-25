"""make comandas.codigo autoincrement

Revision ID: 40e8b95328c2
Revises: 
Create Date: 2025-11-25 00:25:15.503475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40e8b95328c2'
down_revision = None
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    conn = op.get_bind()

    # 1) garantir que a coluna é INT NOT NULL UNIQUE (uma instrução simples)
    conn.execute(sa.text("""
        ALTER TABLE comandas
        MODIFY COLUMN codigo INT NOT NULL UNIQUE
    """))

    # 2) obter MAX(codigo) via SELECT (fetch em Python)
    result = conn.execute(sa.text("SELECT IFNULL(MAX(codigo), 0) AS m FROM comandas")).fetchone()
    maxv = int(result[0]) if result is not None else 0
    next_val = maxv + 1

    # 3) ajustar AUTO_INCREMENT para começar em next_val
    conn.execute(sa.text(f"ALTER TABLE comandas AUTO_INCREMENT = {next_val}"))


def downgrade():
    conn = op.get_bind()
    # reverte: remove a propriedade AUTO_INCREMENT (modifica coluna sem AUTO_INCREMENT)
    conn.execute(sa.text("""
        ALTER TABLE comandas
        MODIFY COLUMN codigo INT NOT NULL
    """))


