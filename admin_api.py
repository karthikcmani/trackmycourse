"""
TrackMyCourse — Administration & Academic Content Management Blueprint
Provides syllabus document uploads, intelligent parsing, preview & publishing,
academic CRUD management, official provenance tracking, and user administration.
"""
import os
import json
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
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
    SyllabusSource,
    SyllabusImport,
    User,
    ActivityLog
)
from syllabus_parser import SyllabusParser
from datetime import datetime

admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")

UPLOAD_FOLDER = os.path.join("instance", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def admin_required_check():
    """Returns True if current user is an authenticated administrator."""
    return current_user.is_authenticated and current_user.is_admin()


# ============================================================================
# 1. SYLLABUS DOCUMENT UPLOAD & EXTRACTION PIPELINE
# ============================================================================

@admin_api.route("/syllabus/upload", methods=["POST"])
def upload_syllabus_document():
    if "document" not in request.files:
        return jsonify({"error": "No file uploaded. Please select a valid document."}), 400

    file = request.files["document"]
    if not file or not file.filename:
        return jsonify({"error": "Empty filename."}), 400

    if not SyllabusParser.allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported file format. Please upload PDF, DOCX, XLSX, CSV, or JSON."
        }), 400

    orig_filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    stored_filename = f"{timestamp}_{orig_filename}"
    file_path = os.path.join(UPLOAD_FOLDER, stored_filename)
    file.save(file_path)

    file_ext = orig_filename.rsplit(".", 1)[-1].lower()

    # Form metadata passed alongside file
    metadata = {
        "university_name": request.form.get("university_name", "APJ Abdul Kalam Technological University"),
        "program_name": request.form.get("program_name", "MCA"),
        "scheme_year": request.form.get("scheme_year", "2020"),
        "semester_no": int(request.form.get("semester_no", 1)),
        "course_name": request.form.get("course_name", ""),
        "course_code": request.form.get("course_code", ""),
        "document_title": request.form.get("document_title", orig_filename),
        "source_url": request.form.get("source_url", "")
    }

    try:
        parsed_data = SyllabusParser.parse_file(file_path, file_ext, metadata)
    except Exception as e:
        return jsonify({"error": f"Failed to parse document: {str(e)}"}), 500

    user_id = current_user.id if current_user.is_authenticated else 1

    # Record in database for preview and review workflow
    syllabus_imp = SyllabusImport(
        filename=stored_filename,
        original_filename=orig_filename,
        file_type=file_ext,
        source_doc_title=metadata["document_title"],
        status="preview",
        extracted_data_json=json.dumps(parsed_data, indent=2),
        uploaded_by_user_id=user_id,
        is_public=False
    )
    db.session.add(syllabus_imp)
    db.session.commit()

    return jsonify({
        "status": "extracted",
        "import_id": syllabus_imp.id,
        "preview": parsed_data,
        "original_filename": orig_filename,
        "message": "Syllabus extracted successfully. Review and approve before publishing."
    })


@admin_api.route("/syllabus/preview/<int:import_id>", methods=["GET"])
def preview_syllabus_import(import_id):
    syllabus_imp = SyllabusImport.query.get_or_404(import_id)
    return jsonify({
        "id": syllabus_imp.id,
        "filename": syllabus_imp.original_filename,
        "status": syllabus_imp.status,
        "source_doc_title": syllabus_imp.source_doc_title,
        "extracted_data": json.loads(syllabus_imp.extracted_data_json) if syllabus_imp.extracted_data_json else {}
    })


