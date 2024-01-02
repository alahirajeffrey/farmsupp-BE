# from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, ForeignKey
# import uuid
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# UserBase = declarative_base()
# OtpBase = declarative_base()

# class User(UserBase):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
#     mobile_number = Column(String,  nullable=False)
#     password = Column(String, nullable=False)
#     is_mobile_verified = Column(Boolean, default=False)
#     country_code = Column(String,  nullable=False, default="+234")
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
#     updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

#     articles = relationship("Article", back_populates="author")
#     otp = relationship("Otp", uselist=False, back_populates="user")


# class Otp(OtpBase):
#     __tablename__ = "otp"

#     id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
#     token = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
#     user = relationship("User", back_populates="otp")