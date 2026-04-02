# Project Resource & Dependency Map

This file tracks how our Documentation (Blueprints) connects to our Python (Construction).

| Feature / Logic | Source Documentation | Python Implementation |
| :--- | :--- | :--- |
| **User & Roles** | `docs/04-data-model.md` | `models.py` & `routers/users.py` |
| **Sunday Grace Period** | `docs/11-backend-logic.md` | `routers/slots.py` |
| **Audit & Revert** | `docs/11-backend-logic.md` | `models.py` (AuditLog Table) |
| **Tenure Awards** | `docs/12-reporting-logic.md` | `routers/reports.py` |
| **Birthday Dashboard** | `docs/12-reporting-logic.md` | `routers/reports.py` |

---

## 🛑 Critical Cross-Checks
- **Changing a Model?** You MUST update the corresponding Router.
- **Changing a Requirement?** You MUST check the Implementation Logic file.
- **Adding a new Library?** Update `backend/requirements.txt`.
