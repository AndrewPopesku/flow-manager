import logging
import time
from typing import Callable, Dict
from app.schemas import TaskResult

logger = logging.getLogger(__name__)

# Task Registry to hold available tasks
TASK_REGISTRY: Dict[str, Callable[[], TaskResult]] = {}


def register_task(name: str):
    def decorator(func: Callable[[], TaskResult]):
        TASK_REGISTRY[name] = func
        return func

    return decorator


@register_task("task1")
def task1_fetch_data() -> TaskResult:
    """
    Simulates fetching data.
    """
    logger.info("Executing task1: Fetching data...")
    time.sleep(0.5)
    return TaskResult(status="success", data={"raw_data": "data"})


@register_task("task2")
def task2_process_data() -> TaskResult:
    """
    Simulates processing data.
    """
    logger.info("Executing task2: Processing data...")
    time.sleep(0.5)
    return TaskResult(status="success", data={"processed_data": "data"})


@register_task("task3")
def task3_store_data() -> TaskResult:
    """
    Simulates storing data.
    """
    logger.info("Executing task3: Storing data...")
    time.sleep(0.5)
    return TaskResult(status="success", data={"storage_id": "12345"})


def get_task_function(task_name: str) -> Callable[[], TaskResult]:
    """
    Retrieves the function for a given task name.
    """
    return TASK_REGISTRY.get(task_name)
