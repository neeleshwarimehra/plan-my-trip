
from langgraph.graph import StateGraph, START, END

from app.agents.state import TravelState
from app.agents.nodes import (
    supervisor_agent,
    planner_agent,
    budget_agent,
    final_response_agent,
)


def build_travel_graph():
    workflow = StateGraph(TravelState)

    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("budget", budget_agent)
    workflow.add_node("final_response", final_response_agent)

    workflow.add_edge(START, "supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        lambda state: (
            "continue"
            if state.get("status") == "processing"
            else "stop"
        ),
        {
            "continue": "planner",
            "stop": END,
        },
    )

    workflow.add_edge("planner", "budget")
    workflow.add_edge("budget", "final_response")
    workflow.add_edge("final_response", END)

    return workflow.compile()


travel_graph = build_travel_graph()
