from langgraph.graph import StateGraph, START, END

from app.agents.state import TravelState
from app.agents.nodes import (
    supervisor_agent,
    transportation_agent,
    hotel_agent,
    itinerary_agent,
    budget_agent,
    final_response_agent,
)


def build_travel_graph():
    workflow = StateGraph(TravelState)

    # Register agents
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("transportation", transportation_agent)
    workflow.add_node("hotel", hotel_agent)
    workflow.add_node("itinerary", itinerary_agent)
    workflow.add_node("budget", budget_agent)
    workflow.add_node("final_response", final_response_agent)

    # Define workflow
    workflow.add_edge(START, "supervisor")

    # Supervisor decides whether to continue
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: (
            "continue"
            if state.get("status") == "processing"
            else "stop"
        ),
        {
            "continue": "transportation",
            "stop": END,
        },
    )

    workflow.add_edge("transportation", "hotel")
    workflow.add_edge("hotel", "itinerary")
    workflow.add_edge("itinerary", "budget")
    workflow.add_edge("budget", "final_response")
    workflow.add_edge("final_response", END)

    return workflow.compile()


travel_graph = build_travel_graph()