# TrackMyCourse — REST API Documentation

Base URL: `/api`

---

## 1. Academic Hierarchy & Syllabus Endpoints

### 1.1 List Universities
- **Route**: `GET /api/universities`
- **Response**:
```json
[
  {
    "id": 1,
    "name": "APJ Abdul Kalam Technological University",
    "code": "KTU",
    "state": "Kerala"
  }
]
```

### 1.2 List Programs
- **Route**: `GET /api/programs?university_id={id}`
- **Response**:
```json
[
  {
    "id": 1,
    "name": "MCA",
    "code": "MCA",
    "degree_type": "Postgraduate"
  }
]
```

### 1.3 List Schemes
- **Route**: `GET /api/schemes?program_id={id}&stream_id={opt_id}`
- **Response**:
```json
[
  {
    "id": 1,
    "year": "2020"
  }
]
```

### 1.4 List Semesters
- **Route**: `GET /api/semesters?scheme_id={id}`
- **Response**:
```json
[
  {
    "id": 1,
    "semester_no": 1
  }
]
```

### 1.5 List Courses
- **Route**: `GET /api/courses?semester_id={id}`
- **Response**:
```json
[
  {
    "id": 7,
    "name": "Advanced Software Engineering",
    "code": "20MCA105",
    "credits": 4,
    "course_type": "Theory"
  }
]
```

### 1.6 Course Syllabus & Topics
- **Route**: `GET /api/syllabus?course_id={id}`
- **Response**:
```json
[
  {
    "id": 1,
    "module": "Module 1",
    "module_no": 1,
    "hours": 8,
    "topics": [
      {
        "id": 1,
        "name": "Introduction to Software Engineering and characteristics of software",
        "topic_no": 1
      }
    ]
  }
]
```

---

## 2. Progress Persistence Endpoints

### 2.1 Save Topic Completion
- **Route**: `POST /api/progress`
- **Body**:
```json
{
  "topic_id": 1,
  "completed": true
}
```
- **Response**:
```json
{
  "status": "saved",
  "topic_id": 1,
  "completed": true,
  "user_id": 1
}
```

### 2.2 Load Course Progress
- **Route**: `GET /api/progress/{course_id}`
- **Response**:
```json
[
  {
    "topic_id": 1,
    "completed": true
  }
]
```

### 2.3 Course Summary Analytics
- **Route**: `GET /api/course-summary/{course_id}`
- **Response**:
```json
{
  "course_id": 7,
  "course_name": "Advanced Software Engineering",
  "course_code": "20MCA105",
  "credits": 4,
  "total_topics": 49,
  "completed_topics": 43,
  "remaining_topics": 6,
  "percentage": 87.8
}
```

---

## 3. Study Organization Endpoints (`/api/study`)

- `GET /api/study/tasks` — List study tasks (filter: `?status=pending|completed`)
- `POST /api/study/tasks` — Create new study task
- `POST /api/study/tasks/{id}/toggle` — Toggle task completion status
- `DELETE /api/study/tasks/{id}` — Delete task
- `GET /api/study/sessions` — List study sessions
- `POST /api/study/sessions` — Log new study session with duration in minutes
- `GET /api/study/notes` — List student revision notes (filter: `?course_id=`)
- `POST /api/study/notes` — Create note
- `PUT /api/study/notes/{id}` — Update note
- `DELETE /api/study/notes/{id}` — Delete note
- `GET /api/study/resources` — List learning resources
- `POST /api/study/resources` — Save learning resource link
- `DELETE /api/study/resources/{id}` — Remove resource
- `GET /api/study/goals` — List active academic goals
- `POST /api/study/goals` — Set new academic goal

---

## 4. Analytics Endpoints (`/api/analytics`)

- `GET /api/analytics/dashboard` — Live computed dashboard data: overall percentage, total topics, completed topics, remaining topics, study hours, enrolled course cards, 7-day study minutes, and recent activity log.

---

## 5. Administration Endpoints (`/api/admin`)

- `POST /api/admin/syllabus/upload` — Multipart file upload (PDF/DOCX/XLSX/JSON) returning parsed academic JSON preview.
- `GET /api/admin/syllabus/preview/{import_id}` — Retrieve extracted syllabus preview.
- `POST /api/admin/syllabus/publish/{import_id}` — Approve and idempotently publish extracted syllabus into the live academic catalogue.
- `GET /api/admin/sources` — List verified provenance sources and primary document citations.
- `GET /api/admin/users` — List user accounts.
- `POST /api/admin/users/{id}/toggle-role` — Toggle user role (`student` <-> `admin`).
- `POST /api/admin/users/{id}/toggle-status` — Enable / disable account.
