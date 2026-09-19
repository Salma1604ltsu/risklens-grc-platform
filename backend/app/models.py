from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(30), default="analyst")


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    asset_type: Mapped[str] = mapped_column(String(50))
    owner: Mapped[str] = mapped_column(String(120))
    criticality: Mapped[int] = mapped_column(Integer, default=3)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    risks: Mapped[list["Risk"]] = relationship(back_populates="asset")


class Risk(Base):
    __tablename__ = "risks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    likelihood: Mapped[int] = mapped_column(Integer)
    impact: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    severity: Mapped[str] = mapped_column(String(20))
    treatment: Mapped[str] = mapped_column(String(50), default="Mitigate")
    status: Mapped[str] = mapped_column(String(30), default="Open")
    owner: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    asset: Mapped[Asset] = relationship(back_populates="risks")


class Control(Base):
    __tablename__ = "controls"
    id: Mapped[int] = mapped_column(primary_key=True)
    control_id: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    framework: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(30), default="Not Implemented")
    owner: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"
    id: Mapped[int] = mapped_column(primary_key=True)
    framework: Mapped[str] = mapped_column(String(80), index=True)
    requirement_id: Mapped[str] = mapped_column(String(80))
    title: Mapped[str] = mapped_column(String(250))
    status: Mapped[str] = mapped_column(String(30), default="Not Assessed")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    evidence_type: Mapped[str] = mapped_column(String(50))
    reference: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="Pending Review")
    uploaded_by: Mapped[str] = mapped_column(String(120))


class Remediation(Base):
    __tablename__ = "remediations"
    id: Mapped[int] = mapped_column(primary_key=True)
    risk_id: Mapped[int] = mapped_column(ForeignKey("risks.id"))
    action: Mapped[str] = mapped_column(Text)
    owner: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30), default="Open")
    due_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
