from flask import Blueprint, request, jsonify
from models import (
    University,
    Program,
    Stream,
    Scheme,
    Semester,
    Course,
    Module,
    Topic
)

# ---------- API BLUEPRINT ----------
api = Blueprint("api", __name__, url_prefix="/api")


# ---------- UNIVERSITIES ----------
@api.route("/universities")
def get_universities():
    universities = University.query.all()
    return jsonify([
        {"id": u.id, "name": u.name} for u in universities
    ])


# ---------- PROGRAMS ----------
@api.route("/programs")
def get_programs():
    university_id = request.args.get("university_id")
    programs = Program.query.filter_by(university_id=university_id).all()
    return jsonify([
        {"id": p.id, "name": p.name} for p in programs
    ])


# ---------- STREAMS ----------
@api.route("/streams")
def get_streams():
    program_id = request.args.get("program_id")
    streams = Stream.query.filter_by(program_id=program_id).all()
    return jsonify([
        {"id": s.id, "name": s.name} for s in streams
    ])


# ---------- SCHEMES ----------
@api.route("/schemes")
def get_schemes():
    program_id = request.args.get("program_id")
    stream_id = request.args.get("stream_id")

    query = Scheme.query.filter_by(program_id=program_id)

    if stream_id:
        query = query.filter_by(stream_id=stream_id)

    schemes = query.all()
    return jsonify([
        {"id": s.id, "year": s.year} for s in schemes
    ])


# ---------- SEMESTERS ----------
@api.route("/semesters")
def get_semesters():
    scheme_id = request.args.get("scheme_id")
    semesters = Semester.query.filter_by(scheme_id=scheme_id).all()
    return jsonify([
        {"id": s.id, "semester_no": s.semester_no} for s in semesters
    ])


# ---------- COURSES ----------
@api.route("/courses")
def get_courses():
    semester_id = request.args.get("semester_id")
    courses = Course.query.filter_by(semester_id=semester_id).all()
    return jsonify([
        {"id": c.id, "name": c.name} for c in courses
    ])


# ---------- SYLLABUS ----------
@api.route("/syllabus")
def get_syllabus():
    course_id = request.args.get("course_id")

    modules = Module.query.filter_by(course_id=course_id).all()

    data = []
    for m in modules:
        data.append({
            "module": m.name,
            "hours": m.hours,
            "topics": [t.name for t in m.topics]
        })

    return jsonify(data)
