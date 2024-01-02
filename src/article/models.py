from src.database import Base
from sqlalchemy import ForeignKey, Column, String, TIMESTAMP, text
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    author_id= Column(UUID(as_uuid=True), ForeignKey("users.id"))
    body = Column(String, nullable=False)
    title = Column(String,  nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    author = relationship("User", back_populates="articles")
