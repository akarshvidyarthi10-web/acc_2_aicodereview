from pydantic import BaseModel
from typing import List, Optional


class PRFile(BaseModel):
    filename: str
    patch: Optional[str] = None


class PullRequest(BaseModel):
    number: int
    title: str
    body: Optional[str] = None
    user: Optional[str] = None
    files: List[PRFile] = []
