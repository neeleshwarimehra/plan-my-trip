
import json
from datetime import date

from app.agents.state import TravelState
from app.core.llm import get_llm
from app.mcp.client import call_travel_mcp_tool


def supervisor_agent(state: TravelState) -> dict:
    """
    Validate trip requirements before starting the workflow.
    """

    required = [
        "origin",
        "destination",
        "start_date",
        "end_date",
        "travelers",
        "budget",
    ]

    missing = [
        field
        for field in required
        if state.get(field) is None
    ]

    if missing:
        return {
            "status": "failed",
            "errors": [
                f"Missing fields: {', '.join(missing)}"
            ],
            "agent_trace": ["supervisor_agent"],
        }

    if state["travelers"] < 1 or state["budget"] <= 0:
        return {
            "status": "failed",
            "errors": ["Invalid travelers or budget."],
            "agent_trace": ["supervisor_agent"],
        }

    start = date.fromisoformat(state["start_date"])
    end = date.fromisoformat(state["end_date"])

    if end < start:
        return {
            "status": "failed",
            "errors": ["End date cannot be before start date."],
            "agent_trace": ["supervisor_agent"],
        }

    return {
        "status": "processing",
        "agent_trace": ["supervisor_agent"],
    }


async def planner_agent(state: TravelState) -> dict:
    """
    Generate an itinerary using Groq and destination research MCP.
    """

    destination = state["destination"]

    research_result = await call_travel_mcp_tool(
        "get_destination_research_queries",
        {
            "destination": destination,
            "interests": state.get("preferences") or None,
        },
    )

    llm = get_llm()

    prompt = f"""
You are an expert AI travel planning assistant.

Create a practical travel plan using these requirements.

Origin: {state['origin']}
Destination: {destination}
Start date: {state['start_date']}
End date: {state['end_date']}
Travelers: {state['travelers']}
Total budget: {state['budget']} {state.get('currency', 'INR')}
Preferences: {state.get('preferences', [])}

Destination research queries:
{json.dumps(research_result, ensure_ascii=False, default=str)}

Use the research queries as guidance for destination-specific
recommendations. They are search suggestions, not verified
live research results.

Return ONLY valid JSON with this structure:

{{
  "destination_overview": "string",
  "transportation_options": [
    {{
      "type": "string",
      "description": "string",
      "estimated_cost": 0
    }}
  ],
  "hotel_options": [
    {{
      "type": "string",
      "description": "string",
      "estimated_cost_per_night": 0
    }}
  ],
  "itinerary": [
    {{
      "day": 1,
      "title": "string",
      "activities": ["string"],
      "estimated_cost": 0
    }}
  ],
  "budget_breakdown": {{
    "transportation": 0,
    "accommodation": 0,
    "food": 0,
    "activities": 0,
    "miscellaneous": 0
  }},
  "recommendations": ["string"]
}}

Rules:
- Create a day-wise itinerary for the requested dates.
- Keep estimates within the total budget where practical.
- Use the requested currency.
- Make recommendations relevant to the destination.
- Do not invent live transportation or hotel availability.
- Transportation and hotel options are suggestions, not bookings.
- Return valid JSON without Markdown fences.
"""

    response = await llm.ainvoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = str(content).strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0]

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Groq returned an invalid JSON travel plan."
        )

    plan = json.loads(content[start:end + 1])

    required_output = [
        "destination_overview",
        "transportation_options",
        "hotel_options",
        "itinerary",
        "budget_breakdown",
        "recommendations",
    ]

    missing = [
        key for key in required_output
        if key not in plan
    ]

    if missing:
        raise ValueError(
            f"AI response missing fields: {', '.join(missing)}"
        )

    return {
        "plan_details": plan,
        "destination_research": research_result,
        "agent_trace": ["planner_agent"],
    }


async def budget_agent(state: TravelState) -> dict:
    """
    Analyze the budget using the Budget Allocation MCP tool.
    """

    start = date.fromisoformat(state["start_date"])
    end = date.fromisoformat(state["end_date"])

    days = (end - start).days + 1

    budget_result = await call_travel_mcp_tool(
        "estimate_budget_allocation",
        {
            "total_budget": float(state["budget"]),
            "travelers": state["travelers"],
            "days": days,
            "currency": state.get("currency", "INR"),
        },
    )

    allocation = budget_result["allocation"]

    analysis = {
        "total_budget": budget_result["total_budget"],
        "travelers": budget_result["travelers"],
        "days": budget_result["days"],
        "budget_per_person": budget_result["budget_per_person"],
        "daily_budget_per_person": (
            budget_result["daily_budget_per_person"]
        ),
        "currency": budget_result["currency"],
        "estimated_breakdown": allocation,
        "is_estimate": budget_result["is_estimate"],
    }

    # Preserve the LLM's original estimate for comparison.
    plan_details = dict(state["plan_details"])

    plan_details["llm_budget_breakdown"] = (
        plan_details.get("budget_breakdown", {})
    )

    # Use deterministic MCP allocation as the primary breakdown.
    plan_details["budget_breakdown"] = allocation
    plan_details["mcp_budget_allocation"] = budget_result

    return {
        "plan_details": plan_details,
        "budget_analysis": analysis,
        "mcp_budget_allocation": budget_result,
        "agent_trace": ["budget_agent"],
    }


async def final_response_agent(state: TravelState) -> dict:
    """
    Generate the final response and preparation checklist using MCP.
    """

    destination = state["destination"]

    checklist_result = await call_travel_mcp_tool(
        "get_trip_preparation_checklist",
        {
            "destination": destination,
            "travelers": state["travelers"],
        },
    )

    summary = (
        f"AI travel plan generated for "
        f"{state['origin']} to {destination}, "
        f"for {state['travelers']} traveler(s)."
    )

    next_steps = [
        "Review the generated day-wise itinerary.",
        "Verify transportation prices and availability.",
        "Compare hotel prices before booking.",
        "Review the estimated budget.",
        "Review the destination preparation checklist.",
        "Confirm bookings before travelling.",
    ]

    plan_details = {
        **state["plan_details"],
        "destination_research": state.get(
            "destination_research", {}
        ),
        "preparation_checklist": checklist_result,
        "budget_analysis": state["budget_analysis"],
    }

    final_response = {
        "summary": summary,
        "plan_details": plan_details,
        "budget_analysis": state["budget_analysis"],
        "preparation_checklist": checklist_result,
        "next_steps": next_steps,
    }

    return {
        "status": "completed",
        "summary": summary,
        "next_steps": next_steps,
        "preparation_checklist": checklist_result,
        "final_response": final_response,
        "agent_trace": ["final_response_agent"],
    }
