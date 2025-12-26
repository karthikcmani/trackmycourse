from app import app
from models import db, Course, Module, Topic, Semester

with app.app_context():

    # 🔎 Get Semester 1 (MCA S1)
    s1 = Semester.query.filter_by(semester_no=1).first()

    # 🔎 Create / Get ADS course
    ads = Course.query.filter_by(
        name="Advanced Data Structures",
        semester_id=s1.id
    ).first()

    if not ads:
        ads = Course(
            name="Advanced Data Structures",
            semester_id=s1.id
        )
        db.session.add(ads)
        db.session.commit()

    # ---------------- MODULE 1 ----------------
    m1 = Module(
        name="Module 1",
        hours=12,
        course_id=ads.id
    )
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Review of basic data structures: Array, Linked List & variants, Stack, Queue, Trees",
        "Set Data Structure: Representation, Bit string implementation",
        "Hashing: Simple hash functions, Collision & resolution techniques",
        "Amortised Analysis: Aggregate, Accounting, Potential methods",
        "Disjoint Sets: Representation, Union-Find algorithms"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(
        name="Module 2",
        hours=10,
        course_id=ads.id
    )
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Balanced BST",
        "Red-Black Trees: properties, rotations, insertion, deletion",
        "B-Trees: insertion, deletion",
        "Introduction to Splay Trees",
        "Introduction to Suffix Trees"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(
        name="Module 3",
        hours=10,
        course_id=ads.id
    )
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Mergeable Heaps & operations",
        "Binomial Heaps: operations & analysis",
        "Fibonacci Heaps: operations & analysis"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(
        name="Module 4",
        hours=14,
        course_id=ads.id
    )
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "Graph representation",
        "Depth First Search (DFS)",
        "Breadth First Search (BFS)",
        "Topological Sorting",
        "Strongly Connected Components",
        "Biconnected Components",
        "Minimum Spanning Trees: Prim’s algorithm",
        "Minimum Spanning Trees: Kruskal’s algorithm",
        "Shortest Path: Dijkstra’s algorithm"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(
        name="Module 5",
        hours=8,
        course_id=ads.id
    )
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "Blockchain Data Structure: Architecture",
        "Blockchain Data Types",
        "Contract Data",
        "Problems in blockchain data analysis"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ Advanced Data Structures syllabus added successfully!")
