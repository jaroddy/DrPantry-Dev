import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float, Text
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./pantry_manager.db")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PantryItem(Base):
    __tablename__ = "pantry_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    item_name = Column(String(200), nullable=False)
    receipt_name = Column(String(200), nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    days_before_expiry = Column(Integer, nullable=True)
    date_estimated_expiry = Column(DateTime, nullable=True)
    perishable = Column(Boolean, default=True)
    type = Column(String(100), nullable=True)
    units = Column(String(50), nullable=True)
    volume = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    upc = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GlobalKnowledgeItem(Base):
    __tablename__ = "global_knowledge_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(200), nullable=False, unique=True, index=True)
    typical_days_before_expiry = Column(Integer, nullable=True)
    perishable = Column(Boolean, default=True)
    type = Column(String(100), nullable=True)
    typical_units = Column(String(50), nullable=True)
    calories_per_unit = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    usage_count = Column(Integer, default=1)

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    meals = Column(JSON, nullable=False)  # Array of meal objects with dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session_maker() as session:
        yield session
