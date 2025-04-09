from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String,Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON


class Sentiment(Base):
    __tablename__='sentiments'

    id = Column(Integer, primary_key=True, nullable=False)
    sentiments = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recommendation = Column(JSON, nullable=True)  # 🔥 Save full recommendation dict



    owner = relationship("Users")

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))