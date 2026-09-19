from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Evidence, Remediation, Risk
from app.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/v1", tags=["Evidence & Remediation"])

class EvidenceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    evidence_type: str = Field(min_length=2, max_length=50)
    reference: str = Field(min_length=2, max_length=500)
    status: str = "Pending Review"
    uploaded_by: str = Field(min_length=2, max_length=120)

class RemediationCreate(BaseModel):
    risk_id: int = Field(gt=0)
    action: str = Field(min_length=5)
    owner: str = Field(min_length=2, max_length=120)
    status: str = "Open"
    due_date: str | None = None

@router.post("/evidence")
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = Evidence(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/evidence")
def list_evidence(status: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Evidence)
    if status:
        query = query.filter(Evidence.status == status)
    return query.order_by(Evidence.id.desc()).all()

@router.post("/remediations")
def create_remediation(payload: RemediationCreate, db: Session = Depends(get_db), user=Depends(require_roles("admin", "grc_manager", "analyst"))):
    if not db.get(Risk, payload.risk_id):
        raise HTTPException(status_code=404, detail="Risk not found")
    item = Remediation(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/remediations")
def list_remediations(status: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Remediation)
    if status:
        query = query.filter(Remediation.status == status)
    return query.order_by(Remediation.id.desc()).all()
