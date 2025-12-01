from fastapi import APIRouter, HTTPException
from app.schemas import Flow, FlowCreate
from app.engine import FlowEngine
import uuid

router = APIRouter()


@router.post("/flow/execute")
async def execute_flow(flow_in: FlowCreate):
    """
    Executes a flow defined in the request body.
    """
    try:
        flow = Flow(id=uuid.uuid4(), **flow_in.model_dump())
        engine = FlowEngine(flow)
        engine.run()
        return {
            "message": f"Flow '{flow.name}' executed successfully.",
            "flow_id": flow.id,
            "history": [r.model_dump() for r in engine.execution_history.values()],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/run-sample")
async def run_sample_flow():
    """
    Runs a hardcoded sample flow for demonstration purposes.
    """
    sample_flow_data = {
        "id": uuid.uuid4(),
        "name": "Data processing flow",
        "start_task": "task1",
        "tasks": [
            {"name": "task1", "description": "Fetch data"},
            {"name": "task2", "description": "Process data"},
            {"name": "task3", "description": "Store data"},
        ],
        "conditions": [
            {
                "name": "condition_task1_result",
                "description": "Evaluate the result of task1.",
                "source_task": "task1",
                "outcome": "success",
                "target_task_success": "task2",
                "target_task_failure": "end",
            },
            {
                "name": "condition_task2_result",
                "description": "Evaluate the result of task2.",
                "source_task": "task2",
                "outcome": "success",
                "target_task_success": "task3",
                "target_task_failure": "end",
            },
        ],
    }

    flow = Flow(**sample_flow_data)
    engine = FlowEngine(flow)
    engine.run()

    # Construct a more detailed response
    history = {k: v.model_dump() for k, v in engine.execution_history.items()}
    return {
        "message": "Sample flow executed.",
        "flow_id": flow.id,
        "execution_history": history,
    }
