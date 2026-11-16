from app import app
from models import db, Semester, Course, Module, Topic

with app.app_context():

    # 🔎 Get MCA Semester 1
    semester = Semester.query.filter_by(semester_no=1).first()

    if not semester:
        print("❌ Semester 1 not found. Seed base academic data first.")
        exit()

    # 🔎 Create / Get Mathematics course
    course_name = "Mathematical Foundations for Computing"

    course = Course.query.filter_by(
        name=course_name,
        semester_id=semester.id
    ).first()

    if not course:
        course = Course(
            name=course_name,
    
            semester_id=semester.id
        )
        db.session.add(course)
        db.session.commit()

    # ---------------- MODULE 1 ----------------
    m1 = Module(
        name="Module 1",
        hours=9,
        course_id=course.id
    )
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Sets and set operations",
        "Relations and classification of relations",
        "Equivalence relations",
        "Closures of relations",
        "Matrix representation of relations",
        "Partial ordering",
        "n-ary relations",
        "Functions"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(
        name="Module 2",
        hours=10,
        course_id=course.id
    )
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Division algorithm",
        "Greatest Common Divisor (GCD)",
        "Prime numbers",
        "Euclidean algorithm",
        "Congruences and properties of congruences",
        "Solutions of linear congruences",
        "First order linear recurrence relations",
        "Second order linear homogeneous recurrence relations with constant coefficients",
        "Non-homogeneous recurrence relations"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(
        name="Module 3",
        hours=10,
        course_id=course.id
    )
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Graphs and graph models",
        "Graph terminology and special types of graphs",
        "Graph representation and graph isomorphism",
        "Connectivity in graphs",
        "Euler paths and Hamilton paths",
        "Shortest path problems",
        "Planar graphs",
        "Directed graphs",
        "Multigraphs",
        "Connected graphs",
        "Euler circuit and trail",
        "Planar and non-planar graphs"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(
        name="Module 4",
        hours=10,
        course_id=course.id
    )
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "Linear systems of equations",
        "Coefficient matrix and augmented matrix",
        "Gauss elimination method and back substitution",
        "Elementary row operations",
        "Row equivalent systems",
        "Row echelon form and its interpretation",
        "Linear independence and rank of a matrix",
        "Solutions of linear systems",
        "Fundamental theorem of non-homogeneous linear systems",
        "Homogeneous linear systems (theory)",
        "Eigen values and eigen vectors",
        "Diagonalization of matrices",
        "Quadratic forms and principle axis theorem"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(
        name="Module 5",
        hours=10,
        course_id=course.id
    )
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "Bivariate data and scatter diagrams",
        "Interpretation of scatter diagrams",
        "Curve fitting",
        "Principle of least squares",
        "Fitting a straight line",
        "Fitting a parabola",
        "Linear correlation and regression",
        "Karl Pearson’s coefficient of correlation",
        "Spearman’s rank correlation coefficient"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ Mathematics syllabus (MCA S1) added successfully!")

