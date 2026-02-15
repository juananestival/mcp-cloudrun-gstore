import datetime
from typing import Any, List, Dict, Optional

def list_offers(product_category: Optional[str] = None, product_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves a list of current offers from the Google Store, optionally filtered by relevance to a product category or name.
    Offers that have expired based on the current date will not be returned.

    Args:
        product_category (Optional[str]): The category of products the offer might apply to (e.g., "phones", "earbuds").
        product_name (Optional[str]): The name of a product the offer might apply to (e.g., "Pixel 10", "Pixel Buds").

    Returns:
        Dict[str, Any]: A dictionary containing a list of matching, unexpired offers.
    """
    # MOCK: Data updated to reflect active promotions for February 2026
    OFFERS_DATA = [
        {"id": "offer1", "title": "Pixel 10 Pro Discount", "description": "Save $200 on Pixel 10 Pro (Unlocked).", "expires": "2026-02-15"},
        {"id": "offer2", "title": "Pixel 10 Pro XL Discount", "description": "Save $250 on Pixel 10 Pro XL (Unlocked).", "expires": "2026-02-15"},
        {"id": "offer3", "title": "Pixel 10 Discount", "description": "Save $150 on Pixel 10 (Unlocked).", "expires": "2026-02-15"},
        {"id": "offer4", "title": "Pixel 10 Pro Fold Savings", "description": "Save $300 on Pixel 10 Pro Fold (Unlocked).", "expires": "2026-02-15"},
        {"id": "offer5", "title": "Pixel 9a Deal", "description": "Save $100 on Pixel 9a (Unlocked).", "expires": "2026-03-31"},
        {"id": "offer6", "title": "Pixel Buds Pro 2 Sale", "description": "Save $50 on Pixel Buds Pro 2.", "expires": "2026-02-15"},
    ]

    # Get current date from context, with a fallback to today's date
    current_date_str = context.state.get("current_date", datetime.date.today().isoformat())
    
    # FIX: Handle date strings with appended timezone info (e.g., "2026-02-15[America/Los_Angeles]")
    if "[" in current_date_str:
        current_date_str = current_date_str.split("[")[0]
        
    try:
        current_date = datetime.date.fromisoformat(current_date_str)
    except ValueError:
        # Fallback to system date if parsing fails
        current_date = datetime.date.today()

    filtered_offers = []
    for offer in OFFERS_DATA:
        try:
            offer_expires_date = datetime.date.fromisoformat(offer["expires"])
        except ValueError:
            continue

        # Check expiration: Offers valid on the expiration date are included
        if offer_expires_date < current_date:
            continue

        match = True
        if product_category:
            if product_category.lower() not in offer["title"].lower() and product_category.lower() not in offer["description"].lower():
                match = False
        if product_name:
            if product_name.lower() not in offer["title"].lower() and product_name.lower() not in offer["description"].lower():
                match = False

        if match:
            filtered_offers.append(offer)

    if not filtered_offers:
        return {"offers": [], "message": "No current offers found matching your criteria."}
    return {"offers": filtered_offers}