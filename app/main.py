"""Job Application Tracker - FastAPI entry point."""
from fastapi import FastAPI
from app.routers import auth, applications
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker",
    description="Track job applications with status workflows and JWT auth",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])


@app.get("/health")
def health():
    return {"status": "ok"}
