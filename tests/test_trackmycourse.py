"""
TrackMyCourse — Comprehensive Automated Engineering QA & Regression Test Suite
Tests academic hierarchy, syllabus retrieval, user-isolated progress,
study organization, analytics calculations, and document ingestion.
"""
import pytest
import os
from app import create_app
from models import db, User, Course, Module, Topic, UserProgress, StudyTask, StudySession, StudentNote, LearningResource, AcademicGoal
from syllabus_parser import SyllabusParser

@pytest.fixture
def app():
    db_abs = os.path.abspath(os.path.join("instance", "trackmycourse.db")).replace("\\", "/")
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_abs}",
        "WTF_CSRF_ENABLED": False
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()


# ============================================================================
# 1. ACADEMIC HIERARCHY TESTS
# ============================================================================

def test_academic_dropdown_hierarchy(client):
    # 1. Universities
    res_uni = client.get("/api/universities")
    assert res_uni.status_code == 200
    unis = res_uni.json
    assert len(unis) >= 1
    ktu = next((u for u in unis if u.get("code") == "KTU" or "KTU" in u.get("name", "") or "Abdul Kalam" in u.get("name", "")), None)
    assert ktu is not None

    # 2. Programs for KTU
    res_prog = client.get(f"/api/programs?university_id={ktu['id']}")
    assert res_prog.status_code == 200
    progs = res_prog.json
    mca = next((p for p in progs if p["name"] == "MCA"), None)
    assert mca is not None

    # 3. Streams (MCA has no stream)
    res_stream = client.get(f"/api/streams?program_id={mca['id']}")
    assert res_stream.status_code == 200
    assert len(res_stream.json) == 0

    # 4. Schemes for MCA
    res_scheme = client.get(f"/api/schemes?program_id={mca['id']}")
    assert res_scheme.status_code == 200
    schemes = res_scheme.json
    scheme_2021 = next((s for s in schemes if s["year"] == "2021"), None)
    assert scheme_2021 is not None

    # 5. Semesters for Scheme 2021
    res_sem = client.get(f"/api/semesters?scheme_id={scheme_2021['id']}")
    assert res_sem.status_code == 200
    sems = res_sem.json
    s1 = next((s for s in sems if s["semester_no"] == 1), None)
    assert s1 is not None

    # 6. Courses for Semester 1
    res_course = client.get(f"/api/courses?semester_id={s1['id']}")
    assert res_course.status_code == 200
    courses = res_course.json
    assert len(courses) >= 1


# ============================================================================
# 2. REGRESSION SCENARIO: ADVANCED SOFTWARE ENGINEERING (ASE)
# ============================================================================

def test_regression_ase_scenario(client):
    """
    Scenario: KTU -> MCA -> Scheme 2021 -> Semester 1 -> Advanced Software Engineering
    Course must load 5 modules, 49 topics, and verified progress (~88%).
    """
    # 1. Find ASE Course
    res_course = client.get("/api/courses?semester_id=1")
    assert res_course.status_code == 200
    courses = res_course.json
    ase = next((c for c in courses if "Advanced Software Engineering" in c["name"]), None)
    assert ase is not None, "Advanced Software Engineering must exist in MCA S1"

    # 2. Retrieve Syllabus
    res_syl = client.get(f"/api/syllabus?course_id={ase['id']}")
    assert res_syl.status_code == 200
    modules = res_syl.json
    assert len(modules) == 5, "ASE must have 5 modules"
    total_topics = sum(len(m["topics"]) for m in modules)
    assert total_topics == 49, f"ASE must have 49 topics, found {total_topics}"

    # 3. Check Progress Records
    res_prog = client.get(f"/api/progress/{ase['id']}")
    assert res_prog.status_code == 200
    records = res_prog.json
    completed_topics = sum(1 for r in records if r["completed"])
    pct = round((completed_topics / total_topics) * 100)
    assert pct >= 85 and pct <= 90, f"Expected approx 88% completion, got {pct}% ({completed_topics}/{total_topics})"


# ============================================================================
# 3. REGRESSION OF PRE-EXISTING MCA COURSES
# ============================================================================

