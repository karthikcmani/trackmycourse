from flask import Blueprint, request, jsonify
from models import (
    University, Program, Stream, Scheme,
    Semester, Course, Module, Topic
)

api = Blueprint("api", __name__)

# ---------- UNIVERSITIES ----------
@api.route("/api/universities")
def get_universities():
    data = University.query.all()
    return jsonify([
        {"id": u.id, "name": u.name} for u in data
    ])


# ---------- PROGRAMS ----------
@api.route("/api/programs")
def get_programs():
    university_id = request.args.get("university_id")
    data = Program.query.filter_by(university_id=university_id).all()
    return jsonify([
        {"id": p.id, "name": p.name} for p in data
    ])


# ---------- STREAMS ----------
@api.route("/api/streams")
def get_streams():
    program_id = request.args.get("program_id")
    data = Stream.query.filter_by(program_id=program_id).all()
    return jsonify([
        {"id": s.id, "name": s.name} for s in data
    ])


# ---------- SCHEMES ----------
@api.route("/api/schemes")
def get_schemes():
    program_id = request.args.get("program_id")
    stream_id = request.args.get("stream_id")

    query = Scheme.query.filter_by(program_id=program_id)

    if stream_id:
        query = query.filter_by(stream_id=stream_id)

    data = query.all()

    return jsonify([
        {"id": sc.id, "year": sc.year} for sc in data
    ])


# ---------- SEMESTERS ----------
@api.route("/api/semesters")
def get_semesters():
    scheme_id = request.args.get("scheme_id")
    data = Semester.query.filter_by(scheme_id=scheme_id).all()
    return jsonify([
        {"id": s.id, "semester_no": s.semester_no} for s in data
    ])


# ---------- COURSES ----------
@api.route("/api/courses")
def get_courses():
    semester_id = request.args.get("semester_id")
    data = Course.query.filter_by(semester_id=semester_id).all()
    return jsonify([
        {"id": c.id, "name": c.name} for c in data
    ])


# ---------- SYLLABUS ----------
@api.route("/api/syllabus")
def get_syllabus():
    course_id = request.args.get("course_id")

    modules = Module.query.filter_by(course_id=course_id).all()

    response = []

    for m in modules:
        topics = Topic.query.filter_by(module_id=m.id).all()
        response.append({
            "module": m.title,
            "hours": m.hours,
            "topics": [t.title for t in topics]
        })

    return jsonify(response)
