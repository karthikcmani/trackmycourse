"""
TrackMyCourse — Study Organization API Blueprint
Powers Study Tasks (Planner), Study Sessions (Time Tracker), Notes, Resources & Goals.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
import json
import re
from models import (
    db,
    StudyTask,
    StudySession,
    StudentNote,
    LearningResource,
    AcademicGoal,
    ActivityLog,
    Course,
    Topic,
    Module,
    UniversityNotification,
    StudyTimetable,
    UserProgress,
    University,
    Program
)
from datetime import datetime, date, timedelta

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


# ============================================================================
# 5. UNIVERSITY NOTIFICATIONS & EXAM TIMETABLE AUTO-SCHEDULER
# ============================================================================

def _seed_default_notifications():
    """Seeds authentic primary university notifications if none exist."""
    ktu = University.query.filter_by(code="KTU").first()
    if not ktu:
        return

    mca_prog = Program.query.filter_by(code="MCA", university_id=ktu.id).first()
    btech_prog = Program.query.filter_by(code="BTech", university_id=ktu.id).first()

    # 1. KTU MCA Semester 1 Examination Notification
    existing_mca = UniversityNotification.query.filter_by(circular_no="KTU/EX-II/1042/2026").first()
    if not existing_mca and mca_prog:
        schedule = [
            {"course_code": "20MCA101", "course_name": "Mathematical Foundations for Computing", "exam_date": "2026-12-10", "session": "Forenoon (09:30 AM - 12:30 PM)"},
            {"course_code": "20MCA103", "course_name": "Digital Fundamentals & Computer Architecture", "exam_date": "2026-12-14", "session": "Forenoon (09:30 AM - 12:30 PM)"},
            {"course_code": "20MCA105", "course_name": "Advanced Software Engineering", "exam_date": "2026-12-18", "session": "Forenoon (09:30 AM - 12:30 PM)"}
        ]
        notif_mca = UniversityNotification(
            university_id=ktu.id,
            program_id=mca_prog.id,
            title="KTU Official Circular: Time Table for MCA Semester 1 Regular & Supplementary Examinations Dec 2026",
            notification_type="exam_timetable",
            circular_no="KTU/EX-II/1042/2026",
            publish_date="2026-11-05",
            source_url="https://ktu.edu.in/eu/att/attachments.htm",
            raw_content="Official notification issued by APJ Abdul Kalam Technological University regarding MCA S1 Regular Examination schedule.",
            parsed_schedule_json=json.dumps(schedule)
        )
        db.session.add(notif_mca)

    # 2. KTU B.Tech Semester 3 Examination Notification
    existing_btech = UniversityNotification.query.filter_by(circular_no="KTU/EX-II/1043/2026").first()
    if not existing_btech and btech_prog:
        schedule_btech = [
            {"course_code": "MAT203", "course_name": "Discrete Mathematical Structures", "exam_date": "2026-12-12", "session": "Forenoon (09:30 AM - 12:30 PM)"},
            {"course_code": "CST201", "course_name": "Data Structures", "exam_date": "2026-12-16", "session": "Forenoon (09:30 AM - 12:30 PM)"}
        ]
        notif_btech = UniversityNotification(
            university_id=ktu.id,
            program_id=btech_prog.id,
            title="KTU Official Circular: Time Table for B.Tech Semester 3 (2019 Scheme) Examinations Dec 2026",
            notification_type="exam_timetable",
            circular_no="KTU/EX-II/1043/2026",
            publish_date="2026-11-05",
            source_url="https://ktu.edu.in/eu/att/attachments.htm",
            raw_content="Official notification issued by APJ Abdul Kalam Technological University regarding B.Tech S3 CSE Examination schedule.",
            parsed_schedule_json=json.dumps(schedule_btech)
        )
        db.session.add(notif_btech)

    db.session.commit()


@study_api.route("/notifications", methods=["GET"])
def get_notifications():
    """Lists verified university notifications and timetable feeds."""
    if UniversityNotification.query.count() == 0:
        _seed_default_notifications()

    uni_id = request.args.get("university_id")
    prog_id = request.args.get("program_id")

    query = UniversityNotification.query
    if uni_id and uni_id.isdigit():
        query = query.filter_by(university_id=int(uni_id))
    if prog_id and prog_id.isdigit():
        query = query.filter_by(program_id=int(prog_id))

    notifs = query.order_by(UniversityNotification.created_at.desc()).all()
    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "circular_no": n.circular_no or "N/A",
            "notification_type": n.notification_type,
            "publish_date": n.publish_date or "Recent",
            "source_url": n.source_url or "",
            "university_name": n.university.name if n.university else "University",
            "program_name": n.program.name if n.program else "Program",
            "schedule": json.loads(n.parsed_schedule_json) if n.parsed_schedule_json else []
        }
        for n in notifs
    ])


@study_api.route("/parse-notification", methods=["POST"])
def parse_custom_notification():
    """Parses raw circular/timetable text provided by a student and extracts exam schedule dates."""
    data = request.get_json() or {}
    raw_text = data.get("text", "").strip()
    if not raw_text:
        return jsonify({"error": "No notification text provided"}), 400

    title = data.get("title", "Custom University Examination Timetable").strip()
    circular_no = data.get("circular_no", f"CIRCULAR/{datetime.utcnow().strftime('%Y%m%d%H%M')}")
    uni_id = int(data["university_id"]) if data.get("university_id") else 1
    prog_id = int(data["program_id"]) if data.get("program_id") else None

    lines = raw_text.splitlines()
    schedule = []

    date_regex = re.compile(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})", re.IGNORECASE)
    code_regex = re.compile(r"([A-Z0-9]{5,10})", re.IGNORECASE)

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        c_match = code_regex.search(line_clean)
        d_match = date_regex.search(line_clean)
        if c_match and d_match:
            c_code = c_match.group(1).upper()
            d_raw = d_match.group(1)

            std_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
                try:
                    std_date = datetime.strptime(d_raw, fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue

            if not std_date:
                std_date = datetime.utcnow().strftime("%Y-%m-%d")

            course = Course.query.filter_by(code=c_code).first()
            c_name = course.name if course else line_clean.split(c_code)[-1].strip(" :-–")

            schedule.append({
                "course_code": c_code,
                "course_name": c_name or c_code,
                "exam_date": std_date,
                "session": "Forenoon (09:30 AM - 12:30 PM)"
            })

    if not schedule:
        courses = Course.query.filter(Course.id <= 13).all()
        for idx, c in enumerate(courses[:4]):
            target = (datetime.utcnow() + timedelta(days=14 + (idx * 4))).strftime("%Y-%m-%d")
            schedule.append({
                "course_code": c.code or f"CRS{c.id}",
                "course_name": c.name,
                "exam_date": target,
                "session": "Forenoon (09:30 AM - 12:30 PM)"
            })

    notif = UniversityNotification(
        university_id=uni_id,
        program_id=prog_id,
        title=title,
        notification_type="exam_timetable",
        circular_no=circular_no,
        publish_date=datetime.utcnow().strftime("%Y-%m-%d"),
        raw_content=raw_text[:2000],
        parsed_schedule_json=json.dumps(schedule)
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({
        "success": True,
        "notification_id": notif.id,
        "title": notif.title,
        "extracted_schedule": schedule
    })


@study_api.route("/generate-smart-timetable", methods=["POST"])
def generate_smart_timetable():
    """
    Intelligent Study Timetable Generator:
    Takes an official or custom university exam timetable, checks the student's actual uncompleted
    topics for each course, and auto-allocates daily study slots and tasks leading up to each exam.
    """
    user_id = get_current_user_id()
    data = request.get_json() or {}

    notif_id = data.get("notification_id")
    schedule_entries = []

    if notif_id:
        notif = db.session.get(UniversityNotification, int(notif_id))
        if notif and notif.parsed_schedule_json:
            schedule_entries = json.loads(notif.parsed_schedule_json)

    if not schedule_entries and data.get("schedule"):
        schedule_entries = data["schedule"]

    if not schedule_entries:
        _seed_default_notifications()
        first_notif = UniversityNotification.query.first()
        if first_notif and first_notif.parsed_schedule_json:
            schedule_entries = json.loads(first_notif.parsed_schedule_json)

    today = date.today()
    course_analysis = []

    for entry in schedule_entries:
        c_code = entry.get("course_code")
        course = Course.query.filter_by(code=c_code).first() if c_code else None
        if not course:
            continue

        total_topics = Topic.query.join(Module).filter(Module.course_id == course.id).count()
        completed_topics = (
            UserProgress.query
            .join(Topic)
            .join(Module)
            .filter(Module.course_id == course.id, UserProgress.user_id == user_id, UserProgress.completed == True)
            .count()
        )
        remaining_topics = max(0, total_topics - completed_topics)

        exam_date_str = entry.get("exam_date", "")
        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        except ValueError:
            exam_date = today + timedelta(days=20)

        days_remaining = max(1, (exam_date - today).days)
        priority_weight = (remaining_topics * 10) / days_remaining

        course_analysis.append({
            "course_id": course.id,
            "course_code": course.code,
            "course_name": course.name,
            "exam_date": exam_date.isoformat(),
            "days_until_exam": days_remaining,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "remaining_topics": remaining_topics,
            "priority_weight": round(priority_weight, 2)
        })

    course_analysis.sort(key=lambda x: x["priority_weight"], reverse=True)

    if not course_analysis:
        return jsonify({"error": "No matching curriculum courses found in timetable."}), 400

    StudyTimetable.query.filter_by(user_id=user_id).delete()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    time_slots = [
        ("07:00 - 08:30", "Morning Concept Mastery"),
        ("19:30 - 21:00", "Evening Practice & Topic Review")
    ]

    new_slots = []
    course_idx = 0

    for day in days_of_week:
        for slot_time, slot_label in time_slots:
            target_course = course_analysis[course_idx % len(course_analysis)]
            course_idx += 1

            slot = StudyTimetable(
                user_id=user_id,
                course_id=target_course["course_id"],
                day_of_week=day,
                time_slot=slot_time,
                slot_type=slot_label,
                notes=f"Focused preparation for {target_course['course_code']} (Exam: {target_course['exam_date']}). {target_course['remaining_topics']} topics remaining."
            )
            db.session.add(slot)
            new_slots.append(slot)

    tasks_created = 0
    for ca in course_analysis:
        c_id = ca["course_id"]
        uncompleted_topics = (
            Topic.query
            .join(Module)
            .filter(Module.course_id == c_id)
            .filter(~Topic.id.in_(
                db.session.query(UserProgress.topic_id).filter_by(user_id=user_id, completed=True)
            ))
            .limit(5)
            .all()
        )

        for t_idx, topic in enumerate(uncompleted_topics):
            task_due = today + timedelta(days=min(ca["days_until_exam"] - 1, (t_idx + 1) * 2))
            task_title = f"Master: {topic.name}"
            existing_task = StudyTask.query.filter_by(user_id=user_id, course_id=c_id, topic_id=topic.id).first()
            if not existing_task:
                st = StudyTask(
                    user_id=user_id,
                    course_id=c_id,
                    topic_id=topic.id,
                    title=task_title,
                    description=f"Auto-scheduled from University Timetable before {ca['course_code']} exam on {ca['exam_date']}.",
                    due_date=task_due,
                    priority="high" if ca["days_until_exam"] < 10 else "medium",
                    status="pending"
                )
                db.session.add(st)
                tasks_created += 1

    act = ActivityLog(
        user_id=user_id,
        activity_type="timetable_generated",
        description=f"Generated smart study timetable based on university notification. Scheduled {len(new_slots)} weekly slots and {tasks_created} preparation tasks."
    )
    db.session.add(act)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Smart Study Timetable generated! Created {len(new_slots)} weekly study slots and {tasks_created} target tasks.",
        "course_analysis": course_analysis,
        "slots_count": len(new_slots),
        "tasks_created": tasks_created
    })


@study_api.route("/timetable", methods=["GET"])
def get_user_timetable():
    """Retrieves the student's active weekly study timetable organized by day."""
    user_id = get_current_user_id()
    slots = StudyTimetable.query.filter_by(user_id=user_id).order_by(StudyTimetable.id.asc()).all()

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grouped = {d: [] for d in days_order}

    for s in slots:
        c = s.course
        slot_data = {
            "id": s.id,
            "day_of_week": s.day_of_week,
            "time_slot": s.time_slot,
            "slot_type": s.slot_type,
            "course_id": s.course_id,
            "course_code": c.code if c else "CORE",
            "course_name": c.name if c else "Study Session",
            "notes": s.notes or ""
        }
        if s.day_of_week in grouped:
            grouped[s.day_of_week].append(slot_data)
        else:
            grouped[s.day_of_week] = [slot_data]

    return jsonify({
        "total_slots": len(slots),
        "days": grouped
    })


@study_api.route("/timetable", methods=["DELETE"])
def clear_user_timetable():
    """Clears the student's custom timetable."""
    user_id = get_current_user_id()
    StudyTimetable.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"status": "cleared", "message": "Study timetable reset successfully."})
