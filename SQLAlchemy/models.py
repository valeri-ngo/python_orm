from typing import List, Optional

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)

class Base(DeclarativeBase):    # equivalent of models.Model
    pass

class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(Text)
    instructions: Mapped[str] = mapped_column(Text)
    chef_id: Mapped[Optional[int]] = mapped_column(ForeignKey('chefs.id'))
    chef: Mapped[Optional["Chef"]] = relationship(
        back_populates="recipes"
    )

class Chef(Base):
    __tablename__ = 'chefs'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    recipes: Mapped[List["Recipe"]] = relationship(
        back_populates="chef"
    )