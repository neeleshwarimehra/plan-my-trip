from app.agents.state import TravelState


def supervisor_agent(state: TravelState) -> dict:
    """Validate trip requirements before starting the workflow."""

    required_fields = [
        "origin",
        "destination",
        "start_date",
        "end_date",
        "travelers",
        "budget",
    ]

    missing_fields = [
        field for field in required_fields
        if not state.get(field)
    ]

    if missing_fields:
        return {
            "status": "failed",
            "errors": [
                f"Missing required fields: {', '.join(missing_fields)}"
            ],
            "agent_trace": ["supervisor_agent"],
        }

    return {
        "status": "processing",
        "errors": [],
        "agent_trace": ["supervisor_agent"],
    }


def transportation_agent(state: TravelState) -> dict:
    """Prepare transportation search requirements."""

    return {
        "transportation_options": [],
        "agent_trace": ["transportation_agent"],
    }


def hotel_agent(state: TravelState) -> dict:
    """Prepare accommodation search requirements."""

    return {
        "hotel_options": [],
        "agent_trace": ["hotel_agent"],
    }


def itinerary_agent(state: TravelState) -> dict:
    """Prepare itinerary generation requirements."""

    return {
        "itinerary": [],
        "agent_trace": ["itinerary_agent"],
    }


def budget_agent(state: TravelState) -> dict:
    """Calculate the available budget per traveler."""

    travelers = state.get("travelers", 1)
    budget = state.get("budget", 0)

    budget_per_person = (
        round(budget / travelers, 2)
        if travelers > 0
        else 0
    )

    return {
        "budget_analysis": {
            "total_budget": budget,
            "travelers": travelers,
            "budget_per_person": budget_per_person,
            "currency": state.get("currency", "INR"),
        },
        "agent_trace": ["budget_agent"],
    }


def final_response_agent(state: TravelState) -> dict:
    """Prepare the initial workflow response."""

    return {
        "status": "completed",
        "final_response": {
            "destination": state["destination"],
            "budget_analysis": state.get("budget_analysis", {}),
            "transportation_options": state.get(
                "transportation_options", []
            ),
            "hotel_options": state.get("hotel_options", []),
            "itinerary": state.get("itinerary", []),
        },
        "agent_trace": ["final_response_agent"],
    }