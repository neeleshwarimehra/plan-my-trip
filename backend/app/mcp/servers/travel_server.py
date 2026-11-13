
import json
from fastmcp import FastMCP

# Initialize PlanMyTrip MCP Server
mcp = FastMCP("PlanMyTrip Travel Server")


@mcp.tool
def estimate_budget_allocation(
    total_budget: float,
    travelers: int,
    days: int,
    currency: str = "INR",
) -> dict:
    """
    Estimate a trip budget allocation across major travel categories.

    The total budget covers all travelers combined.
    This is an estimate, not a live price quotation.
    """

    if total_budget <= 0:
        raise ValueError("Total budget must be greater than zero.")

    if travelers <= 0:
        raise ValueError("Travelers must be greater than zero.")

    if days <= 0:
        raise ValueError("Days must be greater than zero.")

    percentages = {
        "transportation": 35,
        "accommodation": 30,
        "food": 20,
        "activities": 10,
        "miscellaneous": 5,
    }

    breakdown = {
        category: round(total_budget * percentage / 100, 2)
        for category, percentage in percentages.items()
    }

    return {
        "total_budget": total_budget,
        "travelers": travelers,
        "days": days,
        "budget_per_person": round(total_budget / travelers, 2),
        "daily_budget_per_person": round(
            total_budget / travelers / days, 2
        ),
        "allocation": breakdown,
        "currency": currency,
        "is_estimate": True,
    }


@mcp.tool
def get_destination_research_queries(
    destination: str,
    interests: list[str] | None = None,
) -> dict:
    """
    Generate targeted research queries for a travel destination.

    This tool generates search queries; it does not claim to
    retrieve live destination information.
    """

    if not destination.strip():
        raise ValueError("Destination cannot be empty.")

    interests = interests or [
        "tourist attractions",
        "local food",
        "transportation",
        "popular experiences",
    ]

    queries = [
        f"Best {interest} in {destination}"
        for interest in interests
    ]

    return {
        "destination": destination,
        "research_queries": queries,
        "requires_external_research": True,
    }


@mcp.tool
def get_trip_preparation_checklist(
    destination: str,
    travelers: int,
) -> dict:
    """
    Generate a general preparation checklist for a trip.
    """

    if not destination.strip():
        raise ValueError("Destination cannot be empty.")

    if travelers <= 0:
        raise ValueError("Travelers must be greater than zero.")

    checklist = [
        "Verify transportation schedules and availability.",
        "Compare accommodation prices.",
        "Check destination weather forecasts.",
        "Prepare government-approved identification.",
        "Review local transportation options.",
        "Check applicable entry requirements.",
        "Keep emergency contacts available.",
        "Confirm bookings before departure.",
    ]

    return {
        "destination": destination,
        "travelers": travelers,
        "checklist": checklist,
        "items_count": len(checklist),
    }


if __name__ == "__main__":
    mcp.run()