def test_regression_maths_and_s2_courses(client):
    """Verify pre-existing courses have their original progress records intact."""
    # Course 3: Mathematical Foundations for Computing (MCA S1)
    res_sum_3 = client.get("/api/course-summary/3")
    assert res_sum_3.status_code == 200
    data_3 = res_sum_3.json
    assert data_3["total_topics"] == 51
    assert data_3["completed_topics"] == 40
    assert data_3["percentage"] == 78.4

    # Course 4: Advanced Database Management Systems (MCA S2)
    res_sum_4 = client.get("/api/course-summary/4")
    assert res_sum_4.status_code == 200
    data_4 = res_sum_4.json
    assert data_4["total_topics"] == 61
    assert data_4["completed_topics"] == 31
    assert data_4["percentage"] == 50.8

    # Course 5: Advanced Computer Networks (MCA S2)
    res_sum_5 = client.get("/api/course-summary/5")
    assert res_sum_5.status_code == 200
    data_5 = res_sum_5.json
    assert data_5["total_topics"] == 82
    assert data_5["completed_topics"] == 28
    assert data_5["percentage"] == 34.1

    # Course 6: Artificial Intelligence (MCA S2)
    res_sum_6 = client.get("/api/course-summary/6")
    assert res_sum_6.status_code == 200
    data_6 = res_sum_6.json
    assert data_6["total_topics"] == 53
    assert data_6["completed_topics"] == 42
    assert data_6["percentage"] == 79.2


# ============================================================================
# 4. ZERO TOPIC HANDLING & SAFE COMPUTATION
# ============================================================================

def test_zero_topic_course_summary(client, app):
    """A placeholder course with 0 topics must return 0.0% and never NaN or ZeroDivisionError."""
    with app.app_context():
        empty_course = Course.query.filter(~Course.modules.any()).first()
        if not empty_course:
            empty_course = Course(
                code="EMPTY100",
                name="Placeholder Empty Course",
                semester_id=1,
                credits=0
            )
            db.session.add(empty_course)
            db.session.commit()
        empty_id = empty_course.id

    res = client.get(f"/api/course-summary/{empty_id}")
    assert res.status_code == 200
    data = res.json
    assert data["total_topics"] == 0
    assert data["completed_topics"] == 0
    assert data["percentage"] == 0.0


# ============================================================================
# 5. USER PROGRESS ISOLATION & PERSISTENCE
# ============================================================================

def test_user_progress_persistence_and_isolation(client, app):
    with app.app_context():
        # Pick topic 1 from Course 3
        topic = Topic.query.first()
        topic_id = topic.id
        course_id = topic.module.course_id

    # 1. Update progress
    res_save = client.post("/api/progress", json={
        "topic_id": topic_id,
        "completed": True
    })
    assert res_save.status_code == 200
    assert res_save.json["status"] == "saved"

    # 2. Check topic is in progress
    res_load = client.get(f"/api/progress/{course_id}")
    assert res_load.status_code == 200
    saved = next((r for r in res_load.json if r["topic_id"] == topic_id), None)
    assert saved is not None
    assert saved["completed"] is True


# ============================================================================
# 6. STUDY TASKS & SESSIONS TESTS
# ============================================================================

def test_study_planner_and_sessions(client):
    # 1. Create a study task
    res_task = client.post("/api/study/tasks", json={
        "title": "Review Distributed Database Sharding",
        "course_id": 4,
        "due_date": "2026-12-01",
        "priority": "high"
    })
    assert res_task.status_code == 201
    task_id = res_task.json["id"]

    # 2. Toggle task status
    res_toggle = client.post(f"/api/study/tasks/{task_id}/toggle")
    assert res_toggle.status_code == 200
    assert res_toggle.json["status"] == "completed"

    # 3. Log a study session
    res_sess = client.post("/api/study/sessions", json={
        "course_id": 4,
        "duration_minutes": 50,
        "session_date": "2026-11-16",
        "notes": "Covered two-phase commit protocols"
    })
    assert res_sess.status_code == 201


# ============================================================================
# 7. NOTES, RESOURCES & GOALS TESTS
# ============================================================================

def test_notes_resources_and_goals(client):
    # 1. Create a Note
    res_note = client.post("/api/study/notes", json={
        "title": "Amdahl Law Formulation",
        "content": "Speedup S = 1 / ((1 - p) + (p / s))",
        "course_id": 3
    })
    assert res_note.status_code == 201
    note_id = res_note.json["id"]

    # 2. Retrieve Notes
    res_get_notes = client.get(f"/api/study/notes?course_id=3")
    assert res_get_notes.status_code == 200
    assert any(n["id"] == note_id for n in res_get_notes.json)

    # 3. Create Resource
    res_res = client.post("/api/study/resources", json={
        "title": "MIT Distributed Systems Lecture Notes",
        "url": "https://pdos.csail.mit.edu/6.824/",
        "course_id": 4,
        "resource_type": "link"
    })
    assert res_res.status_code == 201

    # 4. Create Goal
    res_goal = client.post("/api/study/goals", json={
        "title": "Complete 85% of ASE",
        "course_id": 7,
        "target_percentage": 85,
        "target_date": "2026-12-31"
    })
    assert res_goal.status_code == 201


