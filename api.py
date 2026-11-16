"""
TrackMyCourse — Core Academic & Progress API Blueprint
Preserves existing API contracts while securing multi-user isolation,
eliminating data leaks, and adding detailed course summaries.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from models import (
    db,
    University,
    Program,
    Stream,
    Scheme,
    Semester,
    Course,
    Module,
    Topic,
    UserProgress,
    ActivityLog
)
from datetime import datetime

api = Blueprint("api", __name__, url_prefix="/api")


def get_current_user_id():
    """Returns authenticated user ID or defaults to scholar ID 1 for backward compatibility."""
    if current_user.is_authenticated:
        return current_user.id
    return 1


# ============================================================================
# ACADEMIC SELECTION ENDPOINTS (PRESERVED CONTRACTS)
# ============================================================================

@api.route("/universities")
def get_universities():
    universities = University.query.order_by(University.name).all()
    return jsonify([
        {"id": u.id, "name": u.name, "code": u.code, "state": u.state}
        for u in universities
    ])


@api.route("/programs")
def get_programs():
    university_id = request.args.get("university_id")
    if not university_id:
        return jsonify([])
    try:
        u_id = int(university_id)
    except ValueError:
        return jsonify({"error": "Invalid university_id"}), 400

    programs = Program.query.filter_by(university_id=u_id).order_by(Program.name).all()
    return jsonify([
        {"id": p.id, "name": p.name, "code": p.code, "degree_type": p.degree_type}
        for p in programs
    ])


@api.route("/streams")
def get_streams():
    program_id = request.args.get("program_id")
    if not program_id:
        return jsonify([])
    try:
        p_id = int(program_id)
    except ValueError:
        return jsonify({"error": "Invalid program_id"}), 400

    streams = Stream.query.filter_by(program_id=p_id).order_by(Stream.name).all()
    return jsonify([
        {"id": s.id, "name": s.name, "code": s.code}
        for s in streams
    ])


@api.route("/schemes")
def get_schemes():
    program_id = request.args.get("program_id")
    stream_id = request.args.get("stream_id")

    if not program_id:
        return jsonify([])
    try:
        p_id = int(program_id)
    except ValueError:
        return jsonify({"error": "Invalid program_id"}), 400

    query = Scheme.query.filter_by(program_id=p_id)

    if stream_id and stream_id.isdigit():
        query = query.filter_by(stream_id=int(stream_id))

    schemes = query.order_by(Scheme.year.desc()).all()
    return jsonify([
        {"id": s.id, "year": s.year}
        for s in schemes
    ])


@api.route("/semesters")
def get_semesters():
    scheme_id = request.args.get("scheme_id")
    if not scheme_id:
        return jsonify([])
    try:
        s_id = int(scheme_id)
    except ValueError:
        return jsonify({"error": "Invalid scheme_id"}), 400

    semesters = Semester.query.filter_by(scheme_id=s_id).order_by(Semester.semester_no).all()
    return jsonify([
        {"id": s.id, "semester_no": s.semester_no}
        for s in semesters
    ])


@api.route("/courses")
def get_courses():
    semester_id = request.args.get("semester_id")
    if not semester_id:
        return jsonify([])
    try:
        s_id = int(semester_id)
    except ValueError:
        return jsonify({"error": "Invalid semester_id"}), 400

    courses = Course.query.filter_by(semester_id=s_id).order_by(Course.name).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "code": c.code or "",
            "credits": c.credits or 4,
            "course_type": c.course_type or "Theory"
        }
        for c in courses
    ])


@api.route("/syllabus")
def get_syllabus():
    course_id = request.args.get("course_id")
    if not course_id:
        return jsonify([])
    try:
        c_id = int(course_id)
    except ValueError:
        return jsonify({"error": "Invalid course_id"}), 400

    modules = Module.query.filter_by(course_id=c_id).order_by(Module.module_no, Module.id).all()

    data = []
    for m in modules:
        topics_sorted = sorted(m.topics, key=lambda t: t.topic_no if t.topic_no is not None else t.id)
        data.append({
            "id": m.id,
            "module": m.name,
            "module_no": m.module_no,
            "hours": m.hours or 0,
            "topics": [
                {"id": t.id, "name": t.name, "topic_no": t.topic_no}
                for t in topics_sorted
            ]
        })

    return jsonify(data)


# ============================================================================
# USER PROGRESS PERSISTENCE (SECURE & USER-ISOLATED)
# ============================================================================

@api.route("/progress", methods=["POST"])
def save_progress():
    data = request.get_json() or {}
    if "topic_id" not in data or "completed" not in data:
        return jsonify({"error": "Missing topic_id or completed status"}), 400

    try:
        topic_id = int(data["topic_id"])
        completed = bool(data["completed"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid topic_id or completed format"}), 400

    user_id = get_current_user_id()

    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({"error": "Topic not found"}), 404

    progress = UserProgress.query.filter_by(
        user_id=user_id,
        topic_id=topic_id
    ).first()

    if progress:
        progress.completed = completed
        progress.updated_at = datetime.utcnow()
    else:
        progress = UserProgress(
            user_id=user_id,
            topic_id=topic_id,
            completed=completed,
            updated_at=datetime.utcnow()
        )
        db.session.add(progress)

    # Activity logging
    action = "Completed" if completed else "Uncompleted"
    course_name = topic.module.course.name if topic.module and topic.module.course else "Course"
    log = ActivityLog(
        user_id=user_id,
        activity_type="topic_progress",
        description=f"{action} topic '{topic.name[:60]}' in {course_name}",
        reference_id=topic.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "status": "saved",
        "topic_id": topic_id,
        "completed": completed,
        "user_id": user_id
    })


@api.route("/progress/<int:course_id>")
def load_progress(course_id):
    """
    CRITICAL FIX: Strictly filters by user_id to prevent multi-user progress leaks.
    """
    user_id = get_current_user_id()

    records = (
        UserProgress.query
        .join(Topic, UserProgress.topic_id == Topic.id)
        .join(Module, Topic.module_id == Module.id)
        .filter(Module.course_id == course_id, UserProgress.user_id == user_id)
        .all()
    )

    return jsonify([
        {"topic_id": r.topic_id, "completed": r.completed}
        for r in records
    ])


@api.route("/course-summary/<int:course_id>")
def course_summary(course_id):
    """Provides complete course analytics: total, completed, remaining, percentage."""
    user_id = get_current_user_id()
    course = Course.query.get_or_404(course_id)

    total_topics = (
        Topic.query
        .join(Module, Topic.module_id == Module.id)
        .filter(Module.course_id == course_id)
        .count()
    )

    completed_topics = (
        UserProgress.query
        .join(Topic, UserProgress.topic_id == Topic.id)
        .join(Module, Topic.module_id == Module.id)
        .filter(
            Module.course_id == course_id,
            UserProgress.user_id == user_id,
            UserProgress.completed == True
        )
        .count()
    )

    percent = round((completed_topics / total_topics) * 100, 1) if total_topics > 0 else 0.0

    return jsonify({
        "course_id": course.id,
        "course_name": course.name,
        "course_code": course.code,
        "credits": course.credits,
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "remaining_topics": max(0, total_topics - completed_topics),
        "percentage": percent
    })
