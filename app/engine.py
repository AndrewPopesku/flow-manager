import logging
from typing import Dict, Optional
from app.schemas import Flow, TaskResult, Condition
from app.tasks import get_task_function

logger = logging.getLogger(__name__)


class FlowEngine:
    def __init__(self):
        pass

    def run(self, flow: Flow) -> Dict[str, TaskResult]:
        """
        Executes the flow starting from the start_task.
        """
        execution_history: Dict[str, TaskResult] = {}
        current_task_name = flow.start_task
        logger.info(f"Starting flow: {flow.name} (ID: {flow.id})")

        while current_task_name and current_task_name != "end":
            # 1. Execute the current task
            task_func = get_task_function(current_task_name)
            if not task_func:
                logger.error(
                    f"Error: Task '{current_task_name}' not found in registry."
                )
                break
            try:
                result = task_func()
                execution_history[current_task_name] = result
                logger.info(
                    f"Task '{current_task_name}' completed with status: {result.status}"
                )
            except Exception as e:
                logger.error(f"Error executing task '{current_task_name}': {e}")
                result = TaskResult(status="failure", data={"error": str(e)})
                execution_history[current_task_name] = result

            # 2. Determine the next task based on conditions
            next_task_name = self._evaluate_next_task(flow, current_task_name, result)
            current_task_name = next_task_name
        logger.info("Flow execution finished.")
        return execution_history

    def _evaluate_next_task(
        self, flow: Flow, current_task_name: str, result: TaskResult
    ) -> str:
        """
        Evaluates conditions to determine the next task.
        """
        relevant_condition: Optional[Condition] = None
        for condition in flow.conditions:
            if condition.source_task == current_task_name:
                relevant_condition = condition
                break

        if not relevant_condition:
            logger.info(
                f"No condition found for task '{current_task_name}'. Ending flow."
            )
            return "end"

        if result.status == relevant_condition.outcome:
            return relevant_condition.target_task_success
        else:
            return relevant_condition.target_task_failure
