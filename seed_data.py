from app import app
from models import db, Program, University, Semester, Course, Module, Topic

with app.app_context():

    # ---------- Program ----------
    mca = Program(name="MCA")
    db.session.add(mca)

    # ---------- University ----------
    ktu = University(name="KTU")
    db.session.add(ktu)

    db.session.commit()

    # ---------- Semester ----------
    s1 = Semester(semester_no=1, program_id=mca.id)
    db.session.add(s1)
    db.session.commit()

    # ---------- Course ----------
    dfca = Course(
        name="Digital Fundamentals & Computer Architecture",
        semester_id=s1.id
    )
    db.session.add(dfca)
    db.session.commit()

    # ---------- Modules & Topics ----------
    modules_data = [
        ("Module 1", 11, [
            "1’s & 2’s complement",
            "Logic gates",
            "Boolean algebra",
            "SOP & POS",
            "K-map minimization",
            "Floating point numbers",
            "Combinational circuits"
        ]),
        ("Module 2", 10, [
            "Sequential circuits",
            "Flip flops",
            "Counters",
            "Registers"
        ]),
        ("Module 3", 10, [
            "Computer abstractions",
            "Architecture design features",
            "Layers of abstraction",
            "Five key components",
            "Processor & memory technologies",
            "Performance basics",
            "Instruction set principles"
        ]),
        ("Module 4", 9, [
            "Processor basics",
            "Datapath building",
            "Pipelining",
            "Hazards",
            "I/O organization",
            "DMA"
        ]),
        ("Module 5", 8, [
            "Memory system basics",
            "SRAM & DRAM",
            "ROM types",
            "Cache memory",
            "Virtual memory"
        ])
    ]

    for title, hours, topics in modules_data:
        module = Module(
            title=title,
            hours=hours,
            course_id=dfca.id
        )
        db.session.add(module)
        db.session.commit()

        for t in topics:
            topic = Topic(title=t, module_id=module.id)
            db.session.add(topic)

        db.session.commit()

    print("✅ KTU MCA S1 DFCA syllabus seeded successfully!")
