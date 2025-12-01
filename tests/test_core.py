import unittest
from app.schemas import Flow, Task, Condition, TaskResult
from app.engine import FlowEngine
from app.tasks import register_task, TASK_REGISTRY


# Mock tasks for testing
@register_task("mock_success")
def mock_success():
    return TaskResult(status="success", data="ok")


@register_task("mock_failure")
def mock_failure():
    return TaskResult(status="failure", data="error")


class TestFlowEngine(unittest.TestCase):
    def setUp(self):
        self.flow_data = {
            "id": "test_flow",
            "name": "Test Flow",
            "start_task": "mock_success",
            "tasks": [
                {"name": "mock_success", "description": "Mock Success"},
                {"name": "mock_failure", "description": "Mock Failure"},
            ],
            "conditions": [
                {
                    "name": "cond1",
                    "description": "check success",
                    "source_task": "mock_success",
                    "outcome": "success",
                    "target_task_success": "end",
                    "target_task_failure": "mock_failure",
                }
            ],
        }

    def test_flow_execution_success(self):
        flow = Flow(**self.flow_data)
        engine = FlowEngine(flow)
        engine.run()

        self.assertIn("mock_success", engine.execution_history)
        self.assertEqual(engine.execution_history["mock_success"].status, "success")
        # Should end after mock_success because target_task_success is "end"
        self.assertNotIn("mock_failure", engine.execution_history)

    def test_flow_execution_failure_path(self):
        # Modify condition to go to mock_failure on success (just to test path)
        self.flow_data["conditions"][0]["target_task_success"] = "mock_failure"
        # Add condition for mock_failure to end
        self.flow_data["conditions"].append(
            {
                "name": "cond2",
                "description": "check failure",
                "source_task": "mock_failure",
                "outcome": "success",  # mock_failure returns failure, so this won't match
                "target_task_success": "end",
                "target_task_failure": "end",
            }
        )

        flow = Flow(**self.flow_data)
        engine = FlowEngine(flow)
        engine.run()

        self.assertIn("mock_success", engine.execution_history)
        self.assertIn("mock_failure", engine.execution_history)
        self.assertEqual(engine.execution_history["mock_failure"].status, "failure")


if __name__ == "__main__":
    unittest.main()
