from app import app
from models import db, Course, Module, Topic, Semester

with app.app_context():

    # 🔎 Get MCA Semester 1
    s1 = Semester.query.filter_by(semester_no=1).first()

    if not s1:
        print("❌ Semester 1 not found. Seed base academic data first.")
        exit()

    # 🔎 Create / Get ASE course
    ase = Course.query.filter_by(
        name="Advanced Software Engineering",
        semester_id=s1.id
    ).first()

    if not ase:
        ase = Course(
            name="Advanced Software Engineering",
            semester_id=s1.id
        )
        db.session.add(ase)
        db.session.commit()

    # ---------------- MODULE 1 ----------------
    m1 = Module(name="Module 1", hours=8, course_id=ase.id)
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Introduction to Software Engineering and characteristics of software",
        "Software life cycle: design, development, testing, deployment, maintenance",
        "Project planning: objectives, scope, estimation models, COCOMO",
        "Staffing and personnel planning",
        "Software engineering models: predictive and adaptive waterfall, Sashimi, incremental waterfall, V-model",
        "Prototyping and prototyping models",
        "Software requirements specification and elicitation",
        "Requirements engineering concepts and modelling",
        "Requirements documentation, use cases and user stories"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(name="Module 2", hours=10, course_id=ase.id)
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Programming style guides and coding standards",
        "Literate programming and software documentation",
        "Documentation generators: Javadoc, phpDocumentor",
        "Version control systems: basic concepts",
        "Distributed version control systems and Git",
        "Setting up Git and core operations",
        "Git CLI operations: clone, add, commit, log, diff",
        "Branching and conflict resolution",
        "Pushing changes and using Git with IDEs",
        "Software quality: requirements, design, development and conformance quality"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(name="Module 3", hours=10, course_id=ase.id)
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Object Oriented Programming concepts",
        "Design patterns: basic concepts and selection",
        "Creational design patterns",
        "Structural design patterns",
        "Behavioural design patterns",
        "Concept of anti-patterns",
        "Unit testing and unit testing frameworks",
        "xUnit architecture",
        "Writing unit tests using JUnit, unittest or phpdbg",
        "Assertions, custom assertions and testing for errors"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(name="Module 4", hours=10, course_id=ase.id)
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "Agile development concepts",
        "Scrum framework",
        "Software testing principles",
        "Program inspections, walkthroughs and reviews",
        "Black box testing techniques",
        "White box testing techniques",
        "Control flow and data flow testing",
        "Testing automation",
        "Defect life cycle",
        "Regression testing and non-functional testing"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(name="Module 5", hours=10, course_id=ase.id)
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "Software configuration management",
        "Managing dependencies and configurations",
        "Build and deployment environments",
        "Continuous integration prerequisites",
        "Essential CI practices",
        "Continuous delivery concepts",
        "Build and deployment automation",
        "Ansible for configuration management",
        "Test automation in CI",
        "Robot Framework for test automation"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ Advanced Software Engineering syllabus added successfully!")
