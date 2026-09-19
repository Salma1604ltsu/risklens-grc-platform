from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.db import get_db
from app.models import Control, ComplianceRequirement
from app.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/v1/compliance", tags=["Compliance"])

class RequirementCreate(BaseModel):
    framework: str = Field(min_length=2, max_length=80)
    requirement_id: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=2, max_length=250)
    status: str = "Not Assessed"
    notes: str | None = None

class ControlCreate(BaseModel):
    control_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=2, max_length=200)
    framework: str = Field(min_length=2, max_length=80)
    status: str = "Not Implemented"
    owner: str = Field(min_length=2, max_length=120)
    description: str | None = None

@router.post("/requirements")
def create_requirement(payload: RequirementCreate, db: Session = Depends(get_db), user=Depends(require_roles("admin", "grc_manager"))):
    item = ComplianceRequirement(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/requirements")
def list_requirements(framework: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(ComplianceRequirement)
    if framework:
        query = query.filter(ComplianceRequirement.framework == framework)
    return query.order_by(ComplianceRequirement.framework, ComplianceRequirement.requirement_id).all()

@router.post("/controls")
def create_control(payload: ControlCreate, db: Session = Depends(get_db), user=Depends(require_roles("admin", "grc_manager"))):
    if db.query(Control).filter(Control.control_id == payload.control_id).first():
        raise HTTPException(status_code=409, detail="Control ID already exists")
    item = Control(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/controls")
def list_controls(framework: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Control)
    if framework:
        query = query.filter(Control.framework == framework)
    return query.order_by(Control.framework, Control.control_id).all()
