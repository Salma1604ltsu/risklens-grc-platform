from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routes import router as grc_router
from app.auth_routes import router as auth_router
from app.compliance import router as compliance_router
from app.evidence_routes import router as evidence_router
from app.dashboard import router as dashboard_router
from app.audit import router as audit_router
from app.reports import router as reports_router
from app.risk.engine import calculate_risk
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RiskLens GRC API",
    version="0.7.0",
    description="Cybersecurity risk and compliance management API",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    # Allow the production Vercel app and its preview deployments.
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(grc_router)
app.include_router(compliance_router)
app.include_router(evidence_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
app.include_router(reports_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "risklens-api", "version": "0.7.0"}


@app.get("/api/v1/risk/calculate", tags=["risk"])
def calculate_risk_score(likelihood: int, impact: int):
    return calculate_risk(likelihood, impact)
