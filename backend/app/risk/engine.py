def _validate_score(value: int, field: str) -> None:
    if not 1 <= value <= 5:
        raise ValueError(f"{field} must be between 1 and 5")


def classify_risk(score: int) -> str:
    if score >= 16:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def calculate_risk(likelihood: int, impact: int) -> dict[str, int | str]:
    _validate_score(likelihood, "likelihood")
    _validate_score(impact, "impact")

    score = likelihood * impact
    return {
        "likelihood": likelihood,
        "impact": impact,
        "score": score,
        "severity": classify_risk(score),
    }
