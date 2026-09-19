from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user, require_roles
from app.db import get_db
from app.models import Asset, Risk, ComplianceRequirement, Evidence, Remediation, Control, AuditLog

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.get("/risk-compliance")
def risk_compliance_report(db: Session = Depends(get_db), user=Depends(require_roles("admin", "grc_manager", "auditor"))):
    risks = db.query(Risk).all()
    requirements = db.query(ComplianceRequirement).all()
    evidence = db.query(Evidence).all()
    remediations = db.query(Remediation).all()
    controls = db.query(Control).all()
    assets = db.query(Asset).all()
    audit_logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(20).all()

    total_requirements = len(requirements)
    assessed = sum(1 for r in requirements if r.status != "Not Assessed")
    implemented_controls = sum(1 for c in controls if c.status == "Implemented")
    total_controls = len(controls)

    return {
        "report": {
            "name": "RiskLens Risk & Compliance Report",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "generated_by": user.email,
        },
        "executive_summary": {
            "total_assets": len(assets),
            "total_risks": len(risks),
            "open_risks": sum(1 for r in risks if r.status == "Open"),
            "critical_risks": sum(1 for r in risks if r.severity == "Critical"),
            "high_risks": sum(1 for r in risks if r.severity == "High"),
            "compliance_assessment_rate_percent": round(assessed / total_requirements * 100, 2) if total_requirements else 0,
            "control_implementation_rate_percent": round(implemented_controls / total_controls * 100, 2) if total_controls else 0,
            "pending_evidence": sum(1 for e in evidence if e.status == "Pending Review"),
            "open_remediations": sum(1 for r in remediations if r.status == "Open"),
            "overdue_remediations": sum(1 for r in remediations if r.status == "Overdue"),
        },
        "risk_breakdown": {
            "critical": sum(1 for r in risks if r.severity == "Critical"),
            "high": sum(1 for r in risks if r.severity == "High"),
            "medium": sum(1 for r in risks if r.severity == "Medium"),
            "low": sum(1 for r in risks if r.severity == "Low"),
        },
        "compliance": {
            "total_requirements": total_requirements,
            "assessed_requirements": assessed,
            "by_framework": {},
        },
        "recent_audit_activity": [
            {"action": log.action, "resource_type": log.resource_type, "resource_id": log.resource_id, "user": log.user_email, "created_at": log.created_at.isoformat()}
            for log in audit_logs
        ],
    }
