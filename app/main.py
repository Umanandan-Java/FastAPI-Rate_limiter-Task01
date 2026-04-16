from fastapi import FastAPI

from .database import Base, engine
from .routers.credentials import router as credentials_router
from .routers.protected import router as protected_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Key & Rate Limiting Service",
    version="1.0.0",
    description="FastAPI backend assignment - Task 1",
)

app.include_router(credentials_router)
app.include_router(protected_router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}

