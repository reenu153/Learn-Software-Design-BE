from pydantic import BaseModel
from typing import Optional

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str]
    order_index: int
    course_path_id: str
    points: Optional[int] = 0