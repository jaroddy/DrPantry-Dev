import os
import json
from typing import List, Dict, Any, Optional

# Initialize OpenAI client (lazy loaded to avoid initialization errors)
_client = None

def get_client():
    global _client
    if _client is None:
        from openai import AsyncOpenAI
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set. ChatGPT features will not work.")
        _client = AsyncOpenAI(api_key=api_key)
    return _client

async def normalize_item_name(receipt_name: str) -> str:
    """Convert receipt name to a normalized item name using GPT"""
    try:
        client = get_client()
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that converts receipt item names into clean, general food item names. Return only the normalized name, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Convert this receipt item to a general food name: {receipt_name}"
                }
            ],
            temperature=0.3,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error normalizing item name: {e}")
        return receipt_name

async def get_item_details(item_name: str) -> Dict[str, Any]:
    """Get detailed information about a food item using GPT"""
    try:
        client = get_client()
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a food expert. Provide detailed information about food items in JSON format.
                    Return a JSON object with these fields:
                    - days_before_expiry: typical days until expiry (integer)
                    - perishable: true/false
                    - type: category like "fruit", "vegetable", "dairy", "meat", "grain", etc.
                    - typical_units: common unit like "piece", "lb", "oz", "kg", etc.
                    - calories_per_unit: approximate calories per unit (float)
                    """
                },
                {
                    "role": "user",
                    "content": f"Provide details for: {item_name}"
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error getting item details: {e}")
        return {
            "days_before_expiry": 7,
            "perishable": True,
            "type": "unknown",
            "typical_units": "piece",
            "calories_per_unit": 100
        }

async def generate_sql_query(user_request: str, pantry_items: List[Dict[str, Any]]) -> str:
    """Generate SQL query based on user's meal planning request"""
    try:
        client = get_client()
        pantry_summary = "\n".join([
            f"- {item['item_name']} ({item.get('type', 'unknown')}, {item.get('volume', '?')} {item.get('units', 'units')})"
            for item in pantry_items[:20]  # Limit to avoid token limits
        ])
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a SQL expert. Generate SQLite SELECT queries for a pantry_items table.
                    The table has columns: item_name, type, units, volume, calories, perishable, days_before_expiry.
                    Return ONLY the SQL query, nothing else."""
                },
                {
                    "role": "user",
                    "content": f"User request: {user_request}\n\nAvailable items:\n{pantry_summary}\n\nGenerate a SQL query to find matching items."
                }
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return "SELECT * FROM pantry_items LIMIT 10"

async def generate_meal_plan(
    user_guidelines: str,
    pantry_items: List[Dict[str, Any]],
    num_days: int = 7
) -> Dict[str, Any]:
    """Generate a meal plan based on user guidelines and available pantry items"""
    try:
        client = get_client()
        pantry_summary = "\n".join([
            f"- {item['item_name']}: {item.get('volume', '1')} {item.get('units', 'unit(s)')}"
            for item in pantry_items[:30]
        ])
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using 3.5-turbo for cost optimization
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a meal planning expert. Create a {num_days}-day meal plan in JSON format.
                    Return a JSON object with a "meals" array. Each meal should have:
                    - date: ISO date string
                    - meal_type: "breakfast", "lunch", or "dinner"
                    - name: meal name
                    - description: brief description
                    - ingredients: array of {{item_name, quantity, unit}}
                    - directions: array of step-by-step instructions
                    - prep_time: e.g., "15 minutes"
                    - cook_time: e.g., "30 minutes"
                    - servings: number of servings
                    - calories: estimated total calories
                    
                    Prioritize using the available pantry items."""
                },
                {
                    "role": "user",
                    "content": f"""Create a meal plan with these guidelines: {user_guidelines}
                    
Available pantry items:
{pantry_summary}

Generate a {num_days}-day meal plan."""
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error generating meal plan: {e}")
        return {"meals": []}

async def chat_with_assistant(
    message: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """General chat interface for the assistant"""
    try:
        client = get_client()
        messages = [
            {
                "role": "system",
                "content": """You are a helpful pantry and meal planning assistant. 
                You help users manage their food inventory and create meal plans.
                Be concise and helpful."""
            }
        ]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"Context: {json.dumps(context)}"
            })
        
        messages.append({
            "role": "user",
            "content": message
        })
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in chat: {e}")
        return "I'm sorry, I encountered an error. Please try again."
