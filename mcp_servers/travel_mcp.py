# mcp_servers/travel_mcp.py
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Travel-Core-Infrastructure")

@mcp.tool()
async def search_flights(origin: str, destination: str, date: str) -> Dict[str, Any]:
    """Queries available flights and includes direct booking URLs."""
    print(f"[MCP LOG] Travel API MCP invoked: search_flights from {origin} to {destination}")
    return {
        "status": "SUCCESS",
        "search_parameters": {"origin": origin, "destination": destination, "date": date},
        "options": [
            {"carrier": "IndiGo Airlines", "flight_no": "6E-432", "departure": "08:15", "price_inr": 12500, "type": "Non-stop", "booking_url": "https://www.goindigo.in/"},
            {"carrier": "Air India Express", "flight_no": "IX-991", "departure": "14:30", "price_inr": 11000, "type": "1-stop", "booking_url": "https://www.airindiaexpress.com/"},
            {"carrier": "Vistara Premium", "flight_no": "UK-201", "departure": "10:00", "price_inr": 18500, "type": "Non-stop", "booking_url": "https://www.airvistara.com/"}
        ]
    }

@mcp.tool()
async def recommend_hotels(destination: str, tier: str) -> List[Dict[str, Any]]:
    """Retrieves recommended accommodations with booking affiliate URLs."""
    print(f"[MCP LOG] Travel API MCP invoked: recommend_hotels for {destination} [{tier}]")
    accommodations = {
        "luxury": [
            {"name": "Taj Mahal Palace (or equivalent Taj Property)", "rating": "4.9", "price_per_night_inr": 35000, "amenities": ["Spa", "Pool", "Fine Dining"], "booking_url": "https://www.tajhotels.com/"},
            {"name": "Oberoi Luxury Suites", "rating": "4.8", "price_per_night_inr": 32000, "amenities": ["Ocean View", "Butler Service"], "booking_url": "https://www.oberoihotels.com/"}
        ],
        "moderate": [
            {"name": "Lemon Tree Premier", "rating": "4.4", "price_per_night_inr": 8500, "amenities": ["Free Wi-Fi", "Gym", "Breakfast Included"], "booking_url": "https://www.lemontreehotels.com/"},
            {"name": "Novotel City Centre", "rating": "4.3", "price_per_night_inr": 9200, "amenities": ["Pool", "Business Lounge"], "booking_url": "https://all.accor.com/brands/novotel.en.shtml"}
        ],
        "budget": [
            {"name": "Zostel Backpackers Hub", "rating": "4.5", "price_per_night_inr": 2500, "amenities": ["Laundry", "Shared Lounge", "Free Wi-Fi"], "booking_url": "https://www.zostel.com/"},
            {"name": "Ibis Styles", "rating": "4.1", "price_per_night_inr": 4500, "amenities": ["Breakfast", "Modern Rooms"], "booking_url": "https://all.accor.com/brands/ibisstyles.en.shtml"}
        ]
    }
    return accommodations.get(tier.lower(), accommodations["moderate"])

if __name__ == "__main__":
    mcp.run(transport="stdio")