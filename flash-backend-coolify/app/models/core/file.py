from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    unique_filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    storage_type = Column(String(50), nullable=False)  # 'local' or 'b2'
    mime_type = Column(String(120), nullable=False)
    size = Column(BigInteger, nullable=True)
    
    # Optional: Link to user who uploaded it
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
