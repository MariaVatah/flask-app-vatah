
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    posted: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    category: Mapped[PostCategory] = mapped_column(
        SQLAlchemyEnum(
            PostCategory,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        nullable=False,
        default=PostCategory.OTHER
    )

    is_active: Mapped[bool | None] = mapped_column(
        Boolean,
        default=True
    )

    author: Mapped[str | None] = mapped_column(
        String(20),
        default="Anonymous"
    )

    def __repr__(self):
        return f"<Post {self.title}>"