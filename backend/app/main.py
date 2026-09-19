from fastapi import FastAPI
from app.db import Base, engine
from app.routes import router as grc_router
from app.auth_routes import router as auth_router
from app.compliance import router as compliance_router
from app.risk.engine import calculate_risk

Base.metadata.create_all(bind=engine)
app = FastAPI(title="RiskLens GRC API", version="0.4.0", description="Cybersecurity risk and compliance management API")
app.include_router(auth_router)
app.include_router(grc_router)
app.include_router(compliance_router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "risklens-api", "version": "0.4.0"}

@app.get("/api/v1/risk/calculate", tags=["risk"])
def calculate_risk_score(likelihood: int, impact: int):
    return calculate_risk(likelihood, impact)
