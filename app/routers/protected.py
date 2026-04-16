from datetime import datetime

from fastapi import APIRouter, Depends

from ..dependencies import require_valid_api_key
from ..models import Credential
from ..schemas import ProtectedResourceResponse, UsageSummaryResponse

router = APIRouter(tags=["Protected APIs"])


@router.get("/data", response_model=ProtectedResourceResponse)
def protected_data(credential: Credential = Depends(require_valid_api_key)):
    return ProtectedResourceResponse(
        message="You accessed protected data",
        key_prefix=credential.key_prefix,
        served_at=datetime.utcnow(),
    )


@router.get("/usage", response_model=UsageSummaryResponse)
def usage_summary(credential: Credential = Depends(require_valid_api_key)):
    return UsageSummaryResponse(
        key_prefix=credential.key_prefix,
        created_at=credential.created_at,
        total_requests=credential.total_requests,
        current_window_count=credential.window_count,
        window_started_at=credential.window_started_at,
        last_used_at=credential.last_used_at,
    )
