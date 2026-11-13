from datetime import date
from typing import Literal
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict, Field, model_validator


class TripPlanRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=100)
    destination: str = Field(min_length=2, max_length=100)
    start_date: date
    end_date: date
    travelers: int = Field(default=1, ge=1, le=20)
    budget: float = Field(gt=0)
    currency: str = "INR"
    preferences: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_trip(self):
        if self.origin.strip().casefold() == self.destination.strip().casefold():
            raise ValueError("Origin and destination must be different.")

        if self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date.")

        return self


class TripPlanResponse(BaseModel):
    trip_id: str
    status: str
    summary: str
    request: TripPlanRequest
    estimated_budget_per_person: float
    next_steps: list[str]
    plan_details: dict
    


class TripRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    origin: str
    destination: str
    start_date: date
    end_date: date
    travelers: int
    budget: float
    currency: str
    preferences: list[str]
    status: str
    summary: str
    estimated_budget_per_person: float
    next_steps: list[str]
    created_at: datetime
    updated_at: datetime
    plan_details: dict

class TripUpdateRequest(BaseModel):
    origin: str | None = Field(default=None, min_length=2, max_length=100)
    destination: str | None = Field(default=None, min_length=2, max_length=100)
    start_date: date | None = None
    end_date: date | None = None
    travelers: int | None = Field(default=None, ge=1, le=20)
    budget: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    preferences: list[str] | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_null_values(cls, values):
        if isinstance(values, dict):
            if not values:
                raise ValueError("At least one field must be provided.")
            if any(value is None for value in values.values()):
                raise ValueError("Fields cannot be null.")
        return values

    @model_validator(mode="after")
    def validate_trip(self):
        if (
            self.origin is not None
            and self.destination is not None
            and self.origin.strip().casefold()
            == self.destination.strip().casefold()
        ):
            raise ValueError("Origin and destination must be different.")

        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("End date must be on or after start date.")

        return self