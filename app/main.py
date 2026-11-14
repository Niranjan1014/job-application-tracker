from fastapi import FastAPI
from app.routers import auth, applications

app = FastAPI(
    title="Job Application Tracker",
    description="Track job applications with secure user accounts and status workflows.",
    version="1.1.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
