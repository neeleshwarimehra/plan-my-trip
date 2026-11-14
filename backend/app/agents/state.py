from operator import add
from typing import Annotated, TypedDict, Any


class TravelState(TypedDict, total=False):
    # Trip requirements
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int
    budget: float
    currency: str
    preferences: list[str]

    # Workflow status
    status: str
    errors: list[str]

    # Agent outputs
    plan_details: dict[str, Any]
    destination_research: Any
    budget_analysis: dict[str, Any]
    mcp_budget_allocation: dict[str, Any]

    # Final response
    summary: str
    next_steps: list[str]
    preparation_checklist: Any
    final_response: dict[str, Any]

    # Accumulate agent execution history
    agent_trace: Annotated[list[str], add]
