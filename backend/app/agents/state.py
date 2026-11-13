from typing import TypedDict, Any


class TravelState(TypedDict, total=False):
    # User trip requirements
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int
    budget: float
    currency: str
    preferences: list[str]

    # Agent outputs
    transportation_options: list[dict[str, Any]]
    hotel_options: list[dict[str, Any]]
    itinerary: list[dict[str, Any]]
    budget_analysis: dict[str, Any]

    # Workflow tracking
    agent_trace: list[str]
    errors: list[str]
    status: str
    final_response: dict[str, Any]