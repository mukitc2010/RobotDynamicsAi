from pydantic import BaseModel
from typing import List


class Task(BaseModel):
    name: str
    description: str = ""
    completed: bool = False


class Milestone(BaseModel):
    name: str
    tasks: List[Task] = []
    achieved: bool = False
