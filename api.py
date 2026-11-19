"""
TrackMyCourse — Core Academic & Progress API Blueprint
Preserves existing API contracts while securing multi-user isolation,
eliminating data leaks, and adding detailed course summaries and live university search.
"""
from flask import Blueprint, request, jsonify, send_from_directory, abort
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
from syllabus_parser import SyllabusParser
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
    ActivityLog,
    SyllabusSource
)
from datetime import datetime

api = Blueprint("api", __name__, url_prefix="/api")


def get_current_user_id():
    """Returns authenticated user ID or defaults to scholar ID 1 for backward compatibility."""
    if current_user.is_authenticated:
        return current_user.id
    return 1


# ============================================================================
# ACADEMIC SELECTION ENDPOINTS (PRESERVED & ENHANCED CONTRACTS)
# ============================================================================

@api.route("/universities")
def get_universities():
    search_query = request.args.get("q", "").strip()
    query = University.query
    if search_query:
        query = query.filter(
            db.or_(
                University.name.ilike(f"%{search_query}%"),
                University.code.ilike(f"%{search_query}%"),
                University.state.ilike(f"%{search_query}%")
            )
        )
    universities = query.order_by(University.name.asc()).all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "code": u.code or "",
            "state": u.state or "",
            "country": u.country or "India",
            "website": u.website or ""
        }
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

    programs = Program.query.filter_by(university_id=u_id).order_by(Program.name.asc()).all()
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

    streams = Stream.query.filter_by(program_id=p_id).order_by(Stream.name.asc()).all()
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
        query = query.filter(
            db.or_(
                Scheme.stream_id == int(stream_id),
                Scheme.stream_id.is_(None)
            )
        )
    else:
        # If program has streams, but no stream_id passed yet, return empty
        has_streams = Stream.query.filter_by(program_id=p_id).count() > 0
        if has_streams:
            return jsonify([])
        query = query.filter(Scheme.stream_id.is_(None))

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

    # Ensure strictly sorted in ascending order (Semester 1, 2, 3, 4, ...)
    semesters = Semester.query.filter_by(scheme_id=s_id).order_by(Semester.semester_no.asc()).all()
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

    courses = Course.query.filter_by(semester_id=s_id).order_by(Course.code.asc().nullslast(), Course.name.asc()).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "code": c.code or "",
            "credits": c.credits or 4,
            "course_type": c.course_type or "Theory",
            "drive_url": c.drive_url or ("https://drive.google.com/drive/folders/1d-bjA0vt65UWnMpIMC4u26_gyewsxMOz" if c.code == "20MCA201" else "")
        }
        for c in courses
    ])


def find_course_local_folder(course_code):
    """Locate local course folder in D:\\MCA2025-27 by course code if available."""
    if not course_code:
        return None
    base_dir = r"D:\MCA2025-27"
    if not os.path.exists(base_dir):
        return None
    import glob
    matches = glob.glob(os.path.join(base_dir, "Semester-*", f"*{course_code}*"))
    if matches and os.path.isdir(matches[0]):
        return matches[0]
    return None


