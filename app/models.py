from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.sql import text
from sqlalchemy.types import TIMESTAMP, DateTime, Integer, String, Date, Boolean

from .database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, nullable=False, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(
        String, nullable=True, unique=True
    )  # use either or email or phone number or both can be but must be unique
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)
    birth_date = Column(Date, nullable=False)
    # is_verified = Column(Boolean, server_default=text("false"))
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    # updated_last = Column(DateTime(timezone=True), default=..., nullable=False)


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(
        Integer, autoincrement=True, nullable=False, primary_key=True, unique=True
    )
    content = Column(String, nullable=False)
    username = Column(
        ForeignKey("users.username", name="FK_users_tweets", ondelete="CASCADE"),
        type_=String,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )


# class Message(Base):
#     __tablename__ = "messages"

#     to_user = Column(
#         ForeignKey("users.username", name="FK_users_message", ondelete="CASCADE"),
#         type_=String,
#         nullable=False,
#         primary_key=True,
#     )
#     from_user = Column(
#         ForeignKey("users.username", name="FK_users_message", ondelete="CASCADE"),
#         type_=String,
#         nullable=False,
#         primary_key=True,
#     )
#     message = Column(String, nullable=False)
