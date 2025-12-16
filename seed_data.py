from app import app
from models import db, University, Program, Scheme, Semester, Course, Module, Topic

with app.app_context():

    # ---------- FETCH EXISTING BASE DATA ----------
    ktu = University.query.filter_by(name="KTU").first()
    mca = Program.query.filter_by(name="MCA").first()

    scheme_2021 = Scheme.query.filter_by(year="2021", program_id=mca.id).first()

    if not scheme_2021:
        print("❌ Scheme not found. Run seed_base_data.py first.")
        exit()

    # ---------- SEMESTER ----------
    sem1 = Semester.query.filter_by(semester_no=1, scheme_id=scheme_2021.id).first()
    if not sem1:
        sem1 = Semester(semester_no=1, scheme_id=scheme_2021.id)
        db.session.add(sem1)
        db.session.flush()

    # ---------- COURSE ----------
    dfca = Course.query.filter_by(
        name="Digital Fundamentals & Computer Architecture",
        semester_id=sem1.id
    ).first()

    if not dfca:
        dfca = Course(
            name="Digital Fundamentals & Computer Architecture",
            semester_id=sem1.id
        )
        db.session.add(dfca)
        db.session.flush()

    # ---------- MODULE 1 ----------
    m1 = Module(name="Module 1", hours=11, course_id=dfca.id)
    db.session.add(m1)
    db.session.flush()

    topics_m1 = [
        "Signed number representation",
        "Logic gates",
        "Boolean algebra",
        "K-map minimization"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------- MODULE 2 ----------
    m2 = Module(name="Module 2", hours=10, course_id=dfca.id)
    db.session.add(m2)
    db.session.flush()

    topics_m2 = [
        "Flip-flops",
        "Counters",
        "Registers"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    db.session.commit()
    print("✅ DFCA syllabus seeded successfully")
