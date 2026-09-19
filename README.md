# RiskLens GRC

Automated Cybersecurity Risk & Compliance Management Platform.

RiskLens is a portfolio-grade GRC application for managing assets, cybersecurity risks, controls, compliance requirements, evidence, audits, vendors, and remediation activities in one place.

## Project Goals

- Centralize organizational cyber risk information
- Calculate inherent and residual risk consistently
- Map risks and controls to common security frameworks
- Track evidence and remediation
- Support audit-ready workflows
- Provide role-based access through a REST API

## Planned Stack

- Backend: Python, FastAPI
- Database: PostgreSQL
- Frontend: React, Tailwind CSS
- Authentication: JWT + RBAC
- API documentation: OpenAPI
- Deployment: Docker
- CI: GitHub Actions

## Risk Model

Risk score is calculated using:

**Risk Score = Likelihood × Impact**

Both likelihood and impact use a 1-5 scale.

The platform will also calculate residual risk after considering control effectiveness.

## Security & Safety

RiskLens is a defensive GRC application. It does not perform exploitation. Any security testing integrations will be restricted to systems for which the operator has explicit authorization.

## Development Roadmap

- [x] Repository initialization
- [ ] Project architecture
- [ ] Database models
- [ ] Risk calculation engine
- [ ] FastAPI backend
- [ ] Authentication and RBAC
- [ ] Asset and risk management
- [ ] Control and compliance management
- [ ] Evidence and audit management
- [ ] Vendor risk management
- [ ] React dashboard
- [ ] Docker deployment
- [ ] CI pipeline
- [ ] Automated tests

## License

MIT
