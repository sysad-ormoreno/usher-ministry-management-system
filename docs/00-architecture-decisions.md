# 00-architecture-decisions.md

## Data Management Strategy
This table defines our hybrid approach to database interactions to ensure a balance between development speed and system performance.

| Task | Methodology | Why? |
| :--- | :--- | :--- |
| **Basic CRUD** | ORM (SQLAlchemy) | Faster and safer for standard Create, Read, Update, Delete operations. |
| **Complex Reporting** | Raw SQL / Stored Procs | Handles heavy "math" and data aggregation inside the database for better performance. |
| **Schema Changes** | Migrations (Alembic) | Version-controlled files ensure every developer's local database stays in sync. |

---

### Quick Reference: When to use what?

    # Use the ORM for simple lookups (Pythonic)
    user = db.query(User).filter(User.phone == "0917...").first()

    # Use Raw SQL for heavy statistics (Performance)
    stats = db.execute("SELECT slot_id, COUNT(*) FROM registrations GROUP BY slot_id")

---

### 1. The "Why" behind Migrations
We don't manually run `CREATE TABLE` commands in the production database. Instead, we use **Migrations**. 
- **Traceability:** We can see exactly who changed a column name and when.
- **Rollback:** If a database change breaks the app, we can "undo" the schema change with one command.
- **Consistency:** Ensures the database in your local environment matches the one on the server.
