from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import TIMESTAMP, text

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    category = Column(Integer, server_default="2")
    published = Column(Boolean, server_default="False", nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


