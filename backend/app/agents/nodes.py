
import json

from app.agents.state import TravelState
from app.core.llm import get_llm


def supervisor_agent(state: TravelState) -> dict:
    required = [
        "origin",
        "destination",
        "start_date",
        "end_date",
        "travelers",
        "budget",
    ]

    missing = [
        field for field in required
        if state.get(field) is None
    ]

    if missing:
        return {
            "status": "failed",
            "errors": [f"Missing fields: {', '.join(missing)}"],
            "agent_trace": ["supervisor_agent"],
        }

    if state["travelers"] < 1 or state["budget"] <= 0:
        return {
            "status": "failed",
            "errors": ["Invalid travelers or budget."],
            "agent_trace": ["supervisor_agent"],
        }

    return {
        "status": "processing",
        "agent_trace": ["supervisor_agent"],
    }


def planner_agent(state: TravelState) -> dict:
    llm = get_llm()

    prompt = f"""
You are an expert AI travel planning assistant.

Create a practical travel plan using these requirements:

Origin: {state['origin']}
Destination: {state['destination']}
Start date: {state['start_date']}
End date: {state['end_date']}
Travelers: {state['travelers']}
Total budget: {state['budget']} {state.get('currency', 'INR')}
Preferences: {state.get('preferences', [])}

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
- Do not invent real-time flight, train, bus or hotel availability.
- All transportation and hotel options are suggestions,
  not confirmed bookings.
- Return valid JSON without Markdown fences.
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = str(content).strip()

    # Handle occasional Markdown JSON fences.
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0]

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Groq returned an invalid JSON travel plan.")

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
        "agent_trace": ["planner_agent"],
    }


def budget_agent(state: TravelState) -> dict:
    budget = float(state["budget"])
    travelers = state["travelers"]

    analysis = {
        "total_budget": budget,
        "travelers": travelers,
        "budget_per_person": round(budget / travelers, 2),
        "currency": state.get("currency", "INR"),
        "estimated_breakdown": state["plan_details"].get(
            "budget_breakdown", {}
        ),
    }

    return {
        "budget_analysis": analysis,
        "agent_trace": ["budget_agent"],
    }


def final_response_agent(state: TravelState) -> dict:
    destination = state["destination"]

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
        "Confirm bookings before travelling.",
    ]

    return {
        "status": "completed",
        "summary": summary,
        "next_steps": next_steps,
        "final_response": {
            "summary": summary,
            "plan_details": state["plan_details"],
            "budget_analysis": state["budget_analysis"],
            "next_steps": next_steps,
        },
        "agent_trace": ["final_response_agent"],
    }
