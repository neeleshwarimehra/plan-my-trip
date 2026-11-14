
from uuid import uuid4, UUID

from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.schemas.trip import TripPlanRequest, TripPlanResponse
# from app.agents.graph import travel_graph



def create_trip_plan(
    request: TripPlanRequest,
    db: Session,
) -> TripPlanResponse:
   
    from app.agents.graph import travel_graph

    graph_result = travel_graph.invoke({
        "origin": request.origin,
        "destination": request.destination,
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat(),
        "travelers": request.travelers,
        "budget": request.budget,
        "currency": request.currency,
        "preferences": request.preferences,
        "agent_trace": [],
    })

    if graph_result.get("status") != "completed":
        raise ValueError(
            str(graph_result.get("errors", ["Trip planning failed."]))
        )

    result = graph_result["final_response"]

    budget_per_person = (
        result["budget_analysis"]["budget_per_person"]
    )

    trip = Trip(
        id=uuid4(),
        origin=request.origin,
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        travelers=request.travelers,
        budget=request.budget,
        currency=request.currency,
        preferences=request.preferences,
        status="planned",
        summary=result["summary"],
        estimated_budget_per_person=budget_per_person,
        next_steps=result["next_steps"],
        plan_details={
            **result["plan_details"],
            "budget_analysis": result["budget_analysis"],
            "agent_trace": graph_result.get("agent_trace", []),
        },
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return TripPlanResponse(
        trip_id=str(trip.id),
        status="planned",
        summary=trip.summary,
        request=request,
        estimated_budget_per_person=budget_per_person,
        next_steps=trip.next_steps,
        plan_details=trip.plan_details,
    )



def get_all_trips(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[Trip]:
    return (
        db.query(Trip)
        .order_by(Trip.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_trip_by_id(
    trip_id: UUID,
    db: Session,
) -> Trip | None:
    return db.query(Trip).filter(
        Trip.id == trip_id
    ).first()


def delete_trip(
    trip_id: UUID,
    db: Session,
) -> bool:
    trip = get_trip_by_id(trip_id, db)

    if trip is None:
        return False

    db.delete(trip)
    db.commit()

    return True



def update_trip(
    trip_id: UUID,
    request,
    db: Session,
) -> Trip | None:

    trip = get_trip_by_id(trip_id, db)

    if trip is None:
        return None

    updates = request.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(trip, field, value)

    # Validate the complete trip after applying partial updates.
    if trip.origin.strip().casefold() == trip.destination.strip().casefold():
        raise ValueError("Origin and destination must be different.")

    if trip.end_date < trip.start_date:
        raise ValueError("End date must be on or after start date.")

    # Recalculate budget per person.
    trip.estimated_budget_per_person = round(
        float(trip.budget) / trip.travelers, 2
    )

    # Regenerate summary.
    trip.summary = (
        f"Trip from {trip.origin} to {trip.destination} "
        f"for {trip.travelers} traveler(s), "
        f"with a total budget of {trip.currency} "
        f"{float(trip.budget):,.2f}."
    )

    db.commit()
    db.refresh(trip)

    return trip