@api.route("/course-files/<int:course_id>")
def get_course_files(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    subpath = request.args.get("subpath", "").strip().lstrip("/\\")
    drive_url = course.drive_url or ""
    if course.code == "20MCA201" and not drive_url:
        drive_url = "https://drive.google.com/drive/folders/1d-bjA0vt65UWnMpIMC4u26_gyewsxMOz"

    root_folder = find_course_local_folder(course.code)
    
    response_data = {
        "course_id": course.id,
        "course_code": course.code or "",
        "course_name": course.name,
        "drive_url": drive_url,
        "has_local_folder": bool(root_folder),
        "folder_name": os.path.basename(root_folder) if root_folder else "",
        "current_subpath": subpath,
        "items": []
    }

    if not root_folder:
        return jsonify(response_data)

    target_dir = os.path.normpath(os.path.join(root_folder, subpath))
    # Security check: prevent directory traversal outside root_folder
    if not target_dir.startswith(os.path.normpath(root_folder)) or not os.path.isdir(target_dir):
        return jsonify(response_data)

    items = []
    try:
        entries = sorted(os.listdir(target_dir))
        for name in entries:
            # Skip hidden / lock / build files
            if name.startswith((".", "~$", "__")) or name.endswith((".ini", ".tmp")):
                continue
            full_path = os.path.join(target_dir, name)
            rel_path = "/".join(filter(None, [subpath, name])).replace("\\", "/")
            
            if os.path.isdir(full_path):
                try:
                    sub_count = len([x for x in os.listdir(full_path) if not x.startswith(".")])
                except Exception:
                    sub_count = 0
                items.append({
                    "name": name,
                    "type": "folder",
                    "path": rel_path,
                    "item_count": sub_count
                })
            else:
                ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
                size_bytes = os.path.getsize(full_path)
                size_str = f"{size_bytes / 1024:.1f} KB" if size_bytes < 1024 * 1024 else f"{size_bytes / (1024*1024):.1f} MB"
                items.append({
                    "name": name,
                    "type": "file",
                    "path": rel_path,
                    "size": size_str,
                    "ext": ext
                })
    except Exception:
        pass

    response_data["items"] = items
    return jsonify(response_data)


@api.route("/open-file/<int:course_id>/<path:filepath>")
def open_course_file(course_id, filepath):
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    root_folder = find_course_local_folder(course.code)
    if not root_folder:
        abort(404)
    safe_filepath = filepath.replace("\\", "/")
    full_path = os.path.normpath(os.path.join(root_folder, safe_filepath))
    if not full_path.startswith(os.path.normpath(root_folder)) or not os.path.isfile(full_path):
        abort(404)
    return send_from_directory(root_folder, safe_filepath, as_attachment=False)


@api.route("/course-drive-url/<int:course_id>", methods=["POST"])
def update_course_drive_url(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    data = request.get_json() or {}
    drive_url = data.get("drive_url", "").strip()
    course.drive_url = drive_url
    db.session.commit()
    return jsonify({
        "success": True,
        "course_id": course.id,
        "drive_url": course.drive_url
    })


@api.route("/syllabus")
def get_syllabus():
    course_id = request.args.get("course_id")
    if not course_id:
        return jsonify([])
    try:
        c_id = int(course_id)
    except ValueError:
        return jsonify({"error": "Invalid course_id"}), 400

    modules = Module.query.filter_by(course_id=c_id).order_by(Module.module_no.asc().nullslast(), Module.id.asc()).all()

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

    topic = db.session.get(Topic, topic_id)
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
    course = db.session.get(Course, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

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
        "course_code": course.code or "",
        "credits": course.credits or 4,
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "remaining_topics": max(0, total_topics - completed_topics),
        "percentage": percent
    })


# ============================================================================
# STUDENT SYLLABUS SUBMISSION & SEMESTER-WISE INGESTION
# ============================================================================

@api.route("/student/parse-syllabus", methods=["POST"])
def student_parse_syllabus():
    """Parses an uploaded file or pasted text and returns an organized semester-wise syllabus preview."""
    metadata = {
        "university_name": request.form.get("university_name", "APJ Abdul Kalam Technological University"),
        "program_name": request.form.get("program_name", "MCA"),
        "scheme_year": request.form.get("scheme_year", "2020"),
        "course_name": request.form.get("course_name", ""),
        "course_code": request.form.get("course_code", ""),
        "document_title": request.form.get("document_title", "Student Submitted Syllabus"),
        "source_url": request.form.get("source_url", "")
    }

    # 1. Handle uploaded file if present
    if "file" in request.files and request.files["file"].filename:
        file = request.files["file"]
        if not SyllabusParser.allowed_file(file.filename):
            return jsonify({"error": "Unsupported file format. Please upload PDF, DOCX, XLSX, or JSON."}), 400

        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        metadata["document_title"] = filename
        parsed = SyllabusParser.parse_file(file_path, metadata=metadata)
        return jsonify(parsed)

    # 2. Handle pasted text
    pasted_text = request.form.get("syllabus_text") or (request.is_json and request.json.get("syllabus_text"))
    if pasted_text and pasted_text.strip():
        parsed = SyllabusParser.parse_text_content(pasted_text, metadata=metadata)
        return jsonify(parsed)

    return jsonify({"error": "Please provide a syllabus file or paste syllabus text."}), 400


@api.route("/student/save-syllabus", methods=["POST"])
def student_save_syllabus():
    """Takes verified semester-wise curriculum JSON and creates University -> Program -> Scheme -> Semesters -> Courses -> Modules -> Topics."""
    user_id = get_current_user_id()
    data = request.get_json() if request.is_json else None
    if not data:
        return jsonify({"error": "No syllabus data provided."}), 400

    uni_name = data.get("university", "APJ Abdul Kalam Technological University").strip()
    prog_name = data.get("program", "MCA").strip()
    scheme_year = str(data.get("scheme", "2020")).strip()
    semesters_data = data.get("semesters", [])

    if not semesters_data:
        return jsonify({"error": "No semester courses found in syllabus data."}), 400

    # 1. Resolve or create University
    uni = University.query.filter(
        db.or_(
            University.name.ilike(f"%{uni_name}%"),
            University.code.ilike(f"%{uni_name}%")
        )
    ).first()
    if not uni:
        uni_code = "".join([w[0] for w in uni_name.split()[:4]]).upper()
        uni = University(name=uni_name, code=uni_code, state="India", country="India")
        db.session.add(uni)
        db.session.flush()

    # 2. Resolve or create Program
    prog = Program.query.filter_by(name=prog_name, university_id=uni.id).first()
    if not prog:
        prog = Program(name=prog_name, code=prog_name[:10].upper(), degree_type="Degree", university_id=uni.id)
        db.session.add(prog)
        db.session.flush()

    # 3. Resolve or create Scheme
    scheme = Scheme.query.filter_by(year=scheme_year, program_id=prog.id).first()
    if not scheme:
        scheme = Scheme(year=scheme_year, program_id=prog.id, stream_id=None)
        db.session.add(scheme)
        db.session.flush()

    total_courses_created = 0
    total_topics_created = 0

    # 4. Iterate Semesters & Courses
    for sem_obj in semesters_data:
        sem_no = int(sem_obj.get("semester_no", 1))
        sem = Semester.query.filter_by(scheme_id=scheme.id, semester_no=sem_no).first()
        if not sem:
            sem = Semester(semester_no=sem_no, scheme_id=scheme.id)
            db.session.add(sem)
            db.session.flush()

        for c_obj in sem_obj.get("courses", []):
            c_name = c_obj.get("name", "").strip()
            c_code = c_obj.get("code", "").strip()
            c_credits = int(c_obj.get("credits", 4))
            c_type = c_obj.get("course_type", "Theory")

            if not c_name:
                continue

            course = Course.query.filter_by(name=c_name, semester_id=sem.id).first()
            if not course and c_code:
                course = Course.query.filter_by(code=c_code, semester_id=sem.id).first()

            if not course:
                course = Course(
                    name=c_name,
                    code=c_code,
                    credits=c_credits,
                    course_type=c_type,
                    semester_id=sem.id
                )
                db.session.add(course)
                db.session.flush()
                total_courses_created += 1

            # Modules & Topics
            for m_idx, m_obj in enumerate(c_obj.get("modules", []), 1):
                m_name = m_obj.get("name", f"Module {m_idx}").strip()
                m_hours = int(m_obj.get("hours", 8))
                m_no = int(m_obj.get("module_no", m_idx))

                module = Module.query.filter_by(name=m_name, course_id=course.id).first()
                if not module:
                    module = Module(name=m_name, module_no=m_no, hours=m_hours, course_id=course.id)
                    db.session.add(module)
                    db.session.flush()

                for t_name in m_obj.get("topics", []):
                    t_clean = t_name.strip()
                    if t_clean and not Topic.query.filter_by(name=t_clean, module_id=module.id).first():
                        db.session.add(Topic(name=t_clean, module_id=module.id))
                        total_topics_created += 1

            # Register provenance record
            src = SyllabusSource(
                university_id=uni.id,
                program_id=prog.id,
                scheme_id=scheme.id,
                course_id=course.id,
                document_title=data.get("provenance", {}).get("source_doc_title", "Student Contributed Syllabus"),
                source_url=data.get("provenance", {}).get("source_url", ""),
                publication_date=datetime.utcnow().strftime("%Y-%m-%d"),
                verification_status="student_submitted",
                verified_by=f"Student User #{user_id}",
                notes="Contributed by student user via Student Syllabus Ingest."
            )
            db.session.add(src)

    # Activity log
    act = ActivityLog(
        user_id=user_id,
        activity_type="syllabus_submitted",
        description=f"Submitted semester-wise syllabus for {uni.name} - {prog.name} ({scheme.year}): {total_courses_created} courses, {total_topics_created} topics."
    )
    db.session.add(act)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Syllabus successfully ingested! Added {total_courses_created} courses and {total_topics_created} topics.",
        "university_id": uni.id,
        "program_id": prog.id,
        "scheme_id": scheme.id,
        "courses_created": total_courses_created,
        "topics_created": total_topics_created
    })
