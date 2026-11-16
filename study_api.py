"""
TrackMyCourse — Study Organization API Blueprint
Powers Study Tasks (Planner), Study Sessions (Time Tracker), Notes, Resources & Goals.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from models import (
    db,
    StudyTask,
    StudySession,
    StudentNote,
    LearningResource,
    AcademicGoal,
    ActivityLog,
    Course,
    Topic
)
from datetime import datetime, date

study_api = Blueprint("study_api", __name__, url_prefix="/api/study")

def get_current_user_id():
    return current_user.id if current_user.is_authenticated else 1


# ============================================================================
# 1. STUDY TASKS (PLANNER)
# ============================================================================

@study_api.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = get_current_user_id()
    status = request.args.get("status")

    query = StudyTask.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)

    tasks = query.order_by(StudyTask.due_date.asc().nullslast(), StudyTask.created_at.desc()).all()
    today = date.today()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description or "",
            "course_id": t.course_id,
            "course_name": t.course.name if t.course else None,
            "topic_id": t.topic_id,
            "topic_name": t.topic.name if t.topic else None,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "priority": t.priority,
            "status": t.status,
            "is_overdue": t.due_date < today if (t.due_date and t.status == "pending") else False,
            "completed_at": t.completed_at.isoformat() if t.completed_at else None
        }
        for t in tasks
    ])


@study_api.route("/tasks", methods=["POST"])
def create_task():
    user_id = get_current_user_id()
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            pass

    course_id = data.get("course_id")
    if course_id:
        try:
            course_id = int(course_id)
        except ValueError:
            course_id = None

    task = StudyTask(
        user_id=user_id,
        title=title,
        description=data.get("description", "").strip(),
        course_id=course_id,
        topic_id=int(data["topic_id"]) if data.get("topic_id") else None,
        due_date=due_date,
        priority=data.get("priority", "medium")
    )
    db.session.add(task)

    log = ActivityLog(
        user_id=user_id,
        activity_type="task_created",
        description=f"Created study task: {title}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "created", "id": task.id}), 201


@study_api.route("/tasks/<int:task_id>/toggle", methods=["POST", "PUT"])
def toggle_task(task_id):
    user_id = get_current_user_id()
    task = StudyTask.query.filter_by(id=task_id, user_id=user_id).first_or_404()

    if task.status == "pending":
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        desc = f"Completed task: {task.title}"
    else:
        task.status = "pending"
        task.completed_at = None
        desc = f"Reopened task: {task.title}"

    log = ActivityLog(
        user_id=user_id,
        activity_type="task_status_changed",
        description=desc,
        reference_id=task.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"status": task.status, "id": task.id})


@study_api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    user_id = get_current_user_id()
    task = StudyTask.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ============================================================================
# 2. STUDY SESSIONS (TIME TRACKING)
# ============================================================================

@study_api.route("/sessions", methods=["GET"])
def get_sessions():
    user_id = get_current_user_id()
    limit = int(request.args.get("limit", 50))

    sessions = (
        StudySession.query
        .filter_by(user_id=user_id)
        .order_by(StudySession.session_date.desc(), StudySession.created_at.desc())
        .limit(limit)
        .all()
    )

    return jsonify([
        {
            "id": s.id,
            "session_date": s.session_date.isoformat(),
            "duration_minutes": s.duration_minutes,
            "course_id": s.course_id,
            "course_name": s.course.name if s.course else "General Study",
            "topic_id": s.topic_id,
            "topic_name": s.topic.name if s.topic else None,
            "notes": s.notes or "",
            "start_time": s.start_time or ""
        }
        for s in sessions
    ])


@study_api.route("/sessions", methods=["POST"])
def log_session():
    user_id = get_current_user_id()
    data = request.get_json() or {}

    duration = int(data.get("duration_minutes", 30))
    if duration <= 0:
        return jsonify({"error": "Duration must be greater than 0"}), 400

    session_date = date.today()
    if data.get("session_date"):
        try:
            session_date = datetime.strptime(data["session_date"], "%Y-%m-%d").date()
        except ValueError:
            pass

    course_id = int(data["course_id"]) if data.get("course_id") else None

    session = StudySession(
        user_id=user_id,
        course_id=course_id,
        topic_id=int(data["topic_id"]) if data.get("topic_id") else None,
        session_date=session_date,
        duration_minutes=duration,
        notes=data.get("notes", "").strip(),
        start_time=data.get("start_time", datetime.now().strftime("%H:%M"))
    )
    db.session.add(session)

    c_name = session.course.name if session.course else "General Study"
    log = ActivityLog(
        user_id=user_id,
        activity_type="study_session",
        description=f"Logged {duration} mins of study for {c_name}",
        reference_id=session.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "logged", "id": session.id}), 201


# ============================================================================
# 3. STUDENT NOTES
# ============================================================================

@study_api.route("/notes", methods=["GET"])
def get_notes():
    user_id = get_current_user_id()
    course_id = request.args.get("course_id")

    query = StudentNote.query.filter_by(user_id=user_id)
    if course_id and course_id.isdigit():
        query = query.filter_by(course_id=int(course_id))

    notes = query.order_by(StudentNote.updated_at.desc()).all()
    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "course_id": n.course_id,
            "course_name": n.course.name if n.course else "General Note",
            "module_id": n.module_id,
            "topic_id": n.topic_id,
            "topic_name": n.topic.name if n.topic else None,
            "updated_at": n.updated_at.strftime("%b %d, %Y %I:%M %p")
        }
        for n in notes
    ])


@study_api.route("/notes", methods=["POST"])
def create_note():
    user_id = get_current_user_id()
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    course_id = int(data["course_id"]) if data.get("course_id") else None

    note = StudentNote(
        user_id=user_id,
        course_id=course_id,
        module_id=int(data["module_id"]) if data.get("module_id") else None,
        topic_id=int(data["topic_id"]) if data.get("topic_id") else None,
        title=title,
        content=content
    )
    db.session.add(note)

    log = ActivityLog(
        user_id=user_id,
        activity_type="note_created",
        description=f"Created note: '{title}'"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "created", "id": note.id}), 201


@study_api.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    user_id = get_current_user_id()
    note = StudentNote.query.filter_by(id=note_id, user_id=user_id).first_or_404()

    data = request.get_json() or {}
    note.title = data.get("title", note.title).strip()
    note.content = data.get("content", note.content).strip()
    note.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({"status": "updated", "id": note.id})


@study_api.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    user_id = get_current_user_id()
    note = StudentNote.query.filter_by(id=note_id, user_id=user_id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ============================================================================
# 4. LEARNING RESOURCES
# ============================================================================

@study_api.route("/resources", methods=["GET"])
def get_resources():
    user_id = get_current_user_id()
    course_id = request.args.get("course_id")

    # Fetch resources belonging to user OR official resources (user_id IS NULL or is_official is True)
    query = LearningResource.query.filter(
        db.or_(LearningResource.user_id == user_id, LearningResource.is_official == True)
    )

    if course_id and course_id.isdigit():
        query = query.filter_by(course_id=int(course_id))

    resources = query.order_by(LearningResource.is_official.desc(), LearningResource.created_at.desc()).all()

    return jsonify([
        {
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "resource_type": r.resource_type,
            "is_official": r.is_official,
            "course_id": r.course_id,
            "course_name": r.course.name if r.course else None,
            "topic_id": r.topic_id
        }
        for r in resources
    ])


@study_api.route("/resources", methods=["POST"])
def add_resource():
    user_id = get_current_user_id()
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    url = data.get("url", "").strip()

    if not title or not url:
        return jsonify({"error": "Title and URL are required"}), 400

    course_id = int(data["course_id"]) if data.get("course_id") else None

    resource = LearningResource(
        user_id=user_id,
        course_id=course_id,
        topic_id=int(data["topic_id"]) if data.get("topic_id") else None,
        title=title,
        url=url,
        resource_type=data.get("resource_type", "link"),
        is_official=False
    )
    db.session.add(resource)
    db.session.commit()

    return jsonify({"status": "added", "id": resource.id}), 201


@study_api.route("/resources/<int:res_id>", methods=["DELETE"])
def delete_resource(res_id):
    user_id = get_current_user_id()
    resource = LearningResource.query.filter_by(id=res_id, user_id=user_id).first_or_404()
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ============================================================================
# 5. ACADEMIC GOALS
# ============================================================================

@study_api.route("/goals", methods=["GET"])
def get_goals():
    user_id = get_current_user_id()
    goals = AcademicGoal.query.filter_by(user_id=user_id).order_by(AcademicGoal.target_date.asc().nullslast()).all()

    return jsonify([
        {
            "id": g.id,
            "title": g.title,
            "description": g.description or "",
            "course_id": g.course_id,
            "course_name": g.course.name if g.course else "Overall Academics",
            "target_percentage": g.target_percentage,
            "current_percentage": g.current_percentage,
            "target_date": g.target_date.isoformat() if g.target_date else None,
            "status": g.status
        }
        for g in goals
    ])


@study_api.route("/goals", methods=["POST"])
def create_goal():
    user_id = get_current_user_id()
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Goal title is required"}), 400

    target_date = None
    if data.get("target_date"):
        try:
            target_date = datetime.strptime(data["target_date"], "%Y-%m-%d").date()
        except ValueError:
            pass

    goal = AcademicGoal(
        user_id=user_id,
        course_id=int(data["course_id"]) if data.get("course_id") else None,
        title=title,
        description=data.get("description", "").strip(),
        target_percentage=int(data.get("target_percentage", 100)),
        current_percentage=int(data.get("current_percentage", 0)),
        target_date=target_date,
        status="active"
    )
    db.session.add(goal)
    db.session.commit()

    return jsonify({"status": "created", "id": goal.id}), 201


@study_api.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    user_id = get_current_user_id()
    goal = AcademicGoal.query.filter_by(id=goal_id, user_id=user_id).first_or_404()
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"status": "deleted"})
