from uuid import uuid4

from app.schemas.trip import TripPlanRequest, TripPlanResponse


def create_trip_plan(request: TripPlanRequest) -> TripPlanResponse:
    budget_per_person = round(
        request.budget / request.travelers, 2
    )

    summary = (
        f"Trip from {request.origin} to {request.destination} "
        f"for {request.travelers} traveler(s), "
        f"with a total budget of {request.currency} "
        f"{request.budget:,.2f}."
    )

    return TripPlanResponse(
        trip_id=str(uuid4()),
        status="draft",
        summary=summary,
        request=request,
        estimated_budget_per_person=budget_per_person,
        next_steps=[
            "Search available transportation options.",
            "Compare hotels and accommodation.",
            "Generate a day-wise travel itinerary.",
            "Optimize the trip within your budget.",
        ],
    )
