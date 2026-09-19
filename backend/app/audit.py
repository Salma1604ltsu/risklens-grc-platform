import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth import get_current_user, require_roles
from app.db import get_db
from app.models import AuditLog, User

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])

def write_audit(db: Session, user: User, action: str, resource_type: str, resource_id=None, details=None):
    log = AuditLog(user_id=user.id, user_email=user.email, action=action, resource_type=resource_type,
                   resource_id=str(resource_id) if resource_id is not None else None,
                   details=json.dumps(details) if details is not None else None)
    db.add(log)
    db.commit()
    return log

@router.get("/logs")
def list_audit_logs(action: str | None = None, resource_type: str | None = None,
                    limit: int = Query(default=100, ge=1, le=500),
                    db: Session = Depends(get_db), user=Depends(require_roles("admin", "grc_manager", "auditor"))):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    return query.order_by(AuditLog.id.desc()).limit(limit).all()

@router.get("/my-activity")
def my_activity(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(AuditLog).filter(AuditLog.user_id == user.id).order_by(AuditLog.id.desc()).limit(limit).all()
