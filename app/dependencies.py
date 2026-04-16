from datetime import datetime, timedelta

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Credential, UsageEvent
from .services.security import hash_api_key

RATE_LIMIT = 5
RATE_WINDOW_SECONDS = 60


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_valid_api_key(
    request: Request,
    x_api_key: str = Header(..., alias="x-api-key"),
    db: Session = Depends(get_db),
) -> Credential:
    credential = (
        db.query(Credential)
        .filter(Credential.key_hash == hash_api_key(x_api_key))
        .first()
    )
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    now = datetime.utcnow()
    if now - credential.window_started_at >= timedelta(seconds=RATE_WINDOW_SECONDS):
        credential.window_started_at = now
        credential.window_count = 0

    if credential.window_count >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded ({RATE_LIMIT} requests / {RATE_WINDOW_SECONDS} seconds)",
        )

    credential.window_count += 1
    credential.total_requests += 1
    credential.last_used_at = now

    db.add(
        UsageEvent(
            credential_id=credential.id,
            endpoint=request.url.path,
            method=request.method,
            created_at=now,
        )
    )
    db.commit()
    db.refresh(credential)
    return credential

