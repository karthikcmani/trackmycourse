from app import app
from models import db, Semester, Course, Module, Topic

with app.app_context():

    # 🔎 Get MCA Semester 1
    semester = Semester.query.filter_by(semester_no=1).first()

    if not semester:
        print("❌ Semester 1 not found. Seed base academic data first.")
        exit()

    # 🔎 Create / Get AI course
    course_name = "Artificial Intelligence"

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
        name="Module 1: Introduction to AI and Production Systems",
        hours=10,
        course_id=course.id
    )
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Introduction to Artificial Intelligence",
        "Problem Formulation",
        "Problem Definition",
        "Production Systems",
        "Problem Characteristics",
        "Production System Characteristics",
        "8 Puzzle Problem",
        "Missionary Cannibals Problem",
        "Crypt Arithmetic Problems",
        "Block World Problem"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(
        name="Module 2: Search Strategies",
        hours=10,
        course_id=course.id
    )
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Blind Search Strategies",
        "Depth First Search (DFS)",
        "Breadth First Search (BFS)",
        "Best First Search",
        "Iterative Deepening Search",
        "Heuristic Search Strategies",
        "Admissible Heuristics",
        "Examples of Admissible Heuristics",
        "Simple Hill Climbing",
        "Steepest Ascending Hill Climbing",
        "Simulated Annealing",
        "A* Algorithm"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(
        name="Module 3: Game Playing and Knowledge Representation",
        hours=10,
        course_id=course.id
    )
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Two Player Zero Sum Games",
        "Modelling Two Player Zero Sum Games as Search Problems",
        "Min-Max Algorithm",
        "Alpha-Beta Pruning (α-β Cutoff)",
        "Knowledge Representation",
        "Frames",
        "Semantic Networks",
        "Conceptual Dependencies"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(
        name="Module 4: Logic and Planning",
        hours=10,
        course_id=course.id
    )
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "First Order Predicate Logic (FOPL)",
        "Well Formed Formula (WFF) in FOPL",
        "Inference Rules for FOPL",
        "Clause Form",
        "Conversion of WFFs to Clause Form",
        "Resolution Refutation",
        "Planning Overview",
        "Components of a Planning System",
        "Goal Stack Planning",
        "Hierarchical Planning"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(
        name="Module 5: Learning, Expert Systems and Fuzzy Logic",
        hours=10,
        course_id=course.id
    )
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "Forms of Learning",
        "Neural Net Learning",
        "Genetic Learning",
        "Expert Systems",
        "Architecture of Expert Systems",
        "Roles of Expert Systems",
        "Languages and Tools for Expert Systems",
        "Typical Expert System Examples",
        "Fuzzy Logic",
        "Fuzzy Variables",
        "Fuzzy Sets",
        "Fuzzy Set Operations",
        "Applications of Fuzzy Sets"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ Artificial Intelligence syllabus added successfully!")