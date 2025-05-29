# models.py
from datetime import datetime
from sqlalchemy import Column, String, Text, TIMESTAMP, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class RawArticle(Base):
    __tablename__ = "osint_raw"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    content_html = Column(Text, nullable=True)
    url = Column(Text, unique=True, nullable=False)
    published_at = Column(TIMESTAMP(timezone=True), nullable=True)
    collected_at = Column(TIMESTAMP(timezone=True), nullable=False)
    source_type = Column(String, nullable=False)
    feed_name = Column(String, nullable=False)
    reliability = Column(String, nullable=True)
    raw_payload = Column(JSON, nullable=True)
    tsv = Column(TSVECTOR)
