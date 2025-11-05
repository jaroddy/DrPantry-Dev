import base64
import io
import re
from typing import List, Dict
from PIL import Image
import pytesseract

async def extract_text_from_image(image_base64: str) -> str:
    """Extract text from base64 encoded image using OCR"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(image_base64.split(',')[-1])
        image = Image.open(io.BytesIO(image_data))
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def parse_receipt_items(receipt_text: str) -> List[Dict[str, str]]:
    """Parse receipt text to extract item names and quantities"""
    items = []
    lines = receipt_text.split('\n')
    
    # Simple pattern matching for receipt items
    # This is a basic implementation; real-world would need more sophisticated parsing
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Skip common receipt headers/footers
        skip_terms = ['total', 'subtotal', 'tax', 'change', 'cash', 'credit', 
                      'debit', 'thank you', 'receipt', 'store', 'date', 'time']
        if any(term in line.lower() for term in skip_terms):
            continue
        
        # Look for items (simple heuristic: lines with letters and possibly numbers/prices)
        if re.search(r'[a-zA-Z]{3,}', line):
            # Try to extract price at end
            price_match = re.search(r'\$?\d+\.\d{2}$', line)
            if price_match:
                item_name = line[:price_match.start()].strip()
            else:
                item_name = line
            
            # Try to extract quantity
            qty_match = re.search(r'^(\d+)x?\s+', item_name, re.IGNORECASE)
            quantity = "1"
            if qty_match:
                quantity = qty_match.group(1)
                item_name = item_name[qty_match.end():].strip()
            
            if item_name and len(item_name) > 2:
                items.append({
                    "receipt_name": item_name,
                    "quantity": quantity
                })
    
    return items
