from pydantic import BaseModel
from typing import List, Optional


class ReviewResponse(BaseModel):
    summary: str
    issues: List[str]
    suggestions: List[str]
    comment: Optional[str] = None
