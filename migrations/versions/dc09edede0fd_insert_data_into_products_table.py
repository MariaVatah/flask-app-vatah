"""Insert data into products table

Revision ID: dc09edede0fd
Revises: b73f4fb86ca7
Create Date: 2026-11-26 04:14:26.330006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc09edede0fd'
down_revision = 'b73f4fb86ca7'
branch_labels = None
depends_on = None


def upgrade():
    # Опис таблиці категорій
    categories_table = sa.table(
        'categories',
        sa.column('name', sa.String())
    )

    # Опис таблиці товарів
    products_table = sa.table(
        'products',
        sa.column('name', sa.String()),
        sa.column('price', sa.Float()),
        sa.column('active', sa.Boolean()),
        sa.column('category_id', sa.Integer())
    )

    # Додавання категорій
    op.bulk_insert(
        categories_table,
        [
            {'name': 'Books'},
            {'name': 'Electronics'},
            {'name': 'Clothing'}
        ]
    )

    # Додавання товарів
    op.bulk_insert(
        products_table,
        [
            {
                'name': 'Laptop',
                'price': 1200.0,
                'active': True,
                'category_id': 3
            },
            {
                'name': 'Smartphone',
                'price': 800.0,
                'active': True,
                'category_id': 3
            },
            {
                'name': 'Novel',
                'price': 15.0,
                'active': True,
                'category_id': 2
            },
            {
                'name': 'T-Shirt',
                'price': 25.0,
                'active': True,
                'category_id': 4
            }
        ]
    )


def downgrade():
    op.execute(
        "DELETE FROM products WHERE name IN "
        "('Laptop', 'Smartphone', 'Novel', 'T-Shirt')"
    )

    op.execute(
        "DELETE FROM categories WHERE name IN "
        "('Books', 'Electronics', 'Clothing')"
    )