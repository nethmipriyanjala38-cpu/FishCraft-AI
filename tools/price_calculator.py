"""
FishCraft AI - Price Calculator Tool
Calculates order totals and applies wholesale/bulk discounts.
"""

from config.settings import FISH_CATALOG

def calculate_order_price(items: dict, location: str = "") -> dict:
    """
    Calculate the total price for an order.
    
    Args:
        items: Dictionary mapping fish type (key from FISH_CATALOG) to quantity (pairs)
        location: String representing the delivery location (e.g., "colombo")
        
    Returns:
        Dictionary containing order details, subtotal, discount, and total.
    """
    result_items = []
    subtotal = 0
    total_pairs = 0
    
    for fish_type, quantity in items.items():
        fish_type = fish_type.lower()
        if fish_type in FISH_CATALOG:
            item_price = FISH_CATALOG[fish_type]["price_per_pair"]
            item_total = item_price * quantity
            
            result_items.append({
                "fish_type": fish_type,
                "name": FISH_CATALOG[fish_type]["name"],
                "quantity": quantity,
                "unit_price": item_price,
                "total": item_total
            })
            
            subtotal += item_total
            total_pairs += quantity
            
    # Apply 10% discount for orders of 10 or more pairs
    discount_amount = 0
    discount_applied = False
    
    if total_pairs >= 10:
        discount_amount = subtotal * 0.10
        discount_applied = True
        
    total = subtotal - discount_amount
    
    # Calculate delivery fee
    delivery_fee = 0
    if location:
        if "colombo" in location.lower():
            delivery_fee = 350
        else:
            delivery_fee = 500
            
    final_total = total + delivery_fee
    
    return {
        "items": result_items,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "discount_applied": discount_applied,
        "delivery_fee": delivery_fee,
        "location_provided": bool(location),
        "total": final_total,
        "total_pairs": total_pairs,
        "currency": "LKR"
    }
