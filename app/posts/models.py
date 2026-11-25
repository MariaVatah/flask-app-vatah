from datetime import datetime
from enum import Enum

from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(
        db.Enum(PostCategory),
        nullable=False,
        default=PostCategory.OTHER
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    author = db.Column(
        db.String(20),
        default="Anonymous"
    )

    def __repr__(self):
        return f"<Post {self.title}>"