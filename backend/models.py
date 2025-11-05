from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# User models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Pantry Item models
class PantryItemBase(BaseModel):
    item_name: str
    receipt_name: Optional[str] = None
    days_before_expiry: Optional[int] = None
    date_estimated_expiry: Optional[datetime] = None
    perishable: bool = True
    type: Optional[str] = None
    units: Optional[str] = None
    volume: Optional[float] = None
    calories: Optional[float] = None
    upc: Optional[str] = None

class PantryItemCreate(PantryItemBase):
    pass

class PantryItemUpdate(BaseModel):
    item_name: Optional[str] = None
    receipt_name: Optional[str] = None
    days_before_expiry: Optional[int] = None
    date_estimated_expiry: Optional[datetime] = None
    perishable: Optional[bool] = None
    type: Optional[str] = None
    units: Optional[str] = None
    volume: Optional[float] = None
    calories: Optional[float] = None
    upc: Optional[str] = None

class PantryItemResponse(PantryItemBase):
    id: int
    user_id: int
    date_added: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Receipt scanning models
class ReceiptScanRequest(BaseModel):
    image_base64: str

class ReceiptItemExtracted(BaseModel):
    receipt_name: str
    quantity: Optional[str] = None

class ReceiptScanResponse(BaseModel):
    items: List[PantryItemResponse]
    message: str

# Meal models
class MealIngredient(BaseModel):
    item_name: str
    quantity: str
    unit: str

class Meal(BaseModel):
    date: str  # ISO date string
    meal_type: str  # breakfast, lunch, dinner, snack
    name: str
    description: Optional[str] = None
    ingredients: List[MealIngredient]
    directions: List[str]
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    servings: Optional[int] = None
    calories: Optional[float] = None

class MealPlanCreate(BaseModel):
    name: str
    description: Optional[str] = None
    meals: List[Meal]

class MealPlanResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    meals: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chat models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    meal_plan: Optional[MealPlanResponse] = None
