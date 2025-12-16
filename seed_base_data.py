from app import app
from models import db, University, Program, Stream, Scheme, Semester, Course

with app.app_context():
    # ---------- University ----------
    ktu = University(name="KTU")
    db.session.add(ktu)
    db.session.commit()

    # ---------- Programs ----------
    mca = Program(name="MCA", university_id=ktu.id)
    btech = Program(name="BTech", university_id=ktu.id)
    db.session.add_all([mca, btech])
    db.session.commit()

    # ---------- Streams (only for BTech) ----------
    cse = Stream(name="Computer Science & Engineering", program_id=btech.id)
    db.session.add(cse)
    db.session.commit()

    # ---------- Schemes ----------
    mca_2021 = Scheme(year="2021", program_id=mca.id, stream_id=None)
    btech_cse_2019 = Scheme(year="2019", program_id=btech.id, stream_id=cse.id)
    btech_cse_2024 = Scheme(year="2024", program_id=btech.id, stream_id=cse.id)
    db.session.add_all([mca_2021, btech_cse_2019, btech_cse_2024])
    db.session.commit()

    # ---------- Semesters ----------
    semesters = []
    for s in range(1, 3):  # keep minimal for now
        semesters.append(Semester(semester_no=s, scheme_id=mca_2021.id))
        semesters.append(Semester(semester_no=s, scheme_id=btech_cse_2019.id))
        semesters.append(Semester(semester_no=s, scheme_id=btech_cse_2024.id))
    db.session.add_all(semesters)
    db.session.commit()

    # ---------- Courses (sample placeholders) ----------
    # MCA S1
    mca_s1 = Semester.query.filter_by(scheme_id=mca_2021.id, semester_no=1).first()
    db.session.add(Course(name="Digital Fundamentals & Computer Architecture", semester_id=mca_s1.id))

    # BTech CSE S1
    btech_s1_2019 = Semester.query.filter_by(scheme_id=btech_cse_2019.id, semester_no=1).first()
    db.session.add(Course(name="Programming in C", semester_id=btech_s1_2019.id))

    db.session.commit()

    print("✅ Base academic data seeded successfully!")
