# TrackMyCourse — Production Deployment Guide

## 1. Environment Configuration

TrackMyCourse is configured to run on standard WSGI application servers (e.g., Gunicorn, Waitress) with support for PostgreSQL or SQLite.

### Recommended Environment Variables:

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `SECRET_KEY` | Cryptographic secret key for session cookies. | `os.environ.get("SECRET_KEY")` |
| `DATABASE_URL` | SQLAlchemy database connection URI. | `sqlite:///instance/trackmycourse.db` (or `postgresql://user:pass@host:5432/trackmycourse`) |
| `FLASK_ENV` | Application environment. | `production` |
| `PORT` | Listening network port. | `5000` |

---

## 2. Running Locally for Development

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run database migration and seeding
.\venv\Scripts\python.exe migrate_db.py
.\venv\Scripts\python.exe seed_academic_catalog.py

# 3. Start development server
.\venv\Scripts\python.exe app.py
```

Access in your browser at:
`http://127.0.0.1:5000/`

---

## 3. Running in Production with Gunicorn

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 "app:create_app()"
```

---

## 4. PostgreSQL Migration Strategy

TrackMyCourse uses SQLAlchemy ORM without raw SQLite-specific SQL:
1. Provision a PostgreSQL instance.
2. Set `DATABASE_URL=postgresql://username:password@db-host:5432/trackmycourse`.
3. Run `python migrate_db.py` to create schema.
4. Run `python seed_academic_catalog.py` to populate official base academic data.
