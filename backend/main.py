from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import timedelta
import uvicorn

from database import init_db, get_db, User
from models import (
    UserCreate, UserLogin, UserResponse, Token,
    PantryItemCreate, PantryItemUpdate, PantryItemResponse,
    ReceiptScanRequest, ReceiptScanResponse,
    MealPlanCreate, MealPlanResponse,
    ChatRequest, ChatResponse
)
from auth import (
    authenticate_user, create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from crud import (
    create_user, create_pantry_item, get_pantry_items, get_pantry_item,
    update_pantry_item, delete_pantry_item, get_global_knowledge_item,
    create_meal_plan, get_meal_plans, get_meal_plan, delete_meal_plan
)
from ocr_service import extract_text_from_image, parse_receipt_items
from chatgpt_service import (
    normalize_item_name, get_item_details, generate_meal_plan,
    chat_with_assistant, extract_last_assistant_message
)

app = FastAPI(
    title="Pantry & Meal Planning Manager API",
    description="Manage your pantry and create meal plans with AI assistance",
    version="1.0.0"
)

# Configure CORS
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    # Validate OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not set. ChatGPT features will not work.")

@app.get("/")
async def root():
    return {
        "message": "Pantry & Meal Planning Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint for monitoring"""
    try:
        # Test database connectivity
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = await create_user(db, user.username, user.password)
    return db_user

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user and return access token"""
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Pantry endpoints
@app.post("/api/pantry", response_model=PantryItemResponse, status_code=201)
async def add_pantry_item(
    item: PantryItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a new item to pantry"""
    # Check global knowledge base first
    knowledge_item = await get_global_knowledge_item(db, item.item_name)
    
    if knowledge_item and not item.days_before_expiry:
        # Use global knowledge to fill in missing data
        item.days_before_expiry = knowledge_item.typical_days_before_expiry
        if not item.type:
            item.type = knowledge_item.type
        if not item.units:
            item.units = knowledge_item.typical_units
    
    return await create_pantry_item(db, current_user.id, item)

@app.get("/api/pantry", response_model=List[PantryItemResponse])
async def list_pantry_items(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all pantry items for current user"""
    return await get_pantry_items(db, current_user.id, skip, limit)

@app.get("/api/pantry/{item_id}", response_model=PantryItemResponse)
async def get_pantry_item_by_id(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific pantry item"""
    item = await get_pantry_item(db, item_id, current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/api/pantry/{item_id}", response_model=PantryItemResponse)
async def update_pantry_item_by_id(
    item_id: int,
    item: PantryItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a pantry item"""
    updated_item = await update_pantry_item(db, item_id, current_user.id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/api/pantry/{item_id}", status_code=204)
async def delete_pantry_item_by_id(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a pantry item"""
    success = await delete_pantry_item(db, item_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

# Receipt scanning endpoint
@app.post("/api/receipt/scan", response_model=ReceiptScanResponse)
async def scan_receipt(
    request: ReceiptScanRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Scan a receipt and add items to pantry"""
    # Extract text from image
    receipt_text = await extract_text_from_image(request.image_base64)
    
    if not receipt_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from image"
        )
    
    # Parse receipt items
    extracted_items = parse_receipt_items(receipt_text)
    
    if not extracted_items:
        raise HTTPException(
            status_code=400,
            detail="Could not find any items in the receipt"
        )
    
    # Process each item
    created_items = []
    for extracted in extracted_items:
        receipt_name = extracted["receipt_name"]
        
        # Normalize item name using ChatGPT
        item_name = await normalize_item_name(receipt_name)
        
        # Check global knowledge base
        knowledge_item = await get_global_knowledge_item(db, item_name)
        
        if knowledge_item:
            # Use existing knowledge
            item_data = PantryItemCreate(
                item_name=item_name,
                receipt_name=receipt_name,
                days_before_expiry=knowledge_item.typical_days_before_expiry,
                perishable=knowledge_item.perishable,
                type=knowledge_item.type,
                units=knowledge_item.typical_units,
                volume=float(extracted.get("quantity", "1")),
                calories=knowledge_item.calories_per_unit
            )
        else:
            # Get details from ChatGPT
            details = await get_item_details(item_name)
            item_data = PantryItemCreate(
                item_name=item_name,
                receipt_name=receipt_name,
                days_before_expiry=details.get("days_before_expiry"),
                perishable=details.get("perishable", True),
                type=details.get("type"),
                units=details.get("typical_units"),
                volume=float(extracted.get("quantity", "1")),
                calories=details.get("calories_per_unit")
            )
        
        # Create pantry item
        db_item = await create_pantry_item(db, current_user.id, item_data)
        created_items.append(db_item)
    
    return {
        "items": created_items,
        "message": f"Successfully added {len(created_items)} items to your pantry"
    }

# Meal plan endpoints
@app.post("/api/meal-plans", response_model=MealPlanResponse, status_code=201)
async def create_new_meal_plan(
    meal_plan: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new meal plan"""
    return await create_meal_plan(db, current_user.id, meal_plan)

@app.get("/api/meal-plans", response_model=List[MealPlanResponse])
async def list_meal_plans(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all meal plans for current user"""
    return await get_meal_plans(db, current_user.id, skip, limit)

@app.get("/api/meal-plans/{meal_plan_id}", response_model=MealPlanResponse)
async def get_meal_plan_by_id(
    meal_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific meal plan"""
    meal_plan = await get_meal_plan(db, meal_plan_id, current_user.id)
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return meal_plan

@app.delete("/api/meal-plans/{meal_plan_id}", status_code=204)
async def delete_meal_plan_by_id(
    meal_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a meal plan"""
    success = await delete_meal_plan(db, meal_plan_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal plan not found")

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with AI assistant for meal planning"""
    # Get user's pantry items for context
    pantry_items = await get_pantry_items(db, current_user.id, limit=100)
    pantry_data = [
        {
            "item_name": item.item_name,
            "type": item.type,
            "volume": item.volume,
            "units": item.units,
            "calories": item.calories,
            "days_before_expiry": item.days_before_expiry
        }
        for item in pantry_items
    ]
    
    # Check if user wants a meal plan
    message_lower = request.message.lower()
    if any(keyword in message_lower for keyword in ["meal plan", "recipe", "cook", "dinner", "lunch", "breakfast"]):
        # Generate meal plan
        meal_plan_data = await generate_meal_plan(
            user_guidelines=request.message,
            pantry_items=pantry_data,
            num_days=7
        )
        
        if meal_plan_data.get("meals"):
            # Save meal plan
            from models import Meal
            from datetime import datetime
            meals = [Meal(**meal) for meal in meal_plan_data["meals"]]
            plan_date = pantry_items[0].date_added.strftime('%Y-%m-%d') if pantry_items else datetime.utcnow().strftime('%Y-%m-%d')
            meal_plan_create = MealPlanCreate(
                name=f"AI Generated Plan - {plan_date}",
                description=request.message,
                meals=meals
            )
            db_meal_plan = await create_meal_plan(db, current_user.id, meal_plan_create)
            
            return ChatResponse(
                response=f"I've created a meal plan for you! It includes {len(meals)} meals. You can view it in your meal plans.",
                meal_plan=db_meal_plan
            )
    
    # Regular chat
    context = {
        "pantry_item_count": len(pantry_items),
        "has_items": len(pantry_items) > 0
    }
    if request.context:
        context.update(request.context)
    
    # Convert conversation history to dict format if provided
    conversation_history_dict = None
    if request.conversation_history:
        conversation_history_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
    
    response_text = await chat_with_assistant(
        request.message, 
        context,
        conversation_history_dict
    )
    return ChatResponse(response=response_text)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
