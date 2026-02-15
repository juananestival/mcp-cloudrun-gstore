import asyncio
import logging
import os
from typing import List, Dict, Any, Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Google Store Mock Server �⌚🏠")

# Mock data for Google Store
STORE_PRODUCTS = [
    # Phones
    {
        "id": "p9pxl",
        "category": "phones",
        "name": "Pixel 9 Pro XL",
        "description": "The most powerful Pixel yet, with a pro-level camera and Gemini AI.",
        "price": 1099.00,
        "currency": "USD",
        "specs": ["6.8-inch Super Actua display", "Triple rear camera system", "Tensor G4 chip"]
    },
    {
        "id": "p9p",
        "category": "phones",
        "name": "Pixel 9 Pro",
        "description": "Pro cameras and Gemini AI in a compact size.",
        "price": 999.00,
        "currency": "USD",
        "specs": ["6.3-inch Super Actua display", "Triple rear camera system", "Tensor G4 chip"]
    },
    {
        "id": "p9",
        "category": "phones",
        "name": "Pixel 9",
        "description": "The everyday premium phone with AI-powered helpfulness.",
        "price": 799.00,
        "currency": "USD",
        "specs": ["6.3-inch Actua display", "Advanced dual rear camera", "Tensor G4 chip"]
    },
    {
        "id": "p8a",
        "category": "phones",
        "name": "Pixel 8a",
        "description": "The AI-powered Pixel at an amazing value.",
        "price": 499.00,
        "currency": "USD",
        "specs": ["6.1-inch Actua display", "Tensor G3 chip", "All-day battery"]
    },
    # Earbuds
    {
        "id": "pbp2",
        "category": "earbuds",
        "name": "Pixel Buds Pro 2",
        "description": "The only earbuds engineered for Gemini.",
        "price": 229.00,
        "currency": "USD",
        "features": ["Large 11mm drivers", "Active Noise Cancellation with Silent Seal 2.0", "Built-in Gemini"]
    },
    {
        "id": "pba",
        "category": "earbuds",
        "name": "Pixel Buds A-Series",
        "description": "Rich sound, for less.",
        "price": 99.00,
        "currency": "USD",
        "features": ["Custom-designed 12mm drivers", "Adaptive Sound", "Up to 5 hours of listening time"]
    },
    # Watches
    {
        "id": "pw3",
        "category": "watches",
        "name": "Pixel Watch 3",
        "description": "The first watch with Loss of Pulse Detection.",
        "price": 349.00,
        "currency": "USD",
        "features": ["Advanced health and fitness by Fitbit", "Daily Readiness Score", "Comprehensive heart health tracking"]
    },
    # Activity Trackers
    {
        "id": "fc6",
        "category": "activity trackers",
        "name": "Fitbit Charge 6",
        "description": "Give your routine a routine.",
        "price": 159.00,
        "currency": "USD",
        "features": ["Built-in GPS", "Heart rate tracking", "Stress management tools"]
    },
    {
        "id": "fi3",
        "category": "activity trackers",
        "name": "Fitbit Inspire 3",
        "description": "Do what you love and feel your best.",
        "price": 99.00,
        "currency": "USD",
        "features": ["Up to 10 days of battery", "Active Zone Minutes", "Always-on heart rate"]
    },
    # Smarthome
    {
        "id": "nth4",
        "category": "smarthome",
        "name": "Nest Learning Thermostat (4th gen)",
        "description": "The thermostat that learns from you.",
        "price": 279.00,
        "currency": "USD",
        "features": ["Smart Schedule", "Energy History", "Home/Away Assist"]
    },
    {
        "id": "ndc",
        "category": "smarthome",
        "name": "Nest Doorbell (wired, 2nd gen)",
        "description": "The wired doorbell that knows who’s there.",
        "price": 179.00,
        "currency": "USD",
        "features": ["24/7 continuous video recording", "Intelligent alerts", "Talk and Listen"]
    },
    # Tablets
    {
        "id": "pt",
        "category": "tablets",
        "name": "Pixel Tablet",
        "description": "The tablet that's also the heart of your home.",
        "price": 399.00,
        "currency": "USD",
        "features": ["11-inch screen", "Charging Speaker Dock included", "Chromecast built-in"]
    },
    # Accessories
    {
        "id": "p9pc",
        "category": "accessories",
        "name": "Pixel 9 Pro Case",
        "description": "Designed to protect and look great.",
        "price": 34.99,
        "currency": "USD",
        "colors": ["Obsidian", "Porcelain", "Hazel", "Rose Quartz"]
    }
]

OFFERS = [
    {
        "id": "offer1",
        "title": "Pixel 9 Pro Trade-in",
        "description": "Get up to $760 back with a qualifying trade-in towards Pixel 9 Pro.",
        "expires": "2024-12-31"
    },
    {
        "id": "offer2",
        "title": "Bundle & Save",
        "description": "Save $50 on Pixel Buds Pro 2 when you buy any Pixel 9 series phone.",
        "expires": "2024-11-15"
    }
]

@mcp.tool()
def list_categories() -> List[str]:
    """
    Lists all available product categories in the Google Store.
    
    Returns:
        A list of unique category names.
    """
    logger.info(">>> 🛠️ Tool: 'list_categories' called")
    categories = sorted(list(set(p["category"] for p in STORE_PRODUCTS)))
    return categories

@mcp.tool()
def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Retrieves all products for a specific category.
    
    Args:
        category: The category name (e.g., 'phones', 'watches', 'smarthome').
        
    Returns:
        A list of products in that category.
    """
    logger.info(f">>> 🛠️ Tool: 'get_products_by_category' called for '{category}'")
    return [p for p in STORE_PRODUCTS if p["category"].lower() == category.lower()]


@mcp.tool()
def get_active_offers() -> List[Dict[str, Any]]:
    """
    Retrieves currently active offers and promotions.
    
    Returns:
        A list of active offers.
    """
    logger.info(">>> 🛠️ Tool: 'get_active_offers' called")
    return OFFERS

@mcp.resource("store://products")
def list_all_products() -> str:
    """
    Provides a comprehensive list of all products in the Google Store.
    """
    logger.info(">>> 📚 Resource: 'store://products' accessed")
    output = "# Google Store Product Catalog\n\n"
    for cat in list_categories():
        output += f"## {cat.title()}\n"
        for p in get_products_by_category(cat):
            output += f"- **{p['name']}**: {p['description']} (${p['price']})\n"
        output += "\n"
    return output

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    # Run in HTTP mode for Cloud Run compatibility
    asyncio.run(
        mcp.run_async(
            transport="streamable-http", 
            host="0.0.0.0", 
            port=port
        )
    )