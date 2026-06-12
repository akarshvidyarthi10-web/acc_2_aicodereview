from pydantic import BaseModel
from typing import Optional, Dict


class ManualReviewRequest(BaseModel):
    repository: str
    pull_request_number: int
    metadata: Optional[Dict[str, str]] = None
