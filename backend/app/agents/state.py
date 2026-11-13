
from typing import TypedDict, Any, Annotated
import operator


class TravelState(TypedDict, total=False):
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int
    budget: float
    currency: str
    preferences: list[str]

    plan_details: dict[str, Any]
    budget_analysis: dict[str, Any]
    summary: str
    next_steps: list[str]

    agent_trace: Annotated[list[str], operator.add]
    errors: list[str]
    status: str
    final_response: dict[str, Any]
