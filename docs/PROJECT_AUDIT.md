# TrackMyCourse — Comprehensive Project Audit (Phase 0)

**Date of Audit**: November 16, 2026  
**Project Path**: `D:\trackmycourse`  
**Auditor**: Senior Engineering Team (Antigravity)  
**Primary Target Branch**: `main`  
**Preserved Personal Branch**: `personal-mode`

---

## 1. Executive Summary

TrackMyCourse is a Flask-based academic progress management and learning organization platform. Prior to this engineering audit, the project existed in two divergent states:
1. `main` (commit `7ee9218`): The core multi-tier academic selection hierarchy and checkbox-based topic progress tracking application.
2. `personal-mode` (commit `515c79c` / preserved at `545f011`): A personalized MCA S1/S2 study tracking workspace featuring local filesystem integration, file viewers, and course-specific trackers.

This audit establishes a complete technical assessment of the existing codebase, documents the verified Git recovery points, inventories database contents, identifies strengths, vulnerabilities, and technical debt, and lays out the step-by-step implementation strategy for transforming TrackMyCourse into a production-grade academic management system.

---

## 2. Git State & Branch Management

### 2.1 Branch Audit
- **`main`**: The canonical product branch. Verified at commit `7ee921834d5f34fa1184ecb338a6d0d3aab8d2e2`.
- **`personal-mode`**: Branch created off `7ee9218` with custom local filesystem explorer and personal MCA tracker. Working-tree modifications were committed cleanly to `545f011a707b0d935c58f1c04b47b49c05f8905a` and pushed to remote `origin/personal-mode`. Per Rule 3.1, this branch remains 100% isolated, intact, and protected.
- **`backup/main-before-rebuild-2026-11-16`**: Created directly at `7ee921834d5f34fa1184ecb338a6d0d3aab8d2e2` and pushed to `origin`.
- **`trackmycourse-pre-rebuild-2026-11-16`**: Annotated Git tag created at `7ee921834d5f34fa1184ecb338a6d0d3aab8d2e2` and verified on `origin`.

### 2.2 Remote Configuration
- **Remote Origin**: `https://github.com/karthikcmani/trackmycourse.git` (both fetch and push).
- Verification confirmed via `git ls-remote --heads --tags origin`:
  - `refs/heads/main`: `7ee9218...`
  - `refs/heads/backup/main-before-rebuild-2026-11-16`: `7ee9218...`
  - `refs/heads/personal-mode`: `545f011...`
  - `refs/tags/trackmycourse-pre-rebuild-2026-11-16`: points to commit `7ee9218...`

---

## 3. Database & Persistence Audit

### 3.1 SQLite Database Location & State
- Database File: `instance/trackmycourse.db`
- File Size: 65,536 bytes (64 KB)
- Verified Backup: `backups/trackmycourse_backup_2026-11-16_220500.db`

### 3.2 Existing Schema Inventory
The existing schema comprises 10 tables:
1. `user`: Columns (`id`, `email`, `password_hash`). Current rows: 0.
2. `university`: Columns (`id`, `name`). Current rows: 1 (`KTU`).
3. `program`: Columns (`id`, `name`, `university_id`). Current rows: 2 (`MCA`, `BTech`).
4. `stream`: Columns (`id`, `name`, `program_id`). Current rows: 1 (`Computer Science & Engineering`).
5. `scheme`: Columns (`id`, `year`, `program_id`, `stream_id`). Current rows: 3 (`MCA 2021`, `BTech CSE 2019`, `BTech CSE 2024`).
6. `semester`: Columns (`id`, `semester_no`, `scheme_id`). Current rows: 6 (Semesters 1-2 across the schemes).
7. `course`: Columns (`id`, `name`, `semester_id`). Current rows: 6.
8. `module`: Columns (`id`, `name`, `hours`, `course_id`). Current rows: 20.
9. `topic`: Columns (`id`, `name`, `module_id`). Current rows: 247.
10. `user_progress`: Columns (`id`, `user_id`, `topic_id`, `completed`). Current rows: 142.

### 3.3 Course-Level Content & Completion Analysis
Analysis of existing data in `instance/trackmycourse.db`:
- **Course 1**: Digital Fundamentals & Computer Architecture (MCA S1) — 0 topics, 0 completed (0.0%).
- **Course 2**: Programming in C (BTech CSE S1) — 0 topics, 0 completed (0.0%).
- **Course 3**: Mathematical Foundations for Computing (MCA S1) — 51 topics, 40 completed (78.4%).
- **Course 4**: Advanced Database Management Systems (MCA S2) — 61 topics, 31 completed (50.8%).
- **Course 5**: Advanced Computer Networks (MCA S2) — 82 topics, 28 completed (34.1%).
- **Course 6**: Artificial Intelligence (MCA S2) — 53 topics, 42 completed (79.2%).

### 3.4 Regression Scenario: Advanced Software Engineering (ASE)
- In addition to the database courses above, `seed_ase.py` defines the official syllabus for **Advanced Software Engineering** (Course under MCA S1) containing 5 modules and 49 topics.
- The regression testing scenario specified in the prompt requires that KTU → MCA → Scheme 2021 → Semester 1 → Advanced Software Engineering displays correctly with modules and topics, and tracks progress up to ~88% (~43 of 49 topics).

---

## 4. Codebase & Architectural Analysis

### 4.1 Backend Architecture (`app.py`, `models.py`, `api.py`)

#### Strengths
- Uses Flask, Flask-SQLAlchemy, and Flask-Login.
- Decoupled API routes in a Flask Blueprint (`api.py`).
- Clear normalized relational hierarchy for academic data: `University` → `Program` → `Stream` → `Scheme` → `Semester` → `Course` → `Module` → `Topic`.
- Support for optional streams (e.g., MCA has no stream, whereas BTech has CSE stream).

