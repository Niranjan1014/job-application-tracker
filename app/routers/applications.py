from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.security import get_current_user

router = APIRouter()
VALID_STATUSES = {"Applied", "Screening", "Interview", "Offer", "Rejected"}


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = Application(**payload.model_dump(), user_id=current_user.id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(
    status_filter: Optional[str] = Query(None, alias="status"),
    company: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Application).filter(Application.user_id == current_user.id)
    if status_filter:
        if status_filter not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid application status")
        query = query.filter(Application.status == status_filter)
    if company:
        query = query.filter(Application.company.ilike(f"%{company}%"))
    return query.order_by(Application.applied_date.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.query(Application).filter(
        Application.id == app_id,
        Application.user_id == current_user.id,
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.patch("/{app_id}", response_model=ApplicationResponse)
def update_application(
    app_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.query(Application).filter(
        Application.id == app_id,
        Application.user_id == current_user.id,
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    changes = payload.model_dump(exclude_unset=True)
    if "status" in changes and changes["status"] not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid application status")
    for field, value in changes.items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.query(Application).filter(
        Application.id == app_id,
        Application.user_id == current_user.id,
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return None
