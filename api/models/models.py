from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="user")
    ab_tests = relationship("ABTest", back_populates="user")


class Content(Base):
    __tablename__ = "content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    product_info = Column(Text)
    final_content = Column(Text, nullable=False)
    original_draft = Column(Text)
    quality_score = Column(Float)
    critique_notes = Column(Text)
    status = Column(String, default="draft")  # draft, published, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="content")
    metrics = relationship("Metrics", back_populates="content")
    sentiment = relationship("SentimentAnalysis", back_populates="content")
    ab_variants = relationship("ABVariant", back_populates="content")


class ABTest(Base):
    __tablename__ = "ab_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String, default="running")  # running, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ab_tests")
    variants = relationship("ABVariant", back_populates="test")


class ABVariant(Base):
    __tablename__ = "ab_variants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("ab_tests.id"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)
    variant_name = Column(String, nullable=False)  # A, B, C, etc.
    metrics = Column(JSONB, default={})
    
    # Relationships
    test = relationship("ABTest", back_populates="variants")
    content = relationship("Content", back_populates="ab_variants")


class Metrics(Base):
    __tablename__ = "metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)
    platform = Column(String, nullable=False)
    engagement_rate = Column(Float, default=0.0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    roi = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="metrics")


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String)  # positive, neutral, negative
    key_topics = Column(JSONB, default={})
    predicted_reactions = Column(JSONB, default={})
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="sentiment")


class CuratedExample(Base):
    __tablename__ = "curated_examples"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String, nullable=False, index=True)
    text = Column(Text, nullable=False)
    # Note: Vector embeddings will be stored as ARRAY for now
    # For production, use pgvector extension with VECTOR type
    embedding = Column(ARRAY(Float), nullable=True)
    performance_score = Column(Float, default=0.0)
    source_url = Column(String, nullable=True)
    curated_at = Column(DateTime, default=datetime.utcnow)