#### Deficiencies & Vulnerabilities
1. **Application Initialization Clutter**:
   - `app.py` instantiates `Flask(__name__)` and defines `app.secret_key` twice.
   - Hardcoded secret key (`"super-secret-key"`).
   - `db.create_all()` executed directly in global startup instead of manageable database migrations.
2. **API Blueprint Duplication & Flaws (`api.py`)**:
   - `Blueprint("api", __name__, url_prefix="/api")` is declared twice.
   - Hardcoded `user_id = 1` in `/api/progress` (both GET and POST).
   - In `GET /api/progress/<int:course_id>`, the query joins `UserProgress` to `Topic` and `Module` on `Module.course_id == course_id`, but **fails to filter by `user_id`**! This would cause progress data from all users to leak together.
   - Lack of parameter validation and error responses; missing arguments cause unhandled 500 errors.
   - Returns unauthenticated JSON even on mutating endpoints.
3. **User & Security Deficiencies (`models.py`)**:
   - `User` model only has `id`, `email`, `password_hash`. No role, full name, timestamps, or profile fields.
   - No authentication routes exist (no `/register`, `/login`, `/logout`).
   - No session protection or CSRF handling for forms.
   - `UserProgress` lacks unique constraint on `(user_id, topic_id)` and lacks an `updated_at` timestamp.
4. **Missing Student & Organizational Models**:
   - No models for:
     - `StudentProfile` / `StudentEnrollment` (saving a student's active university, program, semester)
     - `StudyTask` / `StudySession` (tracking study time and planned tasks)
     - `StudentNote` (course/topic-specific personal notes)
     - `LearningResource` (organized syllabus links/materials)
     - `AcademicGoal` and `ActivityLog`

### 4.2 Frontend Architecture (`templates/index.html`)

#### Strengths
- Clean dependent dropdown cascade: University → Program → Stream → Scheme → Semester → Course.
- Dynamic DOM generation of modules and topics with checkboxes.
- Immediate client-side progress calculation and progress bar rendering.
- Async `fetch` integration saving checkbox states immediately to the backend.

#### Deficiencies
- All HTML, CSS, and JavaScript are bundled in a single file (`templates/index.html`) without reusable stylesheets or modular scripts.
- Edge case bug: if a course has 0 topics, `Math.round((done / total) * 100)` evaluates `0 / 0` yielding `NaN%`.
- Lack of error boundaries: if an API call fails or the server drops, no error toast or retry indicator is shown.
- Missing responsive navigation bar, authentication status indicator, student profile drawer, or access to other academic features (Planner, Notes, Analytics).

---

## 5. Detailed Component Categorization

| Component | Status | Action Required |
| :--- | :--- | :--- |
| **Academic Hierarchy API** | Working | Preserve API contract, add input validation & error handling. |
| **Course & Topic Selection UI** | Working | Preserve exact behavior, enhance styling, eliminate `NaN%` edge case. |
| **Progress Persistence API** | Partially Implemented | Make user-aware, filter by authenticated user, enforce authorization. |
| **User Authentication** | Missing | Implement registration, login, logout, password hashing, and role-based access. |
| **Student Profile & Enrollment** | Missing | Add enrollment model to associate student with active university, program, and semester. |
| **Student Dashboard** | Missing | Build dashboard surfacing enrolled courses, overall completion, recent activity, and study metrics. |
| **Study Planner & Sessions** | Missing | Build task management, study time logging, and calendar/schedule organization. |
| **Student Notes & Resources** | Missing | Create private note-taking and resource bookmarking associated with courses and topics. |
| **Academic Analytics** | Missing | Calculate genuine completion percentages, weekly study activity, and consistency metrics. |
| **Admin Academic Management** | Missing | Build administrative views for managing universities, programs, schemes, courses, and syllabi safely. |
| **Database Migrations** | Missing | Introduce Flask-Migrate / Alembic for non-destructive schema evolution. |
| **Automated Testing Suite** | Missing | Implement pytest test suite covering academic hierarchy, syllabus retrieval, progress tracking, and auth. |

---

## 6. Implementation Strategy & Next Steps

1. **Phase 1 — Foundation & Database Architecture**:
   - Introduce Flask-Migrate / Alembic for schema migrations.
   - Refactor `models.py` cleanly to support `User`, `Role`, `StudentEnrollment`, `StudySession`, `StudyTask`, `StudentNote`, `LearningResource`, `AcademicGoal`, and `ActivityLog`.
   - Ensure backward compatibility with existing SQLite database so zero data is lost.
   - Document in `docs/DATABASE_DESIGN.md`.

2. **Phase 2 — Authentication & Security**:
   - Implement Flask-Login authentication handlers, password hashing with Werkzeug, secure session cookies.
   - Provide registration, login, and profile management views.
   - Protect all personal progress and organizational endpoints.

3. **Phase 3 — Academic Data Management & Idempotent Seeding**:
   - Implement idempotent seeding (detect existing entities before insert, preventing duplicates).
   - Ensure KTU MCA S1/S2 and BTech syllabi (including ASE, Maths, ADS, DBMS, ACN, AI) can be seeded reliably.

4. **Phase 4 — Course Progress System & Regression Verification**:
   - Preserve `templates/index.html` structure and API endpoints.
   - Ensure progress is strictly scoped to the logged-in student.
   - Verify the regression scenario for KTU → MCA → Scheme 2021 → Semester 1 → Advanced Software Engineering.

5. **Phases 5 through 10**:
   - Systematically implement the Student Dashboard, Study Planner, Notes, Resources, Analytics, Admin Management, QA/Testing suite, and Deployment configuration.
