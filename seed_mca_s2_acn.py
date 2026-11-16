from app import app
from models import db, Semester, Course, Module, Topic

with app.app_context():

    # 🔎 Get MCA Semester 1
    semester = Semester.query.filter_by(semester_no=1).first()

    if not semester:
        print("❌ Semester 1 not found. Seed base academic data first.")
        exit()

    # 🔎 Create / Get ACN course
    course_name = "Advanced Computer Networks"

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
        name="Module 1: Computer Networks Overview & Application Layer",
        hours=10,
        course_id=course.id
    )
    db.session.add(m1)
    db.session.commit()

    topics_m1 = [
        "Overview of Computer Networks and Internet",
        "History of Computer Networks",
        "Network Protocols",
        "Last Mile Technologies for Internet Access",
        "Packet Switching",
        "Delay, Queuing and Throughput",
        "Quality of Service (QoS)",
        "Protocol Layering",
        "OSI Reference Model",
        "TCP/IP Model",
        "Application Layer Protocols",
        "Client-Server Architecture",
        "Network Layered Application Architecture",
        "World Wide Web",
        "HTTP",
        "FTP",
        "SMTP",
        "POP3",
        "DNS",
        "Peer-to-Peer File Sharing Networks"
    ]

    for t in topics_m1:
        db.session.add(Topic(name=t, module_id=m1.id))

    # ---------------- MODULE 2 ----------------
    m2 = Module(
        name="Module 2: Transport Layer Protocols",
        hours=10,
        course_id=course.id
    )
    db.session.add(m2)
    db.session.commit()

    topics_m2 = [
        "Introduction to Transport Layer",
        "Multiplexing",
        "De-Multiplexing",
        "Reliable Data Transfer Principles",
        "Stop-and-Wait Protocol",
        "Go-Back-N Protocol",
        "Design and Evaluation of Reliable Protocols",
        "Connection Oriented Transport",
        "Transmission Control Protocol (TCP)",
        "Connectionless Transport",
        "User Datagram Protocol (UDP)",
        "Congestion Control Principles",
        "Network Efficiency",
        "Fairness in Congestion Control"
    ]

    for t in topics_m2:
        db.session.add(Topic(name=t, module_id=m2.id))

    # ---------------- MODULE 3 ----------------
    m3 = Module(
        name="Module 3: Network Layer Protocols",
        hours=10,
        course_id=course.id
    )
    db.session.add(m3)
    db.session.commit()

    topics_m3 = [
        "Virtual Circuits",
        "Datagram Networks",
        "Routing Principles",
        "IPv4",
        "CIDR",
        "Link State Routing Algorithm",
        "Distance Vector Routing Algorithm",
        "Routing on the Internet",
        "RIP",
        "OSPF",
        "BGP",
        "Multicast Routing",
        "Introduction to IPv6",
        "Software Defined Networks",
        "OpenFlow"
    ]

    for t in topics_m3:
        db.session.add(Topic(name=t, module_id=m3.id))

    # ---------------- MODULE 4 ----------------
    m4 = Module(
        name="Module 4: Link Layer & Physical Layer",
        hours=8,
        course_id=course.id
    )
    db.session.add(m4)
    db.session.commit()

    topics_m4 = [
        "Introduction to Link Layer",
        "Error Detection Techniques",
        "Parity Check",
        "Checksum",
        "Cyclic Redundancy Check (CRC)",
        "Multiple Access Protocols",
        "Collision Based Protocols",
        "Token Based Protocols",
        "IEEE 802.3 Ethernet",
        "Switching",
        "Bridging",
        "Transmission Media",
        "Signal Strength",
        "Interference",
        "Data Encoding",
        "Ethernet Switches",
        "Routers",
        "MAC Addressing",
        "ARP",
        "Forwarding Information Base (FIB)"
    ]

    for t in topics_m4:
        db.session.add(Topic(name=t, module_id=m4.id))

    # ---------------- MODULE 5 ----------------
    m5 = Module(
        name="Module 5: Wireless Networks & Security",
        hours=10,
        course_id=course.id
    )
    db.session.add(m5)
    db.session.commit()

    topics_m5 = [
        "IEEE 802.11 Wi-Fi",
        "Bluetooth",
        "Cellular Networks",
        "Network Threats",
        "Network Attacks",
        "Network Address Translation (NAT)",
        "Firewalls",
        "Virtual Private Networks (VPN)",
        "Introduction to Network Management",
        "Simple Network Management Protocol (SNMP)",
        "Network Troubleshooting",
        "Traffic Analysis Tools",
        "Configuration Management"
    ]

    for t in topics_m5:
        db.session.add(Topic(name=t, module_id=m5.id))

    db.session.commit()

    print("✅ Advanced Computer Networks syllabus added successfully!")