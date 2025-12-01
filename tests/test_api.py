from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_run_sample_flow():
    response = client.post("/flow/run-sample")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sample flow executed."
    assert "execution_history" in data
    assert "task1" in data["execution_history"]
    assert "task2" in data["execution_history"]
    assert "task3" in data["execution_history"]


def test_execute_custom_flow():
    flow_payload = {
        "id": "custom_flow",
        "name": "Custom Flow",
        "start_task": "task1",
        "tasks": [{"name": "task1", "description": "Fetch data"}],
        "conditions": [
            {
                "name": "cond1",
                "description": "test",
                "source_task": "task1",
                "outcome": "success",
                "target_task_success": "end",
                "target_task_failure": "end",
            }
        ],
    }
    response = client.post("/flow/execute", json=flow_payload)
    assert response.status_code == 200
    data = response.json()
    assert "success" in [
        h["status"] for h in data["history"]
    ]  # Check if status is present, history is list of dicts
    # Actually history is list of TaskResult dicts: [{'status': 'success', 'data': ...}]
    assert data["history"][0]["status"] == "success"
