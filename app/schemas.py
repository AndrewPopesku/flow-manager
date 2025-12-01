from typing import List, Optional, Any
from pydantic import BaseModel, Field

class Task(BaseModel):
    name: str = Field(..., description="Unique name of the task")
    description: Optional[str] = Field(None, description="Description of what the task does")

class Condition(BaseModel):
    name: str = Field(..., description="Unique name of the condition")
    description: Optional[str] = Field(None, description="Description of the condition")
    source_task: str = Field(..., description="The name of the task whose result is evaluated")
    outcome: str = Field(..., description="The expected outcome of the source task (e.g., 'success')")
    target_task_success: str = Field(..., description="The next task to execute if the outcome matches")
    target_task_failure: str = Field("end", description="The next task to execute if the outcome does not match")

class Flow(BaseModel):
    id: str = Field(..., description="Unique identifier for the flow")
    name: str = Field(..., description="Human-readable name of the flow")
    start_task: str = Field(..., description="The name of the first task to execute")
    tasks: List[Task] = Field(..., description="List of tasks in the flow")
    conditions: List[Condition] = Field(..., description="List of conditions governing flow logic")

class TaskResult(BaseModel):
    status: str = Field(..., description="Status of the task execution (e.g., 'success', 'failure')")
    data: Optional[Any] = Field(None, description="Output data from the task")
