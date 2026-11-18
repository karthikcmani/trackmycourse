"""
TrackMyCourse — Idempotent Academic Catalog & Regression Scenario Seeder
Seeds and updates official academic data without creating duplicate records.
"""
from app import app
from models import db, University, Program, Scheme, Semester, Course, Module, Topic, SyllabusSource, UserProgress, ActivityLog

def seed_academic_catalog():
    with app.app_context():
        print("[*] Running idempotent academic catalog seeding...")

        # 1. KTU University
        ktu = University.query.filter_by(name="KTU").first()
        if not ktu:
            ktu = University(
                name="KTU",
                code="KTU",
                state="Kerala",
                country="India",
                website="https://ktu.edu.in"
            )
            db.session.add(ktu)
            db.session.commit()
            print("[+] Seeded University: KTU")

        # 2. MCA Program
        mca = Program.query.filter_by(name="MCA", university_id=ktu.id).first()
        if not mca:
            mca = Program(
                name="MCA",
                code="MCA",
                degree_type="Postgraduate",
                university_id=ktu.id
            )
            db.session.add(mca)
            db.session.commit()
            print("[+] Seeded Program: MCA")

        # 3. Scheme 2020 (Official KTU MCA Scheme 2020)
        scheme_2020 = Scheme.query.filter_by(year="2020", program_id=mca.id).first()
        if not scheme_2020:
            scheme_2020 = Scheme(year="2020", program_id=mca.id, stream_id=None)
            db.session.add(scheme_2020)
            db.session.commit()
            print("[+] Seeded Scheme: 2020")

        # 4. Semester 1
        s1 = Semester.query.filter_by(scheme_id=scheme_2020.id, semester_no=1).first()
        if not s1:
            s1 = Semester(semester_no=1, scheme_id=scheme_2020.id)
            db.session.add(s1)
            db.session.commit()
            print("[+] Seeded Semester 1")

        # 5. Advanced Software Engineering Course (20MCA105)
        ase = Course.query.filter_by(name="Advanced Software Engineering", semester_id=s1.id).first()
        if not ase:
            ase = Course(
                name="Advanced Software Engineering",
                code="20MCA105",
                credits=4,
                course_type="Theory",
                semester_id=s1.id
            )
            db.session.add(ase)
            db.session.commit()
            print("[+] Seeded Course: Advanced Software Engineering")
        elif not ase.code:
            ase.code = "20MCA105"
            db.session.commit()

        # ASE Modules and Topics definition (from official KTU syllabus)
        ase_curriculum = [
            {
                "module_name": "Module 1",
                "hours": 8,
                "topics": [
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
            },
            {
                "module_name": "Module 2",
                "hours": 10,
                "topics": [
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
            },
            {
                "module_name": "Module 3",
                "hours": 10,
                "topics": [
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
            },
            {
                "module_name": "Module 4",
                "hours": 10,
                "topics": [
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
            },
            {
                "module_name": "Module 5",
                "hours": 10,
                "topics": [
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
            }
        ]

        ase_topic_ids = []
        for mod_idx, mod_data in enumerate(ase_curriculum, 1):
            mod = Module.query.filter_by(name=mod_data["module_name"], course_id=ase.id).first()
            if not mod:
                mod = Module(
                    name=mod_data["module_name"],
                    module_no=mod_idx,
                    hours=mod_data["hours"],
                    course_id=ase.id
                )
                db.session.add(mod)
                db.session.commit()
            elif not mod.module_no:
                mod.module_no = mod_idx
                db.session.commit()

            for top_idx, top_name in enumerate(mod_data["topics"], 1):
                top = Topic.query.filter_by(name=top_name, module_id=mod.id).first()
                if not top:
                    top = Topic(
                        name=top_name,
                        topic_no=top_idx,
                        module_id=mod.id
                    )
                    db.session.add(top)
                    db.session.commit()
                ase_topic_ids.append(top.id)

        print(f"[+] Advanced Software Engineering has {len(ase_topic_ids)} topics verified.")

        # 6. Provenance source for ASE
        source = SyllabusSource.query.filter_by(course_id=ase.id).first()
        if not source:
            source = SyllabusSource(
                university_id=ktu.id,
                program_id=mca.id,
                scheme_id=scheme_2020.id,
                course_id=ase.id,
                document_title="20MCA105 - Advanced Software Engineering Curriculum",
                source_url="https://ktu.edu.in/eu/att/attachments.htm",
                publication_date="2020-07-01",
                verification_status="verified",
                version="2020.1",
                verified_by="KTU Academic Council",
                notes="Official APJ Abdul Kalam Technological University MCA Semester 1 Syllabus"
            )
            db.session.add(source)
            db.session.commit()
            print("[+] Seeded provenance source for Advanced Software Engineering.")

        # 7. Student Regression Scenario Verification:
        # User 1 should have ~88% completion (43 of 49 topics) for Advanced Software Engineering
        existing_ase_progress = UserProgress.query.join(Topic).join(Module).filter(
            Module.course_id == ase.id,
            UserProgress.user_id == 1
        ).count()

        if existing_ase_progress == 0:
            print("[*] Seeding verified regression progress: 43 of 49 topics (88%) for ASE...")
            for i, tid in enumerate(ase_topic_ids):
                is_done = i < 43  # 43 out of 49 = 87.75% -> 88%
                prog = UserProgress(
                    user_id=1,
                    topic_id=tid,
                    completed=is_done
                )
                db.session.add(prog)
            
            # Add activity log record
            activity = ActivityLog(
                user_id=1,
                activity_type="topic_completed",
                description="Completed 43 topics in Advanced Software Engineering (88% progress)",
                reference_id=ase.id
            )
            db.session.add(activity)
            db.session.commit()
            print("[+] Seeded 43/49 progress records (88%) for ASE!")
        else:
            print(f"[*] Found {existing_ase_progress} existing progress records for ASE.")

        print("[*] Academic catalog seeding completed successfully!")

if __name__ == "__main__":
    seed_academic_catalog()
