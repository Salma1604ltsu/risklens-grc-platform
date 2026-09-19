# RiskLens Architecture

## High-level flow

Client -> React frontend -> FastAPI REST API -> PostgreSQL

Cross-cutting services include authentication/RBAC, audit logging, risk calculation, compliance mapping, evidence metadata, and reporting.

## Core domains

### Asset
Represents a business asset such as an application, database, server, endpoint, API, or cloud resource.

### Risk
Represents a threat/vulnerability scenario affecting an asset. A risk stores likelihood, impact, inherent score, treatment, owner, and lifecycle status.

### Control
Represents a security measure used to reduce risk. Controls can be mapped to multiple frameworks.

### Evidence
Represents documentation or an artifact supporting implementation of a control or completion of an audit requirement.

### Compliance Requirement
Represents a framework requirement, such as an ISO 27001, NIST CSF, NIST 800-53, or CIS Controls requirement.

### Audit
Represents an assessment containing requirements, evidence, findings, and corrective actions.

## Risk calculation

Likelihood and impact are integer values from 1 to 5.

Inherent risk = likelihood x impact.

Residual risk is derived from inherent risk and the effectiveness of implemented controls. The calculation will be centralized in the backend so that the same rules are used by the API, dashboard, and reports.

## Security design

- Passwords are stored as secure password hashes, never plaintext.
- JWTs are used for API authentication.
- Authorization is enforced through RBAC.
- API inputs are validated with typed schemas.
- Sensitive configuration is supplied through environment variables.
- Audit events are recorded for important state changes.
