from datetime import date, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, func, inspect, select, text
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Base
from app.models import (
    Card, Category, Child, ChildCard, ChildUser, RelationshipType, User, UserRole,
)
from tests.conftest import migrate


def user(email: str = "parent@example.test", role: UserRole = UserRole.PARENT) -> User:
    return User(
        email=email, password_hash="test-only-already-hashed-value",
        full_name="Test User", role=role,
    )


async def graph(session: AsyncSession) -> tuple[User, Child, Category, Card]:
    parent = user()
    child = Child(full_name="Test Child", birth_date=date(2020, 1, 1))
    category = Category(name_kk="Тағам", name_ru="Еда", slug="food")
    card = Card(
        category=category, title_kk="Су", title_ru="Вода", image_url="/cards/water.png",
    )
    session.add_all([parent, child, card])
    await session.flush()
    session.add_all([
        ChildUser(child_id=child.id, user_id=parent.id,
                  relationship_type=RelationshipType.PARENT),
        ChildCard(child_id=child.id, card_id=card.id, sort_order=2, is_favorite=True),
    ])
    await session.commit()
    return parent, child, category, card


def test_user_defaults_and_update_timestamp(run_db):
    async def case(session, engine):
        parent = user()
        session.add(parent)
        await session.commit()
        assert isinstance(parent.id, UUID)
        assert parent.email == "parent@example.test"
        assert parent.role == UserRole.PARENT
        assert parent.is_active is True
        assert parent.password_hash == "test-only-already-hashed-value"
        assert parent.created_at.utcoffset() == timedelta(0)
        original = parent.updated_at
        # A past timestamp makes the assertion independent of clock resolution.
        parent.updated_at = original - timedelta(days=1)
        await session.commit()
        parent.full_name = "Updated User"
        await session.commit()
        await session.refresh(parent)
        assert parent.updated_at >= original

    run_db(case)


@pytest.mark.parametrize("email", ["parent@example.test", "PARENT@EXAMPLE.TEST"])
def test_email_is_unique_case_insensitively(run_db, email):
    async def case(session, engine):
        session.add(user())
        await session.commit()
        session.add(user(email))
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()

    run_db(case)


def test_children_users_and_personalized_cards(run_db):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        second = Child(full_name="Second Child")
        specialists = [user(f"specialist{i}@example.test", UserRole.SPECIALIST) for i in range(2)]
        session.add_all([second, *specialists])
        await session.flush()
        session.add(ChildUser(child_id=second.id, user_id=parent.id,
                              relationship_type=RelationshipType.PARENT))
        for specialist in specialists:
            session.add(ChildUser(child_id=child.id, user_id=specialist.id,
                                  relationship_type=RelationshipType.SPECIALIST))
        await session.commit()
        session.expunge_all()
        loaded = await session.scalar(select(Child).where(Child.id == child.id).options(
            selectinload(Child.user_links).selectinload(ChildUser.user),
            selectinload(Child.card_links).selectinload(ChildCard.card),
        ))
        assert loaded.birth_date == date(2020, 1, 1)
        assert loaded.notes is None
        assert len(loaded.user_links) == 3
        assert {link.user.role for link in loaded.user_links} == {
            UserRole.PARENT, UserRole.SPECIALIST,
        }
        link = loaded.card_links[0]
        assert link.card.title_ru == "Вода"
        assert link.card.is_active is True
        assert link.card.audio_url_kk is None
        assert link.card.audio_url_ru is None
        assert link.sort_order == 2 and link.is_favorite is True
        assert category.sort_order == 0
        assert second.birth_date is None
        parent = await session.scalar(select(User).where(User.id == parent.id).options(
            selectinload(User.child_links)
        ))
        assert len(parent.child_links) == 2
        with pytest.raises(InvalidRequestError):
            _ = link.card.category

    run_db(case)


def test_personalized_card_defaults(run_db):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        second = Child(full_name="Second Child")
        session.add(second)
        await session.flush()
        link = ChildCard(child_id=second.id, card_id=card.id)
        session.add(link)
        await session.commit()
        assert link.sort_order == 0
        assert link.is_favorite is False
        assert link.created_at.utcoffset() == timedelta(0)

    run_db(case)


@pytest.mark.parametrize("loaded", [False, True])
def test_orm_child_deletion_with_loaded_and_unloaded_links(run_db, loaded):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        child_id = child.id
        session.expunge_all()
        statement = select(Child).where(Child.id == child_id)
        if loaded:
            statement = statement.options(
                selectinload(Child.user_links), selectinload(Child.card_links)
            )
        child = await session.scalar(statement)
        await session.delete(child)
        await session.commit()
        for model in (Child, ChildUser, ChildCard):
            count = await session.scalar(select(func.count()).select_from(model))
            assert count == 0
        for model in (User, Card, Category):
            count = await session.scalar(select(func.count()).select_from(model))
            assert count == 1

    run_db(case)


