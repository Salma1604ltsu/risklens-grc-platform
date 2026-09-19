from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Asset, Risk, ComplianceRequirement, Evidence, Remediation
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    risks = db.query(Risk)
    total_risks = risks.count()
    open_risks = risks.filter(Risk.status == "Open").count()
    critical_risks = risks.filter(Risk.severity == "Critical").count()
    high_risks = risks.filter(Risk.severity == "High").count()
    medium_risks = risks.filter(Risk.severity == "Medium").count()
    low_risks = risks.filter(Risk.severity == "Low").count()
    total_assets = db.query(Asset).count()
    total_requirements = db.query(ComplianceRequirement).count()
    assessed_requirements = db.query(ComplianceRequirement).filter(ComplianceRequirement.status != "Not Assessed").count()
    total_evidence = db.query(Evidence).count()
    pending_evidence = db.query(Evidence).filter(Evidence.status == "Pending Review").count()
    total_remediations = db.query(Remediation).count()
    open_remediations = db.query(Remediation).filter(Remediation.status == "Open").count()
    overdue_remediations = db.query(Remediation).filter(Remediation.status == "Overdue").count()

    compliance_rate = round((assessed_requirements / total_requirements) * 100, 2) if total_requirements else 0
    return {
        "assets": {"total": total_assets},
        "risks": {"total": total_risks, "open": open_risks, "critical": critical_risks, "high": high_risks, "medium": medium_risks, "low": low_risks},
        "compliance": {"requirements": total_requirements, "assessed": assessed_requirements, "assessment_rate_percent": compliance_rate},
        "evidence": {"total": total_evidence, "pending_review": pending_evidence},
        "remediation": {"total": total_remediations, "open": open_remediations, "overdue": overdue_remediations},
    }

@router.get("/risk-distribution")
def risk_distribution(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(Risk.severity, func.count(Risk.id)).group_by(Risk.severity).all()
    return [{"severity": severity, "count": count} for severity, count in rows]

@router.get("/compliance-by-framework")
def compliance_by_framework(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(ComplianceRequirement.framework, ComplianceRequirement.status, func.count(ComplianceRequirement.id)).group_by(ComplianceRequirement.framework, ComplianceRequirement.status).all()
    return [{"framework": framework, "status": status, "count": count} for framework, status, count in rows]
