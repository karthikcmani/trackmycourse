import os
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ============================================================================
# 1. USER & AUTHENTICATION
# ============================================================================

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default="student", nullable=False)  # student | admin
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile = db.relationship("StudentProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    enrollments = db.relationship("StudentEnrollment", backref="user", lazy=True, cascade="all, delete-orphan")
    progress_records = db.relationship("UserProgress", backref="user", lazy=True, cascade="all, delete-orphan")
    tasks = db.relationship("StudyTask", backref="user", lazy=True, cascade="all, delete-orphan")
    sessions = db.relationship("StudySession", backref="user", lazy=True, cascade="all, delete-orphan")
    notes = db.relationship("StudentNote", backref="user", lazy=True, cascade="all, delete-orphan")
    resources = db.relationship("LearningResource", backref="user", lazy=True, cascade="all, delete-orphan")
    goals = db.relationship("AcademicGoal", backref="user", lazy=True, cascade="all, delete-orphan")
    activities = db.relationship("ActivityLog", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"


class StudentProfile(db.Model):
    __tablename__ = "student_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    enrollment_no = db.Column(db.String(50), nullable=True)
    college_name = db.Column(db.String(150), nullable=True)
    current_semester = db.Column(db.Integer, default=1)
    target_graduation_year = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentEnrollment(db.Model):
    __tablename__ = "student_enrollment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id"), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"), nullable=False)
    stream_id = db.Column(db.Integer, db.ForeignKey("stream.id"), nullable=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey("scheme.id"), nullable=False)
    current_semester_id = db.Column(db.Integer, db.ForeignKey("semester.id"), nullable=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


# ============================================================================
# 2. ACADEMIC HIERARCHY
# ============================================================================

class University(db.Model):
    __tablename__ = "university"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), default="India")
    website = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    programs = db.relationship("Program", backref="university", lazy=True, cascade="all, delete-orphan")


class Program(db.Model):
    __tablename__ = "program"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), nullable=True)
    degree_type = db.Column(db.String(50), default="Postgraduate")
    university_id = db.Column(db.Integer, db.ForeignKey("university.id"), nullable=False)

    streams = db.relationship("Stream", backref="program", lazy=True, cascade="all, delete-orphan")
    schemes = db.relationship("Scheme", backref="program", lazy=True, cascade="all, delete-orphan")


class Stream(db.Model):
    __tablename__ = "stream"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(30), nullable=True)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"), nullable=False)

    schemes = db.relationship("Scheme", backref="stream", lazy=True)


class Scheme(db.Model):
    __tablename__ = "scheme"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(20), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"), nullable=False)
    stream_id = db.Column(db.Integer, db.ForeignKey("stream.id"), nullable=True)

    semesters = db.relationship("Semester", backref="scheme", lazy=True, cascade="all, delete-orphan")


class Semester(db.Model):
    __tablename__ = "semester"

    id = db.Column(db.Integer, primary_key=True)
    semester_no = db.Column(db.Integer, nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey("scheme.id"), nullable=False)

    courses = db.relationship("Course", backref="semester", lazy=True, cascade="all, delete-orphan")


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(30), nullable=True)
    credits = db.Column(db.Integer, default=4)
    semester_id = db.Column(db.Integer, db.ForeignKey("semester.id"), nullable=False)
    is_elective = db.Column(db.Boolean, default=False)
    course_type = db.Column(db.String(50), default="Theory")

    modules = db.relationship("Module", backref="course", lazy=True, cascade="all, delete-orphan")
    notes = db.relationship("StudentNote", backref="course", lazy=True)
    resources = db.relationship("LearningResource", backref="course", lazy=True)


class Module(db.Model):
    __tablename__ = "module"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    module_no = db.Column(db.Integer, nullable=True)
    hours = db.Column(db.Integer, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    topics = db.relationship("Topic", backref="module", lazy=True, cascade="all, delete-orphan")


class Topic(db.Model):
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    topic_no = db.Column(db.Integer, nullable=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)

    progress_records = db.relationship("UserProgress", backref="topic", lazy=True, cascade="all, delete-orphan")


# ============================================================================
# 3. PROVENANCE, SYLLABUS SOURCES & DOCUMENT IMPORTS
# ============================================================================

class SyllabusSource(db.Model):
    __tablename__ = "syllabus_source"

    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id"), nullable=True)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"), nullable=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey("scheme.id"), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    document_title = db.Column(db.String(250), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)
    publication_date = db.Column(db.String(50), nullable=True)
    retrieval_date = db.Column(db.DateTime, default=datetime.utcnow)
    verification_status = db.Column(db.String(40), default="verified")  # verified | pending_verification | superseded | unverified
    version = db.Column(db.String(20), default="1.0")
    verified_by = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)


class SyllabusImport(db.Model):
    __tablename__ = "syllabus_import"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(250), nullable=False)
    original_filename = db.Column(db.String(250), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # pdf | docx | xlsx | json
    source_doc_title = db.Column(db.String(250), nullable=True)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id"), nullable=True)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"), nullable=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey("scheme.id"), nullable=True)
    status = db.Column(db.String(40), default="draft")  # draft | preview | verified | published | rejected
    extracted_data_json = db.Column(db.Text, nullable=True)
    uploaded_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_notes = db.Column(db.Text, nullable=True)


# ============================================================================
# 4. STUDENT PROGRESS TRACKING
# ============================================================================

class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "topic_id", name="uq_user_topic_progress"),
    )


# ============================================================================
# 5. STUDY PLANNER & TIME TRACKING
# ============================================================================

class StudyTask(db.Model):
    __tablename__ = "study_task"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default="medium")  # low | medium | high
    status = db.Column(db.String(20), default="pending")  # pending | completed
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="study_tasks", lazy=True)
    topic = db.relationship("Topic", backref="study_tasks", lazy=True)


class StudySession(db.Model):
    __tablename__ = "study_session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    session_date = db.Column(db.Date, default=date.today, nullable=False)
    start_time = db.Column(db.String(20), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="study_sessions", lazy=True)
    topic = db.relationship("Topic", backref="study_sessions", lazy=True)


# ============================================================================
# 6. NOTES, RESOURCES, GOALS & ACTIVITY LOG
# ============================================================================

class StudentNote(db.Model):
    __tablename__ = "student_note"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    module = db.relationship("Module", backref="student_notes", lazy=True)
    topic = db.relationship("Topic", backref="student_notes", lazy=True)


class LearningResource(db.Model):
    __tablename__ = "learning_resource"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # NULL for verified public resources
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(db.String(30), default="link")  # pdf | video | article | book | github
    is_official = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    topic = db.relationship("Topic", backref="resources", lazy=True)


class AcademicGoal(db.Model):
    __tablename__ = "academic_goal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    target_percentage = db.Column(db.Integer, default=100)
    current_percentage = db.Column(db.Integer, default=0)
    target_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default="active")  # active | completed | archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="goals", lazy=True)


class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # topic_completed, study_session, task_done, note_added
    description = db.Column(db.String(300), nullable=False)
    reference_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
