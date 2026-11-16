# TrackMyCourse 🎓

> **A unified, production-quality academic progress management and learning organization platform.**

TrackMyCourse enables university students and scholars to explore their university curriculum, track granular topic-level syllabus completion, organize study sessions, set deadlines, write revision notes, and monitor authentic academic insights over time.

---

## Key Features

1. **Academic Selection Cascade (Preserved Core Workflow)**:
   - Dynamic dependent dropdown selection: `University` &rarr; `Program` &rarr; `Stream` &rarr; `Scheme` &rarr; `Semester` &rarr; `Course`.
   - Real-time syllabus rendering with contact hours and interactive module-wise topics.
   - Animated progress percentage and progress bar calculation (zero-division safe; never shows `NaN%`).
   - Regression-verified for **KTU &rarr; MCA &rarr; Scheme 2021 &rarr; Semester 1 &rarr; Advanced Software Engineering** (~88% completion).

2. **Multi-User Authentication & Isolation**:
   - Secure student registration, login, logout, and profile management with salted password hashing (`werkzeug.security`).
   - Strict progress scoping enforcing that each student's progress is private and isolated.

3. **Student Workspace & Dashboard**:
   - Live dashboard presenting enrolled course progress, total vs. remaining topics, logged study hours, and 7-day consistency graphs.
   - All numbers are computed from database records; zero mock percentages or artificial history.

4. **Study Planner & Learning Time Tracker**:
   - Interactive study task planner with priorities, deadlines, and overdue detection.
   - Study session logger tracking exact duration in minutes for authentic study analytics.

5. **Personal Student Notes & Resources**:
   - Course- and topic-linked revision note editor.
   - Curated learning materials and resource bookmarks categorized by type (PDF, Video, Article, GitHub, Book).

6. **Academic Goals**:
   - Measurable syllabus completion milestone tracking.

7. **Official Curriculum Ingestion & Invariant Provenance**:
   - Multi-format syllabus parser supporting **PDF, DOCX, XLSX, CSV, and JSON**.
   - Admin upload and preview workflow with one-click approval into the shared academic catalogue.
   - Transparent primary source provenance citations for all official curricula.

---

## Technology Stack

- **Backend**: Python 3.13, Flask 3.1, Flask-SQLAlchemy 3.1, Flask-Login 0.6, Werkzeug 3.1
- **Database**: SQLite (Development) / PostgreSQL-Ready (Production via SQLAlchemy ORM)
- **Document Parsers**: `pypdf`, `python-docx`, `openpyxl`
- **Testing**: `pytest`
- **Frontend**: HTML5, CSS3 Variables, Vanilla JavaScript (Refined design system based on the `personal-mode` visual language)

---

## Installation & Running

### 1. Prerequisites
- Python 3.10+
- PowerShell or standard terminal

### 2. Setup Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Initialize Database & Seed Academic Catalog
```powershell
.\venv\Scripts\python.exe migrate_db.py
.\venv\Scripts\python.exe seed_academic_catalog.py
```

### 4. Run Automated QA Tests
```powershell
.\venv\Scripts\python.exe -m pytest tests/ -v
```

### 5. Launch Application
```powershell
.\venv\Scripts\python.exe app.py
```

Visit the platform in your browser at `http://127.0.0.1:5000/`.

---

## Default Verified Accounts

| Role | Email | Password | User ID | Features Accessible |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | `student@trackmycourse.edu` | `student123` | `1` | Dashboard, Course Progress, Study Planner, Notes, Resources, Goals, Analytics |
| **Admin** | `admin@trackmycourse.edu` | `admin123` | `2` | Admin Portal, Syllabus Document Ingestion (PDF/DOCX), Source Provenance, User Management |

---

## Project Structure

```
d:\trackmycourse\
├── app.py                      # Flask Application Factory & Route Dispatcher
├── models.py                   # 20 Relational Models with cascade & integrity rules
├── api.py                      # Academic Hierarchy & User Progress REST APIs
├── auth.py                     # Authentication, Registration & Profile Blueprint
├── study_api.py                # Study Tasks, Sessions, Notes, Resources & Goals
├── analytics_api.py            # Analytics Computation & Weekly Metrics
├── admin_api.py                # Syllabus Document Upload & Extraction Pipeline
├── syllabus_parser.py          # Intelligent Parser for PDF, DOCX, XLSX, JSON
├── migrate_db.py               # Safe Non-Destructive Database Migration
├── seed_academic_catalog.py    # Idempotent Academic Catalog & Regression Seeder
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Exclusion Rules
├── tests/
│   └── test_trackmycourse.py   # Comprehensive Pytest Automated Suite
├── templates/
│   ├── base.html               # Master Layout & Sidebar Navigation
│   ├── index.html              # Preserved Core Course Progress Page
│   ├── home.html               # Landing Overview Page
│   ├── dashboard.html          # Student Dashboard
│   ├── academics.html          # Academic Catalog & Provenance Registry
│   ├── planner.html            # Study Tasks & Session Logger
│   ├── notes.html              # Personal Revision Notes
│   ├── resources.html          # Learning Resource Links
│   ├── goals.html              # Academic Milestone Goals
│   ├── analytics.html          # Progress Analytics & Consistency Charts
│   ├── profile.html            # Student Profile & Enrollment Settings
│   ├── auth/
│   │   ├── login.html          # Sign In View
│   │   └── register.html       # Account Registration View
│   └── admin/
│       └── admin.html          # Administration & Ingestion Portal
├── docs/                       # Complete Engineering Documentation
└── backups/                    # Timestamped Database Backups
```

---

## Git Branches

- **`main`**: The canonical production engineering branch.
- **`personal-mode`**: Preserved isolated branch with personal MCA S1 ADS tracker and local file sidebar. Completely untouched and protected.
- **`backup/main-before-rebuild-2026-11-16`**: Pre-rebuild recovery branch verified on remote `origin`.
