import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("TravelToolsServer")

AVIATION_API_KEY = os.getenv("AVIATION_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


@mcp.tool()
async def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    passengers: int = 1,
) -> dict:
    """Search live flights between origin and destination using Aviationstack."""
    if not AVIATION_API_KEY:
        return {"status": "skipped", "message": "AVIATION_API_KEY not set", "flights": []}

    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATION_API_KEY,
        "dep_iata": origin.strip().upper()[:3],
        "arr_iata": destination.strip().upper()[:3],
        "limit": 5,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            flights = [
                {
                    "airline": item.get("airline", {}).get("name"),
                    "flight_number": item.get("flight", {}).get("iata"),
                    "departure": item.get("departure", {}).get("scheduled"),
                    "arrival": item.get("arrival", {}).get("scheduled"),
                    "status": item.get("flight_status"),
                }
                for item in data.get("data", [])
            ]
            return {"status": "success", "passengers": passengers, "flights": flights}
        except Exception as e:
            return {"status": "error", "message": str(e), "flights": []}


@mcp.tool()
async def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    budget_per_night: float | None = None,
) -> dict:
    """Search live hotel options and rates at the destination using Tavily."""
    if not TAVILY_API_KEY:
        return {"status": "skipped", "message": "TAVILY_API_KEY not set", "hotels": []}

    budget_clause = f" under {budget_per_night} per night" if budget_per_night else ""
    query = f"best hotels in {destination} from {check_in} to {check_out}{budget_clause} rates reviews"

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5,
                },
            )
            resp.raise_for_status()
            results = resp.json().get("results", [])
            hotels = [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("content"),
                }
                for r in results
            ]
            return {"status": "success", "hotels": hotels}
        except Exception as e:
            return {"status": "error", "message": str(e), "hotels": []}


@mcp.tool()
async def get_destination_research_queries(
    destination: str,
    interests: list[str] | None = None,
) -> dict:
    """Generate destination research queries and fetch live Tavily destination highlights."""
    interest_str = ", ".join(interests) if interests else "sightseeing, local food, culture"
    queries = [
        f"top things to do in {destination} for {interest_str}",
        f"best local neighborhoods and transport tips in {destination}",
        f"estimated daily travel expenses in {destination}",
    ]

    highlights = []
    if TAVILY_API_KEY:
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                resp = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": TAVILY_API_KEY,
                        "query": f"top travel attractions and tips in {destination} {interest_str}",
                        "search_depth": "basic",
                        "max_results": 4,
                    },
                )
                resp.raise_for_status()
                highlights = [
                    {"title": r.get("title"), "snippet": r.get("content")}
                    for r in resp.json().get("results", [])
                ]
            except Exception:
                highlights = []

    return {
        "destination": destination,
        "interests": interests or [],
        "queries": queries,
        "live_highlights": highlights,
    }


@mcp.tool()
async def estimate_budget_allocation(
    total_budget: float,
    travelers: int,
    days: int,
    currency: str = "INR",
) -> dict:
    """Deterministically allocate trip budget across core travel categories."""
    safe_days = max(days, 1)
    safe_travelers = max(travelers, 1)

    allocation = {
        "transportation": round(total_budget * 0.30, 2),
        "accommodation": round(total_budget * 0.35, 2),
        "food": round(total_budget * 0.18, 2),
        "activities": round(total_budget * 0.12, 2),
        "miscellaneous": round(total_budget * 0.05, 2),
    }

    budget_per_person = round(total_budget / safe_travelers, 2)
    daily_budget_per_person = round(budget_per_person / safe_days, 2)

    return {
        "total_budget": total_budget,
        "travelers": safe_travelers,
        "days": safe_days,
        "budget_per_person": budget_per_person,
        "daily_budget_per_person": daily_budget_per_person,
        "currency": currency,
        "allocation": allocation,
        "is_estimate": True,
    }


@mcp.tool()
async def get_trip_preparation_checklist(
    destination: str,
    travelers: int = 1,
) -> dict:
    """Return a structured pre-trip preparation checklist for the destination."""
    return {
        "destination": destination,
        "travelers": travelers,
        "documents": [
            "Government-issued photo ID / Passport (valid for 6+ months)",
            "Confirmed flight/train tickets and hotel booking vouchers",
            "Travel insurance policy details",
        ],
        "essentials": [
            "Universal power adapter and portable power bank",
            "Personal medications and basic first-aid kit",
            "Weather-appropriate clothing and comfortable walking shoes",
        ],
        "finance_and_connectivity": [
            "Notify bank / enable international or domestic UPI/card limits",
            f"Download offline maps and local transit apps for {destination}",
        ],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")