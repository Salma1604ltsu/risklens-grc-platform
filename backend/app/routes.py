from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Asset, Risk
from app.risk.engine import calculate_risk
from app.schemas import AssetCreate, RiskCreate, RiskResponse

router = APIRouter(prefix="/api/v1", tags=["GRC"])


@router.post("/assets")
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).order_by(Asset.id.desc()).all()


@router.post("/risks", response_model=RiskResponse)
def create_risk(payload: RiskCreate, db: Session = Depends(get_db)):
    if not db.get(Asset, payload.asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")
    result = calculate_risk(payload.likelihood, payload.impact)
    risk = Risk(**payload.model_dump(), score=result["score"], severity=result["severity"])
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk


@router.get("/risks", response_model=list[RiskResponse])
def list_risks(db: Session = Depends(get_db)):
    return db.query(Risk).order_by(Risk.id.desc()).all()
