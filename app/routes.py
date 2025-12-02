from fastapi import APIRouter, HTTPException
from app.schemas import Flow, FlowCreate, FlowExecutionResponse
from app.engine import FlowEngine
import uuid
import json
import os

router = APIRouter()
flow_engine = FlowEngine()


@router.post("/flow/execute")
async def execute_flow(flow_in: FlowCreate):
    """
    Executes a flow defined in the request body.
    """
    try:
        flow = Flow(id=uuid.uuid4(), **flow_in.model_dump())
        history = flow_engine.run(flow)
        return {
            "message": f"Flow '{flow.name}' executed successfully.",
            "flow_id": flow.id,
            "history": [r.model_dump() for r in history.values()],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/run-sample", response_model=FlowExecutionResponse)
async def run_sample_flow():
    """
    Runs a hardcoded sample flow for demonstration purposes.
    """
    # Load sample flow data from JSON file
    file_path = os.path.join(os.path.dirname(__file__), "sample_flow.json")
    with open(file_path, "r") as f:
        sample_flow_data = json.load(f)

    # Add a dynamic ID
    sample_flow_data["id"] = uuid.uuid4()

    flow = Flow(**sample_flow_data)
    history = flow_engine.run(flow)

    # Construct a more detailed response
    return FlowExecutionResponse(
        message="Sample flow executed.",
        flow_id=flow.id,
        execution_history=history,
    )
