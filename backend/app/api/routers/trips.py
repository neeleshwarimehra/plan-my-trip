from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.trip import (
    TripPlanRequest,
    TripPlanResponse,
    TripRecordResponse,
    TripUpdateRequest,
)
from app.services.trip_service import (
    create_trip_plan,
    get_all_trips,
    get_trip_by_id,
    delete_trip,
    update_trip,
)


router = APIRouter(
    prefix="/api/trips",
    tags=["Trips"],
)


@router.post(
    "/plan",
    response_model=TripPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def plan_trip(
    request: TripPlanRequest,
    db: Session = Depends(get_db),
) -> TripPlanResponse:
    return create_trip_plan(request, db)


@router.get(
    "",
    response_model=list[TripRecordResponse],
)
def list_trips(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_all_trips(db, skip, limit)


@router.get(
    "/{trip_id}",
    response_model=TripRecordResponse,
)
def retrieve_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(trip_id, db)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    return trip



@router.patch(
    "/{trip_id}",
    response_model=TripRecordResponse,
)
def modify_trip(
    trip_id: UUID,
    request: TripUpdateRequest,
    db: Session = Depends(get_db),
):
    try:
        trip = update_trip(trip_id, request, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    return trip


@router.delete(
    "/{trip_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = delete_trip(trip_id, db)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    return None