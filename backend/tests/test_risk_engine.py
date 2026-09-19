import pytest

from app.risk.engine import calculate_risk, classify_risk


def test_risk_calculation():
    result = calculate_risk(4, 5)
    assert result["score"] == 20
    assert result["severity"] == "Critical"


def test_risk_boundaries():
    assert classify_risk(1) == "Low"
    assert classify_risk(5) == "Medium"
    assert classify_risk(10) == "High"
    assert classify_risk(16) == "Critical"


def test_invalid_likelihood():
    with pytest.raises(ValueError):
        calculate_risk(6, 3)