@admin_api.route("/syllabus/publish/<int:import_id>", methods=["POST"])
def publish_syllabus_import(import_id):
    syllabus_imp = SyllabusImport.query.get_or_404(import_id)
    if not syllabus_imp.extracted_data_json:
        return jsonify({"error": "No extracted data found for this import."}), 400

    data = json.loads(syllabus_imp.extracted_data_json)

    # 1. Resolve or Create University
    uni_name = data.get("university", "APJ Abdul Kalam Technological University")
    uni = University.query.filter_by(name=uni_name).first()
    if not uni:
        uni = University(name=uni_name, code=uni_name[:10].upper(), country="India")
        db.session.add(uni)
        db.session.flush()

    # 2. Resolve or Create Program
    prog_name = data.get("program", "MCA")
    prog = Program.query.filter_by(name=prog_name, university_id=uni.id).first()
    if not prog:
        prog = Program(name=prog_name, code=prog_name[:10].upper(), university_id=uni.id)
        db.session.add(prog)
        db.session.flush()

    # 3. Resolve or Create Scheme
    scheme_year = str(data.get("scheme", "2020"))
    scheme = Scheme.query.filter_by(year=scheme_year, program_id=prog.id).first()
    if not scheme:
        scheme = Scheme(year=scheme_year, program_id=prog.id)
        db.session.add(scheme)
        db.session.flush()

    # 4. Iterate Semesters & Courses
    imported_courses_count = 0
    imported_topics_count = 0

    for sem_data in data.get("semesters", []):
        sem_no = int(sem_data.get("semester_no", 1))
        sem = Semester.query.filter_by(scheme_id=scheme.id, semester_no=sem_no).first()
        if not sem:
            sem = Semester(semester_no=sem_no, scheme_id=scheme.id)
            db.session.add(sem)
            db.session.flush()

        for c_data in sem_data.get("courses", []):
            c_name = c_data.get("name", "Curriculum Course")
            c_code = c_data.get("code", "")
            
            course = Course.query.filter_by(name=c_name, semester_id=sem.id).first()
            if not course:
                course = Course(
                    name=c_name,
                    code=c_code,
                    credits=int(c_data.get("credits", 4)),
                    course_type=c_data.get("course_type", "Theory"),
                    semester_id=sem.id
                )
                db.session.add(course)
                db.session.flush()
                imported_courses_count += 1
            elif c_code and not course.code:
                course.code = c_code

            # Modules
            for mod_idx, mod_data in enumerate(c_data.get("modules", []), 1):
                mod_name = mod_data.get("name", f"Module {mod_idx}")
                hours = int(mod_data.get("hours", 8))
                
                module = Module.query.filter_by(name=mod_name, course_id=course.id).first()
                if not module:
                    module = Module(
                        name=mod_name,
                        module_no=mod_idx,
                        hours=hours,
                        course_id=course.id
                    )
                    db.session.add(module)
                    db.session.flush()

                # Topics
                for top_idx, top_name in enumerate(mod_data.get("topics", []), 1):
                    topic = Topic.query.filter_by(name=top_name, module_id=module.id).first()
                    if not topic:
                        topic = Topic(
                            name=top_name,
                            topic_no=top_idx,
                            module_id=module.id
                        )
                        db.session.add(topic)
                        imported_topics_count += 1

            # Provenance Source Record
            prov = data.get("provenance", {})
            src = SyllabusSource(
                university_id=uni.id,
                program_id=prog.id,
                scheme_id=scheme.id,
                course_id=course.id,
                document_title=prov.get("source_doc_title", syllabus_imp.source_doc_title or c_name),
                source_url=prov.get("source_url", ""),
                verification_status="verified",
                version="1.0",
                verified_by="Administrator Verification Engine"
            )
            db.session.add(src)

    syllabus_imp.status = "published"
    syllabus_imp.reviewed_at = datetime.utcnow()
    syllabus_imp.is_public = True
    db.session.commit()

    return jsonify({
        "status": "published",
        "courses_added": imported_courses_count,
        "topics_added": imported_topics_count,
        "message": f"Successfully published {imported_courses_count} courses and {imported_topics_count} topics to official catalog."
    })


# ============================================================================
# 2. PROVENANCE & SOURCES LISTING
# ============================================================================

@admin_api.route("/sources", methods=["GET"])
def get_provenance_sources():
    sources = SyllabusSource.query.order_by(SyllabusSource.id.desc()).all()
    return jsonify([
        {
            "id": s.id,
            "document_title": s.document_title,
            "source_url": s.source_url or "",
            "publication_date": s.publication_date or "",
            "retrieval_date": s.retrieval_date.strftime("%Y-%m-%d") if s.retrieval_date else "",
            "verification_status": s.verification_status,
            "version": s.version,
            "verified_by": s.verified_by or "Official University Portal",
            "course_id": s.course_id,
            "notes": s.notes or ""
        }
        for s in sources
    ])


# ============================================================================
# 3. USER MANAGEMENT & CONTROL
# ============================================================================

@admin_api.route("/users", methods=["GET"])
def list_users():
    users = User.query.order_by(User.id).all()
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at.strftime("%Y-%m-%d") if u.created_at else ""
        }
        for u in users
    ])


@admin_api.route("/users/<int:user_id>/toggle-role", methods=["POST"])
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)
    user.role = "admin" if user.role == "student" else "student"
    db.session.commit()
    return jsonify({"status": "updated", "role": user.role, "id": user.id})


@admin_api.route("/users/<int:user_id>/toggle-status", methods=["POST"])
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({"status": "updated", "is_active": user.is_active, "id": user.id})