@pytest.mark.parametrize("table", ["child_cards", "child_users", "categories"])
def test_duplicate_associations_and_slug_rejected(run_db, table):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        duplicate = {
            "child_cards": lambda: ChildCard(child_id=child.id, card_id=card.id),
            "child_users": lambda: ChildUser(
                child_id=child.id, user_id=parent.id,
                relationship_type=RelationshipType.SPECIALIST,
            ),
            "categories": lambda: Category(name_kk="Тағам", name_ru="Еда", slug=category.slug),
        }[table]()
        session.add(duplicate)
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()

    run_db(case)


@pytest.mark.parametrize("foreign_key", [
    "card_category", "child_user_child", "child_user_user",
    "child_card_child", "child_card_card",
])
def test_foreign_keys_reject_missing_records(run_db, foreign_key):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        missing = uuid4()
        record = {
            "card_category": lambda: Card(category_id=missing, title_kk="Су",
                                            title_ru="Вода", image_url="/water.png"),
            "child_user_child": lambda: ChildUser(child_id=missing, user_id=parent.id,
                                                    relationship_type=RelationshipType.PARENT),
            "child_user_user": lambda: ChildUser(child_id=child.id, user_id=missing,
                                                   relationship_type=RelationshipType.PARENT),
            "child_card_child": lambda: ChildCard(child_id=missing, card_id=card.id),
            "child_card_card": lambda: ChildCard(child_id=child.id, card_id=missing),
        }[foreign_key]()
        session.add(record)
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()

    run_db(case)


@pytest.mark.parametrize("entity", [User, Child, Card])
def test_database_delete_cascades_preserve_other_entities(run_db, entity):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        ids = {User: parent.id, Child: child.id, Card: card.id}
        await session.execute(delete(entity).where(entity.id == ids[entity]))
        await session.commit()
        for model in (User, Child, Card):
            count = await session.scalar(select(func.count()).select_from(model))
            assert count == (0 if model is entity else 1)
        for model, removed in (
            (ChildUser, entity in (User, Child)),
            (ChildCard, entity in (Child, Card)),
        ):
            assert await session.scalar(select(func.count()).select_from(model)) == (0 if removed else 1)
        assert await session.scalar(select(func.count()).select_from(Category)) == 1

    run_db(case)


def test_category_with_cards_cannot_be_deleted(run_db):
    async def case(session, engine):
        parent, child, category, card = await graph(session)
        category_id, card_id = category.id, card.id
        with pytest.raises(IntegrityError):
            await session.execute(
                delete(Category).where(Category.id == category_id)
            )
        await session.rollback()
        await session.execute(delete(Card).where(Card.id == card_id))
        await session.execute(
            delete(Category).where(Category.id == category_id)
        )
        await session.commit()

    run_db(case)


@pytest.mark.parametrize("table,column", [
    ("users", "role"), ("child_users", "relationship_type"),
])
def test_role_constraints(run_db, table, column):
    async def case(session, engine):
        await graph(session)
        with pytest.raises(IntegrityError):
            await session.execute(text(f"UPDATE {table} SET {column} = 'invalid'"))
        await session.rollback()

    run_db(case)


def test_migration_upgrade_downgrade_and_reapply(run_db):
    async def case(session, engine):
        expected = {"users", "children", "child_users", "categories", "cards", "child_cards"}
        assert set(Base.metadata.tables) == expected
        async with engine.begin() as connection:
            tables = await connection.run_sync(lambda sync: set(inspect(sync).get_table_names()))
            assert tables == expected | {"alembic_version"}
            assert await connection.scalar(text("SELECT version_num FROM alembic_version")) == "0002"
            await connection.run_sync(lambda sync: migrate(sync, "0001", downgrade=True))
            tables = await connection.run_sync(lambda sync: set(inspect(sync).get_table_names()))
            assert tables == {"alembic_version"}
            assert await connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
            await connection.run_sync(lambda sync: migrate(sync, "head"))
            from alembic.autogenerate import compare_metadata
            from alembic.migration import MigrationContext

            differences = await connection.run_sync(lambda sync: compare_metadata(
                MigrationContext.configure(sync, opts={"compare_type": True}), Base.metadata
            ))
            assert differences == []
        await graph(session)

    run_db(case)
