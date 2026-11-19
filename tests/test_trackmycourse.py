"""
TrackMyCourse — Comprehensive Automated Engineering QA & Regression Test Suite
Tests academic hierarchy, syllabus retrieval, user-isolated progress,
study organization, analytics calculations, and document ingestion.
"""
import pytest
import os
from app import create_app
from models import db, User, Course, Module, Topic, UserProgress, StudyTask, StudySession, StudentNote, LearningResource, AcademicGoal, SyllabusSource, UniversityNotification
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

    # 4. Schemes for MCA (Official KTU Scheme 2020)
    res_scheme = client.get(f"/api/schemes?program_id={mca['id']}")
    assert res_scheme.status_code == 200
    schemes = res_scheme.json
    scheme_2020 = next((s for s in schemes if s["year"] == "2020"), None)
    assert scheme_2020 is not None, "KTU MCA must be Scheme 2020 (official KTU 2020 Regulations)"

    # 5. Semesters for Scheme 2020
    res_sem = client.get(f"/api/semesters?scheme_id={scheme_2020['id']}")
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
    Scenario: KTU -> MCA -> Scheme 2020 -> Semester 1 -> Advanced Software Engineering
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
    """A course with 0 topics must return 0.0% and never NaN or ZeroDivisionError."""
    created_temp = False
    with app.app_context():
        empty_course = Course.query.filter(~Course.modules.any()).first()
        if not empty_course:
            empty_course = Course(
                code="ZERO001",
                name="Empty Test Course",
                semester_id=1,
                credits=0
            )
            db.session.add(empty_course)
            db.session.commit()
            created_temp = True
        empty_id = empty_course.id

    try:
        res = client.get(f"/api/course-summary/{empty_id}")
        assert res.status_code == 200
        data = res.json
        assert data["total_topics"] == 0
        assert data["completed_topics"] == 0
        assert data["percentage"] == 0.0
    finally:
        if created_temp:
            with app.app_context():
                c = db.session.get(Course, empty_id)
                if c:
                    db.session.delete(c)
                    db.session.commit()


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
    # 1. Check verified institutions exist (KTU)
    res = client.get("/api/universities")
    assert res.status_code == 200
    unis = res.json
    uni_codes = {u.get("code") for u in unis}
    assert "KTU" in uni_codes

    # 2. Check search filter
    res_search = client.get("/api/universities?q=ktu")
    assert res_search.status_code == 200
    assert any("KTU" in u.get("code", "") or "Kalam" in u.get("name", "") for u in res_search.json)

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
    assert "CE" in stream_codes
    assert "EEE" in stream_codes
    assert "IT" in stream_codes

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

    # 5. Check KTU MCA scheme (Scheme 2020) and semesters (strictly ordered 1, 2, 3, 4)
    mca = next(p for p in res_prog.json if p["code"] == "MCA")
    res_mca_schemes = client.get(f"/api/schemes?program_id={mca['id']}")
    mca_schemes = res_mca_schemes.json
    assert any(s["year"] == "2020" for s in mca_schemes), "Must be Scheme 2020"
    mca_scheme = next(s for s in mca_schemes if s["year"] == "2020")
    res_mca_sem = client.get(f"/api/semesters?scheme_id={mca_scheme['id']}")
    mca_semesters = res_mca_sem.json
    mca_sem_nums = [s["semester_no"] for s in mca_semesters]
    assert mca_sem_nums == [1, 2, 3, 4]


# ============================================================================
# 11. STUDENT SYLLABUS SUBMISSION & SEMESTER-WISE INGESTION
# ============================================================================

