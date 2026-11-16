# TrackMyCourse — Authentication & Security Architecture

## 1. Overview

TrackMyCourse provides user authentication and session management built on `flask-login` and `werkzeug.security`.

---

## 2. Authentication Flow

1. **User Registration** (`/register`):
   - Accepts `full_name`, `username`, `email`, `password`, `university_id`, and `program_id`.
   - Validates email uniqueness and password length (minimum 6 characters).
   - Generates a salted PBKDF2 password hash.
   - Automatically initializes a `StudentProfile` and `StudentEnrollment` for the user.
   - Automatically signs the student in upon successful registration.

2. **User Login** (`/login`):
   - Accepts `email`, `password`, and optional `remember_me`.
   - Validates password hash with `werkzeug.security.check_password_hash`.
   - Checks account status (`is_active`).
   - Dispatches administrators to `/admin` and students to `/dashboard`.

3. **User Logout** (`/logout`):
   - Clears the session cookie via `logout_user()` and redirects to `/`.

---

## 3. Pre-Seeded Primary Accounts

To facilitate immediate verification and maintain compatibility with pre-existing user progress data:

| Role | Email | Password | User ID | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | `student@trackmycourse.edu` | `student123` | `1` | Primary scholar account holding pre-existing completion records (~88% in ASE, ~78% in Maths, ~79% in AI). |
| **Administrator** | `admin@trackmycourse.edu` | `admin123` | `2` | Privileged account with access to the Admin Portal, document uploads, and syllabus verification. |

---

## 4. Multi-User Isolation Safeguards

- **Progress Scoping**: All mutations and reads in `/api/progress` explicitly filter by `UserProgress.user_id == current_user.id` (or fallback to student ID 1 in unauthenticated mode).
- **Data Leak Prevention**: Eliminates previous flaws where `GET /api/progress/<course_id>` queried across all users without user ID constraints.
- **CSRF & Form Validation**: Protected form submissions and sanitized user input across all endpoints.
