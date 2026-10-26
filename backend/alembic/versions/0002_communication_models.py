"""Create users, children and personalized communication cards."""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def created_at() -> sa.Column:
    return sa.Column(
        "created_at", sa.DateTime(timezone=True), nullable=False,
        server_default=sa.func.now(),
    )


def updated_at() -> sa.Column:
    return sa.Column(
        "updated_at", sa.DateTime(timezone=True), nullable=False,
        server_default=sa.func.now(),
    )


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum(
            "parent", "specialist", "admin", name="user_role",
            native_enum=False, create_constraint=True,
        ), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        created_at(), updated_at(),
    )
    op.create_index("uq_users_email_lower", "users", [sa.text("lower(email)")], unique=True)
    op.create_table(
        "children",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        created_at(), updated_at(),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name_kk", sa.String(255), nullable=False),
        sa.Column("name_ru", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        created_at(),
        sa.UniqueConstraint("slug", name="uq_categories_slug"),
    )
    op.create_table(
        "child_users",
        sa.Column("child_id", sa.Uuid(), sa.ForeignKey("children.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("relationship_type", sa.Enum(
            "parent", "specialist", name="relationship_type",
            native_enum=False, create_constraint=True,
        ), nullable=False),
        created_at(),
    )
    op.create_index("ix_child_users_user_id", "child_users", ["user_id"])
    op.create_table(
        "cards",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("category_id", sa.Uuid(),
                  sa.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title_kk", sa.String(255), nullable=False),
        sa.Column("title_ru", sa.String(255), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("audio_url_kk", sa.Text(), nullable=True),
        sa.Column("audio_url_ru", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        created_at(), updated_at(),
    )
    op.create_index("ix_cards_category_id", "cards", ["category_id"])
    op.create_table(
        "child_cards",
        sa.Column("child_id", sa.Uuid(), sa.ForeignKey("children.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("card_id", sa.Uuid(), sa.ForeignKey("cards.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_favorite", sa.Boolean(), nullable=False, server_default=sa.false()),
        created_at(),
    )
    op.create_index("ix_child_cards_card_id", "child_cards", ["card_id"])


def downgrade() -> None:
    op.drop_index("ix_child_cards_card_id", table_name="child_cards")
    op.drop_table("child_cards")
    op.drop_index("ix_cards_category_id", table_name="cards")
    op.drop_table("cards")
    op.drop_index("ix_child_users_user_id", table_name="child_users")
    op.drop_table("child_users")
    op.drop_table("categories")
    op.drop_table("children")
    op.drop_index("uq_users_email_lower", table_name="users")
    op.drop_table("users")
