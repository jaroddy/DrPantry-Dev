from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from database import User, PantryItem, GlobalKnowledgeItem, MealPlan
from models import (
    PantryItemCreate, PantryItemUpdate, 
    MealPlanCreate
)
from auth import get_password_hash

# User CRUD
async def create_user(db: AsyncSession, username: str, password: str) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Pantry Item CRUD
async def create_pantry_item(
    db: AsyncSession, 
    user_id: int, 
    item: PantryItemCreate
) -> PantryItem:
    """Create a new pantry item"""
    # Calculate expiry date if days_before_expiry is provided
    date_estimated_expiry = None
    if item.days_before_expiry:
        date_estimated_expiry = datetime.utcnow() + timedelta(days=item.days_before_expiry)
    
    db_item = PantryItem(
        user_id=user_id,
        item_name=item.item_name,
        receipt_name=item.receipt_name,
        days_before_expiry=item.days_before_expiry,
        date_estimated_expiry=date_estimated_expiry or item.date_estimated_expiry,
        perishable=item.perishable,
        type=item.type,
        units=item.units,
        volume=item.volume,
        calories=item.calories,
        upc=item.upc
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    
    # Update global knowledge base
    await update_global_knowledge(db, item.item_name, item)
    
    return db_item

async def get_pantry_items(
    db: AsyncSession, 
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[PantryItem]:
    """Get all pantry items for a user"""
    result = await db.execute(
        select(PantryItem)
        .where(PantryItem.user_id == user_id)
        .order_by(PantryItem.date_added.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_pantry_item(
    db: AsyncSession, 
    item_id: int, 
    user_id: int
) -> Optional[PantryItem]:
    """Get a specific pantry item"""
    result = await db.execute(
        select(PantryItem)
        .where(PantryItem.id == item_id, PantryItem.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_pantry_item(
    db: AsyncSession,
    item_id: int,
    user_id: int,
    item: PantryItemUpdate
) -> Optional[PantryItem]:
    """Update a pantry item"""
    db_item = await get_pantry_item(db, item_id, user_id)
    if db_item is None:
        return None
    
    update_data = item.model_dump(exclude_unset=True)
    
    # Recalculate expiry date if days_before_expiry changed
    if "days_before_expiry" in update_data and update_data["days_before_expiry"]:
        update_data["date_estimated_expiry"] = datetime.utcnow() + timedelta(
            days=update_data["days_before_expiry"]
        )
    
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_pantry_item(
    db: AsyncSession, 
    item_id: int, 
    user_id: int
) -> bool:
    """Delete a pantry item"""
    db_item = await get_pantry_item(db, item_id, user_id)
    if db_item is None:
        return False
    
    await db.delete(db_item)
    await db.commit()
    return True

# Global Knowledge CRUD
async def get_global_knowledge_item(
    db: AsyncSession, 
    item_name: str
) -> Optional[GlobalKnowledgeItem]:
    """Get a global knowledge item by name"""
    result = await db.execute(
        select(GlobalKnowledgeItem)
        .where(GlobalKnowledgeItem.item_name == item_name)
    )
    return result.scalar_one_or_none()

async def update_global_knowledge(
    db: AsyncSession,
    item_name: str,
    item_data: PantryItemCreate
):
    """Update or create global knowledge item"""
    existing = await get_global_knowledge_item(db, item_name)
    
    if existing:
        # Increment usage count
        existing.usage_count += 1
        await db.commit()
    else:
        # Create new global knowledge entry
        db_knowledge = GlobalKnowledgeItem(
            item_name=item_name,
            typical_days_before_expiry=item_data.days_before_expiry,
            perishable=item_data.perishable,
            type=item_data.type,
            typical_units=item_data.units,
            calories_per_unit=item_data.calories / item_data.volume if item_data.calories and item_data.volume else None
        )
        db.add(db_knowledge)
        await db.commit()

# Meal Plan CRUD
async def create_meal_plan(
    db: AsyncSession,
    user_id: int,
    meal_plan: MealPlanCreate
) -> MealPlan:
    """Create a new meal plan"""
    meals_data = [meal.model_dump() for meal in meal_plan.meals]
    
    db_meal_plan = MealPlan(
        user_id=user_id,
        name=meal_plan.name,
        description=meal_plan.description,
        meals=meals_data
    )
    db.add(db_meal_plan)
    await db.commit()
    await db.refresh(db_meal_plan)
    return db_meal_plan

async def get_meal_plans(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[MealPlan]:
    """Get all meal plans for a user"""
    result = await db.execute(
        select(MealPlan)
        .where(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_meal_plan(
    db: AsyncSession,
    meal_plan_id: int,
    user_id: int
) -> Optional[MealPlan]:
    """Get a specific meal plan"""
    result = await db.execute(
        select(MealPlan)
        .where(MealPlan.id == meal_plan_id, MealPlan.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def delete_meal_plan(
    db: AsyncSession,
    meal_plan_id: int,
    user_id: int
) -> bool:
    """Delete a meal plan"""
    db_meal_plan = await get_meal_plan(db, meal_plan_id, user_id)
    if db_meal_plan is None:
        return False
    
    await db.delete(db_meal_plan)
    await db.commit()
    return True
