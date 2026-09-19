from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    asset_type: str = Field(min_length=2, max_length=50)
    owner: str = Field(min_length=2, max_length=120)
    criticality: int = Field(default=3, ge=1, le=5)
    description: str | None = None


class RiskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    asset_id: int = Field(gt=0)
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    treatment: str = "Mitigate"
    owner: str = Field(min_length=2, max_length=120)
    description: str | None = None


class RiskResponse(RiskCreate):
    id: int
    score: int
    severity: str
    status: str

    class Config:
        from_attributes = True
