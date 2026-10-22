from pydantic import BaseModel
from typing import Optional,Dict,Any,Literal
from uuid import UUID

class EvaluationRequest(BaseModel):
    question_id: UUID
    solution_type: Literal["text", "mermaid", "reactflow"]
    solution_text: Optional[str] = None
    mermaid_code: Optional[str] = None
    graph: Optional[Dict[str, Any]] = None  # React Flow JSON

class HintRequest(BaseModel):
    submission_id: int