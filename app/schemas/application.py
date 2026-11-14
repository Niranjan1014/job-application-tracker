from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    job_url: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: str
    job_url: Optional[str] = None
    applied_date: datetime
