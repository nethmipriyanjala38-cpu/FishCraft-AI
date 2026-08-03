"""
FishCraft AI - Order Builder Tool
Generates a formatted, user-friendly order summary.
"""

from config.settings import FISH_CATALOG

def build_order_summary(order_data: dict) -> str:
    """
    Format the calculated order data into a beautiful text summary.
    
    Args:
        order_data: Output from calculate_order_price()
    """
    if not order_data.get("items"):
        return "Your order is empty or contains invalid items."
        
    lines = ["## 🛒 Your FishCraft Order Summary\n"]
    lines.append("| Item | Qty (Pairs) | Unit Price | Total |")
    lines.append("|------|-------------|------------|-------|")
    
    for item in order_data["items"]:
        # Try to get emoji
        emoji = FISH_CATALOG.get(item["fish_type"], {}).get("emoji", "🐟")
        name = item["name"]
        qty = item["quantity"]
        unit = f"Rs.{item['unit_price']}"
        total = f"Rs.{item['total']:,.2f}"
        
        lines.append(f"| {emoji} {name} | {qty} | {unit} | **{total}** |")
        
    lines.append("\n---")
    lines.append(f"**Subtotal:** Rs.{order_data['subtotal']:,.2f}")
    
    if order_data["discount_applied"]:
        lines.append(f"**Discount (10% bulk):** -Rs.{order_data['discount_amount']:,.2f} 🟢")
        
    if order_data.get("location_provided"):
        lines.append(f"**Delivery Fee:** Rs.{order_data['delivery_fee']:,.2f} 🚚")
        
    lines.append(f"### **Total Amount:** Rs.{order_data['total']:,.2f}")
    
    if not order_data.get("location_provided"):
        lines.append("\n*Note: Delivery fee not included. Standard shipping is Rs.350 (Colombo) or Rs.500 (Outstation). Please provide your location.*")
    
    return "\n".join(lines)
