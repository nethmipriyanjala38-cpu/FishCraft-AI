"""
FishCraft AI - Stock Checker Tool
Provides agents with current stock availability.
"""

from config.settings import FISH_CATALOG

def check_stock(fish_type: str = None) -> dict:
    """
    Check stock availability for a specific fish type or all fish.
    
    Args:
        fish_type: Optional fish type key to check. If None, returns all.
        
    Returns:
        Dictionary mapping fish names to their available stock and details.
    """
    if fish_type and fish_type.lower() in FISH_CATALOG:
        ft = fish_type.lower()
        return {
            ft: {
                "name": FISH_CATALOG[ft]["name"],
                "stock": FISH_CATALOG[ft]["stock"],
                "price": FISH_CATALOG[ft]["price_per_pair"],
                "status": "In Stock" if FISH_CATALOG[ft]["stock"] > 0 else "Out of Stock"
            }
        }
        
    # Return all if none specified or not found
    result = {}
    for key, data in FISH_CATALOG.items():
        result[key] = {
            "name": data["name"],
            "stock": data["stock"],
            "price": data["price_per_pair"],
            "status": "In Stock" if data["stock"] > 0 else "Out of Stock"
        }
        
    return result
