from database import Base
from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    mobile_number = Column(String,  nullable=False)
    password = Column(String, nullable=False)
    is_mobile_verified = Column(Boolean, default=False)
    country_code = Column(String,  nullable=False, default="+234")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    articles = relationship("Article", back_populates="author")
    otp = relationship("Otp", uselist=False, back_populates="user")


class Otp(Base):
    __tablename__ = "otp"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    user = relationship("User", back_populates="otp")

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    author_id= Column(UUID(as_uuid=True), ForeignKey("users.id"))
    body = Column(String, nullable=False)
    title = Column(String,  nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    author = relationship("User", back_populates="articles")