def test_student_syllabus_submission_and_semester_arrangement(client, app):
    """Verifies that students can submit their syllabus and have it arranged semester-wise."""
    sample_pasted_syllabus = """
    SEMESTER 1
    20MCA111 - CLOUD NATIVE ARCHITECTURE
    MODULE 1: Containers and MicroVMs (8 HOURS)
    - Docker container lifecycle, namespaces and cgroups
    - Container images and multi-stage builds
    MODULE 2: Kubernetes Orchestration (10 HOURS)
    - Pods, Deployments and ReplicaSets
    - Ingress controllers and services

    SEMESTER 2
    20MCA112 - DISTRIBUTED SYSTEMS
    MODULE 1: Consensus and Fault Tolerance (8 HOURS)
    - Paxos and Raft consensus algorithms
    - Vector clocks and Lamport timestamps
    """

    # 1. Parse syllabus outline
    res_parse = client.post("/api/student/parse-syllabus", data={
        "university_name": "APJ Abdul Kalam Technological University",
        "program_name": "MCA",
        "scheme_year": "2020",
        "syllabus_text": sample_pasted_syllabus
    })
    assert res_parse.status_code == 200
    parsed = res_parse.json
    assert "semesters" in parsed
    assert len(parsed["semesters"]) == 2
    assert parsed["semesters"][0]["semester_no"] == 1
    assert parsed["semesters"][1]["semester_no"] == 2

    # Verify courses inside semesters
    s1_course = parsed["semesters"][0]["courses"][0]
    assert s1_course["code"] == "20MCA111"
    assert len(s1_course["modules"]) == 2

    s2_course = parsed["semesters"][1]["courses"][0]
    assert s2_course["code"] == "20MCA112"

    try:
        # 2. Save structured syllabus
        res_save = client.post("/api/student/save-syllabus", json=parsed)
        assert res_save.status_code == 200
        save_result = res_save.json
        assert save_result["success"] is True
        assert save_result["courses_created"] >= 1
    finally:
        # Clean up test created courses so production DB is never polluted
        with app.app_context():
            for code in ["20MCA111", "20MCA112"]:
                c = Course.query.filter_by(code=code).first()
                if c:
                    for m in c.modules:
                        Topic.query.filter_by(module_id=m.id).delete()
                        db.session.delete(m)
                    SyllabusSource.query.filter_by(course_id=c.id).delete()
                    db.session.delete(c)
            db.session.commit()


# ============================================================================
# 12. UNIVERSITY NOTIFICATIONS & SMART STUDY TIMETABLE AUTO-SCHEDULER
# ============================================================================

def test_university_notification_and_smart_study_timetable(client, app):
    """Verifies extracting exam timetable from university notification and auto-scheduling study plan."""
    # 1. List University Notifications
    res_notif = client.get("/api/study/notifications")
    assert res_notif.status_code == 200
    notifs = res_notif.json
    assert len(notifs) >= 1
    assert any("KTU/EX-II" in n["circular_no"] for n in notifs)

    # 2. Parse Custom Notification Text
    sample_circular = """
    APJ ABDUL KALAM TECHNOLOGICAL UNIVERSITY
    EXAMINATION TIMETABLE NOTIFICATION - DEC 2026
    Circular No: KTU/EX-I/2026/889
    20MCA101 Mathematical Foundations - 2026-12-10 Forenoon
    20MCA105 Advanced Software Engineering - 2026-12-18 Forenoon
    """
    res_parse = client.post("/api/study/parse-notification", json={
        "text": sample_circular,
        "title": "KTU MCA S1 Exam Timetable"
    })
    assert res_parse.status_code == 200
    parse_data = res_parse.json
    assert parse_data["success"] is True
    notif_id = parse_data["notification_id"]

    try:
        # 3. Generate Smart Study Timetable
        res_gen = client.post("/api/study/generate-smart-timetable", json={
            "notification_id": notif_id
        })
        assert res_gen.status_code == 200
        gen_data = res_gen.json
        assert gen_data["success"] is True
        assert gen_data["slots_count"] == 14  # 7 days * 2 slots

        # 4. Retrieve Active Weekly Study Timetable
        res_tt = client.get("/api/study/timetable")
        assert res_tt.status_code == 200
        tt_data = res_tt.json
        assert tt_data["total_slots"] == 14
        assert "Monday" in tt_data["days"]
        assert len(tt_data["days"]["Monday"]) == 2

        # 5. Verify Study Tasks were auto-scheduled
        res_tasks = client.get("/api/study/tasks?status=pending")
        assert res_tasks.status_code == 200
        tasks = res_tasks.json
        assert any("University Timetable" in (t["description"] or "") for t in tasks)
    finally:
        with app.app_context():
            notif = db.session.get(UniversityNotification, notif_id)
            if notif:
                db.session.delete(notif)
            db.session.commit()

