from datetime import datetime

from pydantic import BaseModel, Field


class CreateCredentialResponse(BaseModel):
    api_key: str = Field(..., description="Store this key securely; it is shown only once.")
    key_prefix: str
    created_at: datetime


class ProtectedResourceResponse(BaseModel):
    message: str
    key_prefix: str
    served_at: datetime


class UsageSummaryResponse(BaseModel):
    key_prefix: str
    created_at: datetime
    total_requests: int
    current_window_count: int
    window_started_at: datetime
    last_used_at: datetime | None

