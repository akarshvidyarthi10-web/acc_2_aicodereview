from pydantic import BaseModel
from typing import List


class ReviewResult(BaseModel):
    summary: str
    issues: List[str]
    suggestions: List[str]
    comment: str
