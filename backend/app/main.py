from fastapi import FastAPI

from app.risk.engine import calculate_risk

app = FastAPI(
    title="RiskLens GRC API",
    version="0.1.0",
    description="Cybersecurity risk and compliance management API",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "risklens-api"}


@app.get("/api/v1/risk/calculate", tags=["risk"])
def calculate_risk_score(likelihood: int, impact: int) -> dict[str, int | str]:
    result = calculate_risk(likelihood, impact)
    return result
