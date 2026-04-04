# 00. Architectural Decision Records (ADR)
> **File:** `00-architecture-decisions.md`  
> **Status:** `STABLE` | **Domain:** `System Design & Standards`

---

## 1. Executive Summary
This document outlines the core technical philosophies and data management strategies for the Ushering Ministry System. It serves as the "Rulebook" for choosing between ORM simplicity and Raw SQL performance to ensure the system remains both scalable and maintainable.

---

## 2. Data Management Strategy
We employ a hybrid database interaction model to balance developer velocity with execution efficiency.

| Task | Methodology | Rationale |
| :--- | :--- | :--- |
| **Basic CRUD** | **ORM (SQLAlchemy)** | Maximizes safety and speed for standard Create, Read, Update, and Delete operations. |
| **Complex Reporting** | **Raw SQL / Analytics** | Offloads heavy data aggregation and "math" to the database engine for peak performance. |
| **Schema Evolution** | **Alembic Migrations** | Provides a version-controlled history, ensuring environment parity across all developer machines. |

---

## 3. Implementation Reference

### Pythonic CRUD (ORM)
*Use for single-record lookups and basic relationship mapping.*
```python
# Standard lookup by Unique Index
user = db.query(User).filter(User.phone == "0917...").first()
```

### High-Performance Analytics (Raw SQL)
*Use for dashboarding, multi-table joins, and group-by aggregations.*
```sql
-- Calculating slot utilization for the Admin Dashboard
SELECT slot_id, COUNT(*) FROM registrations GROUP BY slot_id;
```

---

## 4. The Migration Protocol
Manual `ALTER TABLE` commands are strictly prohibited in the production environment. 

* **Traceability:** Every schema change is linked to a specific migration file and timestamp.
* **Safety (Rollbacks):** If a structural change causes a regression, the schema can be reverted to a "Last Known Good" state with a single command.
* **Environment Parity:** Guarantees that the Local, Staging, and Production databases are structurally identical.