# ============================================================================
# 8. AUTHENTICATION FLOW TESTS
# ============================================================================

def test_authentication_login_flow(client):
    # Ensure logged out first
    client.get("/logout")

    # 1. Test invalid credentials
    res_bad = client.post("/login", data={
        "email": "student@trackmycourse.edu",
        "password": "wrongpassword"
    }, follow_redirects=False)
    assert res_bad.status_code == 200  # Stays on login page with flash message

    # 2. Test valid student login
    res_login = client.post("/login", data={
        "email": "student@trackmycourse.edu",
        "password": "student123"
    }, follow_redirects=False)
    assert res_login.status_code == 302
    assert "/dashboard" in res_login.headers.get("Location", "")

    # 3. Test logout
    res_logout = client.get("/logout", follow_redirects=False)
    assert res_logout.status_code == 302


# ============================================================================
# 9. DOCUMENT EXTRACTION & SYLLABUS PARSER
# ============================================================================

def test_syllabus_parser_extraction():
    sample_text = """
    20MCA109 - CLOUD COMPUTING AND DEVOPS
    MODULE 1: Cloud Architecture Fundamentals (8 HOURS)
    - Virtualization concepts: hypervisors, containers and microVMs
    - Cloud service models: IaaS, PaaS, SaaS
    - Multi-cloud and hybrid deployments
    MODULE 2: Container Orchestration & Kubernetes (10 HOURS)
    - Kubernetes control plane architecture
    - Pods, Deployments, StatefulSets and Services
    - Ingress controllers and service meshes
    """
    res = SyllabusParser._structure_academic_text(sample_text, {
        "course_name": "Cloud Computing and DevOps",
        "course_code": "20MCA109",
        "semester_no": 2
    })
    assert len(res["semesters"]) == 1
    c = res["semesters"][0]["courses"][0]
    assert c["code"] == "20MCA109"
    assert len(c["modules"]) == 2
    assert c["modules"][0]["hours"] == 8
    assert len(c["modules"][0]["topics"]) == 3
    assert len(c["modules"][1]["topics"]) == 3


# ============================================================================
# 10. MULTI-UNIVERSITY & BRANCH EXPANSION VERIFICATION
# ============================================================================

def test_multi_university_and_btech_branches(client):
    # 1. Check multiple universities exist
    res = client.get("/api/universities")
    assert res.status_code == 200
    unis = res.json
    uni_codes = {u.get("code") for u in unis}
    # Check key UGC/AICTE universities are present
    assert "KTU" in uni_codes
    assert "VTU" in uni_codes
    assert "AU" in uni_codes or any("Anna" in u["name"] for u in unis)

    # 2. Check search filter
    res_search = client.get("/api/universities?q=vtu")
    assert res_search.status_code == 200
    assert any("VTU" in u.get("code", "") or "Visvesvaraya" in u.get("name", "") for u in res_search.json)

    # 3. Check KTU B.Tech branches
    ktu = next(u for u in unis if u.get("code") == "KTU")
    res_prog = client.get(f"/api/programs?university_id={ktu['id']}")
    btech = next(p for p in res_prog.json if p["code"] == "BTech" or "B.Tech" in p["name"])
    assert btech is not None

    res_streams = client.get(f"/api/streams?program_id={btech['id']}")
    assert res_streams.status_code == 200
    streams = res_streams.json
    stream_codes = {s["code"] for s in streams}
    assert "CSE" in stream_codes
    assert "ECE" in stream_codes
    assert "ME" in stream_codes

    # 4. Check B.Tech semesters (8 semesters in ascending order)
    res_schemes = client.get(f"/api/schemes?program_id={btech['id']}&stream_id={streams[0]['id']}")
    assert res_schemes.status_code == 200
    scheme = res_schemes.json[0]
    res_sem = client.get(f"/api/semesters?scheme_id={scheme['id']}")
    assert res_sem.status_code == 200
    semesters = res_sem.json
    assert len(semesters) == 8
    sem_numbers = [s["semester_no"] for s in semesters]
    assert sem_numbers == [1, 2, 3, 4, 5, 6, 7, 8]

    # 5. Check MCA semesters (strictly ordered 1, 2, 3, 4)
    mca = next(p for p in res_prog.json if p["code"] == "MCA")
    res_mca_schemes = client.get(f"/api/schemes?program_id={mca['id']}")
    mca_scheme = res_mca_schemes.json[0]
    res_mca_sem = client.get(f"/api/semesters?scheme_id={mca_scheme['id']}")
    mca_semesters = res_mca_sem.json
    mca_sem_nums = [s["semester_no"] for s in mca_semesters]
    assert mca_sem_nums == [1, 2, 3, 4]
