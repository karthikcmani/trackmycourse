from app import app
from models import db, Semester, Course, Module, Topic

with app.app_context():

    # 🔎 Get MCA Semester 1
    semester = Semester.query.filter_by(semester_no=1).first()

    if not semester:
        print("❌ Semester 1 not found. Seed base academic data first.")
        exit()

    # 🔎 Create / Get ADBMS course
    course_name = "Advanced Database Management Systems"

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
    m1 = Module(name="Module 1: Relational Databases", hours=10, course_id=course.id)
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Purpose of Database System",
        "Database System Applications",
        "View of Data: Abstraction, Instances and Schemas",
        "Data Models",
        "Database Architecture",
        "Database Users and DBA",
        "Relational Model Structure",
        "Keys and Schema",
        "Relational Query Language",
        "Relational Algebra (basic + additional operations)",
        "Entity Relationship Model",
        "Constraints (Mapping, Key, Participation)",
        "ER Diagrams and Mapping",
        "Extended ER Features (Specialization, Generalization, Aggregation)"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(name="Module 2: Database Design", hours=10, course_id=course.id)
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Database Tables and Need for Normalization",
        "Functional Dependencies",
        "Minimal Set of Functional Dependencies",
        "First Normal Form (1NF)",
        "Second Normal Form (2NF)",
        "Third Normal Form (3NF)",
        "Improving Design",
        "Surrogate Keys",
        "Boyce-Codd Normal Form (BCNF)",
        "Fourth Normal Form (4NF)",
        "Fifth Normal Form (5NF)",
        "Normalization in Database Design"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(name="Module 3: Transactions & Concurrency", hours=10, course_id=course.id)
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Transaction Concepts and Properties (ACID)",
        "Transaction Management with SQL",
        "Transaction Log",
        "Concurrency Problems (Lost Update, Dirty Read, Inconsistent Retrieval)",
        "Scheduler",
        "Locking Methods",
        "Two Phase Locking",
        "Deadlocks",
        "Timestamp Methods (Wait/Die, Wait/Wound)",
        "Optimistic Concurrency Control",
        "Database Recovery"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(name="Module 4: Storage & Querying", hours=8, course_id=course.id)
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "RAID",
        "File Organization",
        "Record Organization",
        "Indexing Concepts",
        "Ordered Indices",
        "B+ Tree Structure",
        "B Tree Index",
        "Static Hashing",
        "Dynamic Hashing",
        "Query Processing Overview",
        "Selection Operation"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(name="Module 5: Advanced & NoSQL", hours=10, course_id=course.id)
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "Distributed Databases",
        "Homogeneous and Heterogeneous Databases",
        "Distributed Storage and Transactions",
        "Object Oriented Databases",
        "Complex and Structured Types in SQL",
        "Inheritance in SQL",
        "XML and DTD",
        "XML Schema and Applications",
        "NoSQL Databases Overview",
        "MongoDB Sharding and Replication",
        "HBase",
        "Cassandra",
        "CAP Theorem"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ ADBMS syllabus added successfully!")