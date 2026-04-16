from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Credential
from ..schemas import CreateCredentialResponse
from ..services.security import generate_api_key, hash_api_key

router = APIRouter(tags=["Credential Management"])


@router.post("/api-key", response_model=CreateCredentialResponse, status_code=201)
def create_credential(db: Session = Depends(get_db)):
    api_key = generate_api_key()
    now = datetime.utcnow()

    credential = Credential(
        key_hash=hash_api_key(api_key),
        key_prefix=api_key[:8],
        created_at=now,
        window_started_at=now,
    )
    db.add(credential)
    db.commit()

    return CreateCredentialResponse(api_key=api_key, key_prefix=api_key[:8], created_at=now)
