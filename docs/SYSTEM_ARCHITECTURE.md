# TrackMyCourse — System Architecture

## 1. Architectural Overview

TrackMyCourse is built as a modular, production-ready web platform on Python, Flask, Flask-SQLAlchemy, and Flask-Login, with SQLite as the default development database and built-in PostgreSQL readiness for production environments.

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT TIER                                       |
|  Responsive Web Interface (Modern Slate Theme based on personal-mode design)      |
|  Vanilla JS • Modular Fetch API • Dynamic Hierarchy Cascade • CSS Variables       |
+-----------------------------------------------------------------------------------+
                                        | (HTTPS / REST)
+-----------------------------------------------------------------------------------+
|                             APPLICATION LAYER (Flask)                             |
|                                                                                   |
|  [Core App Factory: app.py]                                                       |
|  ├── Blueprints:                                                                  |
|  │   ├── auth.py         -> Registration, Login, Logout, Profile                  |
|  │   ├── api.py          -> Academic Hierarchy & User Progress Persistence        |
|  │   ├── study_api.py    -> Study Tasks, Study Sessions, Notes, Resources, Goals  |
|  │   ├── analytics_api.py-> Real Metrics, Course Summaries, 7-Day Activity Chart  |
|  │   └── admin_api.py    -> Curriculum Ingestion, Preview & User Admin            |
|  │                                                                                |
|  ├── Ingestion Engine: syllabus_parser.py (pypdf, python-docx, openpyxl)          |
|  └── Data Layer: models.py (20 relational models with cascade & index rules)      |
+-----------------------------------------------------------------------------------+
                                        | (SQLAlchemy ORM)
+-----------------------------------------------------------------------------------+
|                                PERSISTENCE LAYER                                  |
|  SQLite (instance/trackmycourse.db)  |  PostgreSQL Ready (DATABASE_URL)           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Component Design

### 2.1 Web Route Controllers (`app.py`)
- `/` — Product homepage and feature overview.
- `/dashboard` — Live student dashboard summarizing enrolled courses, completion percentages, 7-day study consistency, and upcoming tasks.
- `/progress` — Preserved and refined core course progress page featuring the complete dependent dropdown cascade and animated topic completion checkboxes.
- `/ui` — Backward-compatible redirect to `/progress`.
- `/academics` — Public verified academic catalogue and primary source provenance registry.
- `/planner` — Interactive study task planner and study session time-logger.
- `/notes` — Topic-linked student revision note keeper.
- `/resources` — Curated learning materials and resource bookmarks.
- `/goals` — Measurable academic milestone management.
- `/analytics` — Course-by-course analytics and completion ratio visualizations.
- `/admin` — Administration portal for syllabus document extraction, preview, publication, and user management.

### 2.2 Security & Authentication (`auth.py`)
- Password hashing using Werkzeug's salted PBKDF2/SHA-256 algorithm.
- Cookie-based session authentication with `remember_me` support.
- Role-based authorization (`student`, `admin`) protecting administration endpoints.
- User-isolated progress queries enforcing that student A can never read or mutate student B's progress.

### 2.3 Document Ingestion Engine (`syllabus_parser.py`)
- Multi-format extraction: PDF (via `pypdf`), DOCX (via `python-docx`), and XLSX/CSV (via `openpyxl`).
- Natural language and regex parsing identifying course titles, codes, module/unit numbers, contact hours, and individual topics.
- Pre-publication preview and administrative approval workflow before publishing to the shared catalogue.
