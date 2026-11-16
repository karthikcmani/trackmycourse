# TrackMyCourse — Database Architecture & Schema Specification

## 1. Relational Entity Overview

The TrackMyCourse database is partitioned into three logical domains:
1. **Academic Catalogue Data** (Reusable public entities)
2. **Student Workspace Data** (Private user entities)
3. **Curriculum Ingestion & Provenance** (Source verification entities)

```
                            Entity Relationship Diagram
                            
 [University]
      │ 1:N
 [Program]
      │ 1:N
 [Stream] (Optional)
      │ 1:N
  [Scheme]
      │ 1:N
 [Semester]
      │ 1:N
  [Course] ──< [SyllabusSource]
      │ 1:N
  [Module]
      │ 1:N
  [Topic] <────┐ 1:N
               │
 [User] ───────┼─> [UserProgress] (Unique: user_id + topic_id)
   │ 1:1       │
   ├─> [StudentProfile]
   ├─> [StudentEnrollment]
   ├─> [StudyTask]
   ├─> [StudySession]
   ├─> [StudentNote]
   ├─> [LearningResource]
   ├─> [AcademicGoal]
   └─> [ActivityLog]
```

---

## 2. Table Specifications

### 2.1 Academic Hierarchy Tables
- **`university`**: `id` (PK), `name`, `code`, `state`, `country`, `website`, `created_at`
- **`program`**: `id` (PK), `name`, `code`, `degree_type`, `university_id` (FK)
- **`stream`**: `id` (PK), `name`, `code`, `program_id` (FK)
- **`scheme`**: `id` (PK), `year`, `program_id` (FK), `stream_id` (FK, nullable)
- **`semester`**: `id` (PK), `semester_no`, `scheme_id` (FK)
- **`course`**: `id` (PK), `name`, `code`, `credits`, `semester_id` (FK), `is_elective`, `course_type`
- **`module`**: `id` (PK), `name`, `module_no`, `hours`, `course_id` (FK)
- **`topic`**: `id` (PK), `name`, `topic_no`, `module_id` (FK)

### 2.2 Student Workspace Tables
- **`user`**: `id` (PK), `email` (Unique), `username` (Unique), `password_hash`, `full_name`, `role`, `is_active`, `created_at`
- **`student_profile`**: `id` (PK), `user_id` (FK, Unique), `enrollment_no`, `college_name`, `current_semester`, `target_graduation_year`, `bio`, `created_at`
- **`student_enrollment`**: `id` (PK), `user_id` (FK), `university_id` (FK), `program_id` (FK), `stream_id` (FK), `scheme_id` (FK), `current_semester_id` (FK), `enrolled_at`, `is_active`
- **`user_progress`**: `id` (PK), `user_id` (FK), `topic_id` (FK), `completed` (Boolean), `updated_at`. **Constraint**: `UNIQUE(user_id, topic_id)`
- **`study_task`**: `id` (PK), `user_id` (FK), `course_id` (FK), `topic_id` (FK), `title`, `description`, `due_date`, `priority`, `status`, `completed_at`, `created_at`
- **`study_session`**: `id` (PK), `user_id` (FK), `course_id` (FK), `topic_id` (FK), `session_date`, `start_time`, `duration_minutes`, `notes`, `created_at`
- **`student_note`**: `id` (PK), `user_id` (FK), `course_id` (FK), `module_id` (FK), `topic_id` (FK), `title`, `content`, `created_at`, `updated_at`
- **`learning_resource`**: `id` (PK), `user_id` (FK, nullable for public items), `course_id` (FK), `topic_id` (FK), `title`, `url`, `resource_type`, `is_official`, `created_at`
- **`academic_goal`**: `id` (PK), `user_id` (FK), `course_id` (FK), `title`, `description`, `target_percentage`, `current_percentage`, `target_date`, `status`, `created_at`
- **`activity_log`**: `id` (PK), `user_id` (FK), `activity_type`, `description`, `reference_id`, `created_at`

### 2.3 Provenance & Ingestion Tables
- **`syllabus_source`**: `id` (PK), `university_id` (FK), `program_id` (FK), `scheme_id` (FK), `course_id` (FK), `document_title`, `source_url`, `publication_date`, `retrieval_date`, `verification_status`, `version`, `verified_by`, `notes`
- **`syllabus_import`**: `id` (PK), `filename`, `original_filename`, `file_type`, `source_doc_title`, `university_id` (FK), `program_id` (FK), `scheme_id` (FK), `status`, `extracted_data_json`, `uploaded_by_user_id` (FK), `is_public`, `created_at`, `reviewed_at`, `review_notes`

---

## 3. Migration & Non-Destructive Invariance

The migration script (`migrate_db.py`) enforces:
1. `PRAGMA table_info` checks before executing any `ALTER TABLE ... ADD COLUMN` statements.
2. Zero data loss for pre-existing records (all 142 completion records in `instance/trackmycourse.db` were safely retained).
3. Backups preserved in `backups/trackmycourse_backup_2026-11-16_220500.db` and `backups/trackmycourse_pre_phase1_2026-11-16.db`.
