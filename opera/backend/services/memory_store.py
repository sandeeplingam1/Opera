"""Basic memory store for Opera.

This module defines the storage layer for memory items. It uses SQLModel
and SQLite for persistence. The storage API encapsulates basic CRUD
operations for MemoryItem objects.
"""

from contextlib import contextmanager
from typing import Iterable, Optional

from sqlmodel import Session, SQLModel, create_engine, select

from ..models.memory import MemoryItem


# SQLite database file. In a real deployment this could be swapped for
# PostgreSQL or another durable store.
DATABASE_URL = "sqlite:///./opera.db"


engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Initializes the database schema."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterable[Session]:
    """Context manager that yields a SQLModel session and ensures it's closed."""
    with Session(engine) as session:
        yield session


def add_memory(item: MemoryItem) -> MemoryItem:
    """Persist a MemoryItem and return the stored instance."""
    with get_session() as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def list_memories(memory_type: Optional[str] = None) -> list[MemoryItem]:
    """Retrieve memories, optionally filtered by type."""
    with get_session() as session:
        query = select(MemoryItem)
        if memory_type:
            query = query.where(MemoryItem.type == memory_type)
        results = session.exec(query)
        return results.all()


def update_memory(item: MemoryItem) -> MemoryItem:
    """Update an existing MemoryItem."""
    with get_session() as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item