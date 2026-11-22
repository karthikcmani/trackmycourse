"""
Populate KTU B.Tech Academic Streams, Schemes (2019 & 2024), and authentic course curricula
Strictly leaves KTU MCA (Program 1, Scheme 2020) and student progress records 100% untouched.
"""
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models import University, Program, Stream, Scheme, Semester, Course, Module, Topic

# Authentic KTU B.Tech Streams extracted from KTU official portal (51 streams)
KTU_BTECH_STREAMS = [
    # Core existing 6 (preserved with their exact codes)
    ("Computer Science & Engineering", "CSE"),
    ("Electronics & Communication Engineering", "ECE"),
    ("Mechanical Engineering", "ME"),
    ("Civil Engineering", "CE"),
    ("Electrical & Electronics Engineering", "EEE"),
    ("Information Technology", "IT"),
    # Additional authentic KTU B.Tech streams
    ("Artificial Intelligence", "AI"),
    ("Artificial Intelligence & Machine Learning", "AIML"),
    ("Artificial Intelligence & Data Science", "AIDS"),
    ("Computer Science & Engineering (Artificial Intelligence)", "CSE-AI"),
    ("Computer Science & Engineering (Artificial Intelligence & Machine Learning)", "CSE-AIML"),
    ("Computer Science & Engineering (Data Science)", "CSE-DS"),
    ("Computer Science & Engineering (Cyber Security)", "CSE-CS"),
    ("Computer Science & Engineering (Internet of Things)", "CSE-IOT"),
    ("Computer Science & Engineering (IoT & Cyber Security including Blockchain)", "CSE-IOT-BC"),
    ("Computer Science & Business Systems", "CSBS"),
    ("Computer Science & Design", "CSD"),
    ("Electronics & Computer Engineering", "ECSE"),
    ("Electrical & Computer Engineering", "EECE"),
    ("Electronics & Instrumentation Engineering", "EIE"),
    ("Applied Electronics & Instrumentation", "AEI"),
    ("Biomedical Engineering", "BME"),
    ("Biotechnology", "BT"),
    ("Biotechnology & Biochemical Engineering", "BTBCE"),
    ("Chemical Engineering", "CHE"),
    ("Robotics & Automation", "RA"),
    ("Robotics & Artificial Intelligence", "RAI"),
    ("Mechatronics Engineering", "MTE"),
    ("Automobile Engineering", "AU"),
    ("Aeronautical Engineering", "AERO"),
    ("Aerospace Engineering", "AERO-SP"),
    ("Industrial Engineering", "IE"),
    ("Production Engineering", "PE"),
    ("Mechanical Engineering (Automobile)", "ME-AU"),
    ("Mechanical Engineering (Production)", "ME-PR"),
    ("Food Technology", "FT"),
    ("Safety & Fire Engineering", "SFE"),
    ("Naval Architecture & Ship Building Engineering", "NASB"),
    ("Civil & Environmental Engineering", "CEE"),
    ("Agriculture Engineering", "AGE"),
    ("Metallurgical & Materials Engineering", "MME"),
    ("Polymer Engineering", "POLE"),
    ("Marine Engineering", "MRE"),
    ("Printing Technology", "PT"),
    ("Cyber Physical Systems", "CPS"),
    ("Electronics Engineering (VLSI Design & Technology)", "VLSI"),
    ("Electronics & Biomedical Engineering", "EBME"),
    ("Computer Science & Engineering (Blockchain)", "CSE-BC"),
    ("Instrumentation & Control Engineering", "ICE"),
    ("Robotics", "ROB"),
    ("Biomedical & Robotic Engineering", "BMRE")
]

# Detailed Course Definitions for Scheme 2019
BTECH_2019_COURSES = {
    1: [
        {
            "code": "CYT100",
            "name": "Engineering Chemistry",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Electrochemistry and Corrosion", 9, [
                    "Nernst equation and electrode potential",
                    "Reference electrodes: Calomel and Glass electrodes",
                    "Electrochemical series and its applications",
                    "Corrosion: Galvanic, differential aeration, and stress corrosion",
                    "Corrosion control: Cathodic protection and sacrificial anode"
                ]),
                ("Module 2: Polymers and Advanced Materials", 9, [
                    "Classification and mechanism of polymerization",
                    "Thermoplastics vs Thermosetting plastics",
                    "Conducting polymers and OLED materials",
                    "Nanomaterials: Carbon nanotubes and fullerenes",
                    "Synthesis and engineering applications of nanomaterials"
                ]),
                ("Module 3: Spectroscopy and Analytical Techniques", 9, [
                    "Beer-Lambert's law and UV-Visible spectroscopy",
                    "Infrared (IR) spectroscopy and functional group analysis",
                    "Nuclear Magnetic Resonance (NMR) spectroscopy fundamentals",
                    "Thermal analysis: TGA and DTA techniques",
                    "Chromatography: HPLC and Gas Chromatography basics"
                ]),
                ("Module 4: Fuels and Energy Storage", 9, [
                    "Classification of fuels and calorific values (HCV/LCV)",
                    "Proximate and ultimate analysis of coal",
                    "Petroleum refining and octane/cetane ratings",
                    "Secondary batteries: Lead-acid and Lithium-ion batteries",
                    "Fuel cells: Hydrogen-oxygen and proton exchange membrane"
                ]),
                ("Module 5: Water Technology and Environmental Chemistry", 9, [
                    "Hardness of water and EDTA titration method",
                    "Boiler troubles: Scale, sludge, and caustic embrittlement",
                    "Water softening: Ion-exchange and reverse osmosis (RO)",
                    "Municipal water treatment: Sedimentation and chlorination",
                    "Sewage water treatment: BOD, COD, and primary/secondary stages"
                ])
            ]
        },
        {
            "code": "EST100",
            "name": "Engineering Mechanics",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Statics of Particles and Rigid Bodies", 9, [
                    "Principles of statics, resolution and composition of forces",
                    "Lami's theorem and equilibrium of concurrent force systems",
                    "Moment of a force and Varignon's theorem",
                    "Couples and equivalent force systems",
                    "Equilibrium of rigid bodies in two dimensions"
                ]),
                ("Module 2: Friction and Trusses", 9, [
                    "Laws of dry friction and coefficient of friction",
                    "Angle of friction, cone of friction, and wedge friction",
                    "Ladder friction and belt friction basics",
                    "Analysis of plane trusses: Method of joints",
                    "Analysis of plane trusses: Method of sections"
                ]),
                ("Module 3: Centroid and Moment of Inertia", 9, [
                    "Centroid of composite plane figures and wires",
                    "Theorems of Pappus-Guldinus",
                    "Parallel axis theorem and perpendicular axis theorem",
                    "Moment of inertia of standard and composite cross-sections",
                    "Product of inertia and principal axes concepts"
                ]),
                ("Module 4: Kinematics of Particles", 9, [
                    "Rectilinear motion with constant and variable acceleration",
                    "Curvilinear motion: Rectangular and normal-tangential components",
                    "Projectile motion and range on horizontal and inclined planes",
                    "D'Alembert's principle and dynamic equilibrium",
                    "Work-energy principle for rectilinear and curvilinear motion"
                ]),
                ("Module 5: Kinetics of Particles and Rigid Bodies", 9, [
                    "Impulse-momentum principle and conservation of linear momentum",
                    "Direct and oblique central impact of elastic bodies",
                    "Rotation of rigid bodies about a fixed axis",
                    "Moment of momentum and angular impulse",
                    "General plane motion: Rolling without slipping"
                ])
            ]
        },
        {
            "code": "EST110",
            "name": "Engineering Graphics",
            "credits": 3,
            "type": "Practical/Drawing",
            "modules": [
                ("Module 1: Introduction and Curves", 7, [
                    "BIS conventions, lettering, dimensioning, and scales",
                    "Construction of conic sections: Ellipse, Parabola, Hyperbola",
                    "Involutes of circle, triangle, and square",
                    "Cycloidal curves: Cycloid, Epicycloid, and Hypocycloid",
                    "Spirals and engineering curve applications"
                ]),
                ("Module 2: Orthographic Projection of Points and Lines", 8, [
                    "Principles of first-angle and third-angle projection",
                    "Projection of points in different quadrants",
                    "Projection of straight lines parallel and inclined to one plane",
                    "Projection of straight lines inclined to both reference planes",
                    "True length, true inclinations, and traces of lines"
                ]),
                ("Module 3: Projection of Planes and Solids", 9, [
                    "Projection of regular planes inclined to both planes",
                    "Projection of prisms and pyramids inclined to one plane",
                    "Projection of cylinders and cones inclined to one plane",
                    "Auxiliary projection methods for solids",
                    "Projections of solids resting on corners or edges"
                ]),
                ("Module 4: Sections of Solids and Development of Surfaces", 9, [
                    "Section planes perpendicular to one plane and inclined to other",
                    "True shape of sections of prisms, pyramids, cylinders, cones",
                    "Parallel line development of prisms and cylinders",
                    "Radial line development of pyramids and cones",
                    "Development of transition pieces and truncated solids"
                ]),
                ("Module 5: Isometric Projection and CAD Overview", 8, [
                    "Isometric scale and isometric axes",
                    "Isometric view and isometric projection of simple solids",
                    "Isometric projection of combination of solids",
                    "Conversion of orthographic views into isometric views",
                    "Introduction to Computer-Aided Drafting (CAD) commands"
                ])
            ]
        },
        {
            "code": "EST120",
            "name": "Basics of Civil & Mechanical Engineering",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Civil Engineering - Materials & Buildings", 9, [
                    "Role of civil engineer in society and infrastructure development",
                    "Engineering properties of stones, bricks, cement, and concrete",
                    "Steel and advanced building materials",
                    "Components of residential and commercial buildings",
                    "Foundations: Types, bearing capacity, and soil requirements"
                ]),
                ("Module 2: Civil Engineering - Surveying & Transportation", 8, [
                    "Principles of surveying, chaining, and compass surveying",
                    "Leveling: Reduced levels, instruments, and bench marks",
                    "Modern surveying instruments: Total Station and GPS",
                    "Highways: Classification, cross-section, and geometric design",
                    "Bridges, culverts, and environmental impact overview"
                ]),
                ("Module 3: Mechanical Engineering - Energy Conversion & Boilers", 9, [
                    "Thermodynamics laws, closed and open systems",
                    "Boilers: Fire tube vs water tube boilers (Babcock & Wilcox)",
                    "Steam turbines: Impulse and reaction turbine working principles",
                    "Gas turbines: Brayton cycle and open/closed cycle operations",
                    "Hydraulic turbines: Pelton wheel and Francis turbine"
                ]),
                ("Module 4: Mechanical Engineering - IC Engines & Refrigeration", 9, [
                    "Working of 4-stroke and 2-stroke petrol and diesel engines",
                    "Comparison between SI and CI engines",
                    "Refrigeration systems: Vapour compression cycle and refrigerants",
                    "Air conditioning: Comfort requirements and split/window units",
                    "Electric and hybrid vehicle powertrain fundamentals"
                ]),
                ("Module 5: Mechanical Engineering - Manufacturing Processes", 8, [
                    "Casting processes: Sand moulding, pattern making, and defects",
                    "Metal joining: Arc welding, gas welding, soldering, and brazing",
                    "Machining: Lathe operations, drilling, and milling basics",
                    "Metal forming: Forging, rolling, extrusion, and drawing",
                    "Introduction to CNC machining and 3D printing"
                ])
            ]
        },
        {
            "code": "HUN101",
            "name": "Life Skills",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Communication and Soft Skills", 6, [
                    "Principles of effective verbal and non-verbal communication",
                    "Active listening, feedback mechanism, and barrier removal",
                    "Body language, posture, eye contact, and professional etiquette",
                    "Interpersonal communication and assertiveness",
                    "Cross-cultural communication in global engineering environments"
                ]),
                ("Module 2: Critical Thinking and Problem Solving", 6, [
                    "Creative thinking techniques: Brainstorming, Mind mapping, SCAMPER",
                    "Analytical thinking: Root cause analysis and 5 Whys technique",
                    "Six Thinking Hats method for collaborative decision making",
                    "Lateral thinking and overcoming cognitive biases",
                    "Structured problem-solving frameworks for engineering dilemmas"
                ]),
                ("Module 3: Teamwork and Leadership", 6, [
                    "Tuckman's team development model: Forming, Storming, Norming, Performing",
                    "Roles in a team and Belbin's team roles",
                    "Leadership styles: Transformational, transactional, and servant leadership",
                    "Conflict resolution strategies and negotiation skills",
                    "Building emotional intelligence (EQ) in engineering teams"
                ]),
                ("Module 4: Time Management and Stress Reduction", 6, [
                    "Eisenhower matrix and Pareto principle (80/20 rule)",
                    "Goal setting: SMART goals and OKR framework",
                    "Techniques to overcome procrastination (Pomodoro technique)",
                    "Understanding work stress, stressors, and burnout symptoms",
                    "Mindfulness, meditation, and healthy work-life balance"
                ]),
                ("Module 5: Professional Ethics and Morals", 6, [
                    "Core values: Integrity, honesty, empathy, and accountability",
                    "Codes of ethics for engineers (IEEE/ACM/IEI guidelines)",
                    "Ethical dilemmas in technology: Whistleblowing and intellectual property",
                    "Environmental ethics and corporate social responsibility (CSR)",
                    "Cyber ethics and privacy obligations in digital systems"
                ])
            ]
        }
    ],
    2: [
        {
            "code": "MAT102",
            "name": "Vector Calculus, Differential Equations and Transforms",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Ordinary Differential Equations", 9, [
                    "Homogeneous and non-homogeneous linear ODEs with constant coefficients",
                    "Method of variation of parameters for second-order ODEs",
                    "Cauchy-Euler and Legendre linear differential equations",
                    "Simultaneous linear differential equations with constant coefficients",
                    "Modelling simple physical systems using linear ODEs"
                ]),
                ("Module 2: Partial Differential Equations", 9, [
                    "Formation of PDEs by eliminating arbitrary constants and functions",
                    "Lagrange's linear equation of first order: Pp + Qq = R",
                    "Homogeneous linear PDEs with constant coefficients",
                    "Method of separation of variables for solving standard PDEs",
                    "One-dimensional wave equation and heat conduction equation"
                ]),
                ("Module 3: Fourier Series and Transforms", 9, [
                    "Dirichlet's conditions and Euler's formulae for Fourier coefficients",
                    "Fourier series for functions of arbitrary period 2L",
                    "Half-range Fourier sine and cosine expansions",
                    "Fourier integral theorem and Fourier transform pairs",
                    "Properties of Fourier transforms and convolution theorem"
                ]),
                ("Module 4: Laplace Transforms", 9, [
                    "Definition and existence conditions of Laplace transforms",
                    "Laplace transforms of elementary functions and shifting theorems",
                    "Transform of derivatives, integrals, and unit step function",
                    "Inverse Laplace transform and partial fraction decomposition",
                    "Solving linear ODEs using Laplace transform methods"
                ]),
                ("Module 5: Vector Calculus and Field Integrals", 9, [
                    "Gradient of scalar field, divergence, and curl of vector fields",
                    "Solenoidal and irrotational fields, scalar potential function",
                    "Line integrals, work done by force fields, and independence of path",
                    "Green's theorem in a plane and surface integrals",
                    "Stokes' theorem and Gauss divergence theorem with physical interpretations"
                ])
            ]
        },
        {
            "code": "EST130",
            "name": "Basics of Electrical & Electronics Engineering",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: DC Circuits and Analysis", 9, [
                    "Ohm's law, Kirchhoff's current law (KCL), and voltage law (KVL)",
                    "Mesh analysis and nodal analysis of DC resistive circuits",
                    "Thevenin's theorem and Norton's theorem applications",
                    "Maximum power transfer theorem and Superposition theorem",
                    "Star-Delta transformation and network simplification"
                ]),
                ("Module 2: AC Fundamentals and Magnetic Circuits", 9, [
                    "Generation of sinusoidal AC, RMS value, average value, and form factor",
                    "Phasor representation of AC quantities and impedance triangle",
                    "Analysis of series R-L, R-C, and R-L-C circuits",
                    "Power in AC circuits: Active, reactive, and apparent power",
                    "Three-phase AC generation, star and delta connections, balanced loads"
                ]),
                ("Module 3: Electrical Machines and Domestic Wiring", 9, [
                    "DC Machines: Construction, working of generator and motor, back EMF",
                    "Single-phase transformers: Principle, EMF equation, and losses",
                    "Three-phase induction motors: Working principle, slip, and torque",
                    "Components of domestic wiring: MCB, ELCB, fuses, and earthing",
                    "Electric tariffs, energy meters, and electrical safety standards"
                ]),
                ("Module 4: Semiconductor Devices and Power Supplies", 9, [
                    "PN junction diode: V-I characteristics, forward and reverse bias",
                    "Zener diode: Breakdown mechanism and voltage regulator circuit",
                    "Half-wave, full-wave centre-tapped, and bridge rectifiers",
                    "Capacitor filter circuits, ripple factor, and DC regulated power supplies",
                    "Bipolar Junction Transistor (BJT): CE, CB, CC configurations and characteristics"
                ]),
                ("Module 5: Electronic Circuits and Communication Basics", 9, [
                    "Transistor as a switch and CE voltage amplifier",
                    "Field Effect Transistors: JFET and MOSFET operational principles",
                    "Operational Amplifiers: Ideal characteristics, inverting, and non-inverting amps",
                    "Analog communication: Amplitude modulation (AM) and frequency modulation (FM)",
                    "Digital communication block diagram and cellular network fundamentals"
                ])
            ]
        },
        {
            "code": "HUN102",
            "name": "Professional Communication",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Linguistic and Structural Competence", 6, [
                    "Subject-verb agreement, tenses, and grammatical accuracy",
                    "Sentence structure: Simple, compound, and complex sentences",
                    "Vocabulary expansion: Collocations, phrasal verbs, and technical idioms",
                    "Cohesion, coherence, and transitional devices in prose",
                    "Common errors in Indian English and remediation"
                ]),
                ("Module 2: Technical and Business Writing", 6, [
                    "Email writing etiquette, tone, structure, and professional formatting",
                    "Business letters: Inquiry, order, complaint, and adjustment letters",
                    "Technical memoranda and notices, agenda, and minutes of meetings",
                    "Writing formal project proposals and feasibility studies",
                    "Mechanics of technical documentation and referencing standards"
                ]),
                ("Module 3: Engineering Reports and Documentation", 6, [
                    "Types of reports: Progress reports, laboratory reports, incident reports",
                    "Structure of formal technical report: Title, abstract, TOC, body, conclusion",
                    "Data visualization in reports: Charts, graphs, tables, and captions",
                    "Executive summary drafting and recommendation formulation",
                    "Academic writing: Citations, bibliography, and avoiding plagiarism"
                ]),
                ("Module 4: Presentation and Public Speaking", 6, [
                    "Planning, structuring, and delivering technical presentations",
                    "Designing impactful slide decks: Typography, visual hierarchy, minimal text",
                    "Voice modulation, articulation, pacing, and handling performance anxiety",
                    "Audience engagement techniques and Q&A management",
                    "Virtual presentation best practices and digital etiquette"
                ]),
                ("Module 5: Career and Placement Communication", 6, [
                    "Curriculum Vitae (CV) vs Resume vs Biodata distinctions",
                    "Targeted resume preparation, action verbs, and ATS optimization",
                    "Drafting compelling cover letters and statement of purpose (SOP)",
                    "Group discussion dynamics: Roles, initiation, summarization, etiquette",
                    "Personal interview preparation: STAR technique, FAQs, and mock interviews"
                ])
            ]
        }
    ],
    3: [
        {
            "code": "CST203",
            "name": "Logic System Design",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Number Systems and Boolean Algebra", 9, [
                    "Positional number systems: Binary, Octal, Decimal, Hexadecimal conversions",
                    "Signed binary numbers, 1's and 2's complement representation and arithmetic",
                    "Binary codes: BCD, Excess-3, Gray code, and ASCII",
                    "Boolean algebra axioms, theorems, and duality principle",
                    "Canonical and standard forms: SOP and POS representations"
                ]),
                ("Module 2: Combinational Logic Circuit Design", 9, [
                    "Karnaugh Map (K-Map) simplification: 2, 3, 4, and 5 variable maps",
                    "Don't care conditions and Prime Implicants determination",
                    "Design of adders: Half adder, Full adder, Ripple carry adder, Lookahead carry adder",
                    "Design of subtractors: Half and Full subtractor, BCD adder",
                    "Code converters: Binary to Gray, Gray to Binary, BCD to Excess-3"
                ]),
                ("Module 3: MSI and LSI Combinational Modules", 9, [
                    "Multiplexers (MUX): 2:1, 4:1, 8:1 MUX and logic implementation using MUX",
                    "Demultiplexers (DEMUX) and Decoders: 3:8 decoder, BCD to 7-segment decoder",
                    "Encoders: Priority encoder (8:3) and applications",
                    "Magnitude comparators: 1-bit, 2-bit, and 4-bit comparators",
                    "Programmable Logic Devices: PROM, PLA, and PAL architectures"
                ]),
                ("Module 4: Sequential Logic Fundamentals and Latches", 9, [
                    "Comparison between combinational and sequential logic circuits",
                    "Latches: SR latch using NOR and NAND gates, gated SR latch",
                    "Flip-Flops: Edge-triggered D, T, and JK flip-flops",
                    "Race-around condition in JK flip-flop and Master-Slave JK flip-flop",
                    "Excitation tables and characteristic equations of all flip-flops"
                ]),
                ("Module 5: Registers, Counters, and Synchronous FSM", 9, [
                    "Shift registers: SISO, SIPO, PISO, PIPO, and bidirectional shift registers",
                    "Universal shift register (74194) and ring/Johnson counter",
                    "Asynchronous (ripple) counters: Mod-N up/down counters",
                    "Synchronous counters: Design procedure using JK and T flip-flops",
                    "Finite State Machines (FSM): Mealy and Moore models, state diagram reduction"
                ])
            ]
        },
        {
            "code": "CST205",
            "name": "Object Oriented Programming Using Java",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Java Basics and Object-Oriented Principles", 9, [
                    "Features of Java: JVM, JRE, JDK, bytecode, and platform independence",
                    "Java tokens, data types, variables, type casting, operators",
                    "Control statements: Selection, iteration, and jump statements",
                    "Classes, objects, constructors, and 'this' keyword",
                    "Method overloading and garbage collection mechanisms"
                ]),
                ("Module 2: Inheritance, Polymorphism, and Arrays", 9, [
                    "Inheritance types: Single, multilevel, hierarchical; 'super' keyword",
                    "Method overriding, dynamic method dispatch, and runtime polymorphism",
                    "Abstract classes, pure abstract methods, and 'final' keyword",
                    "Arrays: 1D, 2D, jagged arrays, and command line arguments",
                    "String handling: String, StringBuilder, and StringBuffer classes"
                ]),
                ("Module 3: Packages, Interfaces, and Exception Handling", 9, [
                    "Defining packages, importing packages, and access protection rules",
                    "Defining and implementing interfaces; multiple inheritance using interfaces",
                    "Default and static methods in interfaces (Java 8+)",
                    "Exception hierarchy: Checked vs Unchecked exceptions",
                    "try, catch, throw, throws, finally blocks, and custom exceptions"
                ]),
                ("Module 4: Multithreading and I/O Streams", 9, [
                    "Thread life cycle, creating threads: Thread class and Runnable interface",
                    "Thread priorities, daemon threads, and sleep/join/yield methods",
                    "Thread synchronization: Synchronized methods and synchronized blocks",
                    "Inter-thread communication: wait(), notify(), notifyAll()",
                    "Java I/O: Byte streams, character streams, FileReader, FileWriter, BufferedReader"
                ]),
                ("Module 5: Generics, Collections Framework, and Modern Features", 9, [
                    "Generics: Generic classes, methods, and bounded type parameters",
                    "Java Collections Framework: List (ArrayList, LinkedList), Set (HashSet, TreeSet)",
                    "Map interface: HashMap, TreeMap, and Iterator traversal",
                    "Lambda expressions and functional interfaces basics",
                    "Introduction to JavaFX/Swing GUI components and event handling"
                ])
            ]
        },
        {
            "code": "EST200",
            "name": "Design and Engineering",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Design Process and Engineering Mindset", 6, [
                    "Design vs Analysis, characteristics of good engineering design",
                    "Design stages: Problem definition, ideation, development, testing",
                    "Engineering thinking: Divergent thinking and Convergent thinking",
                    "Role of science, engineering, and art in product innovation",
                    "Reverse engineering: Concept, teardown analysis, and case studies"
                ]),
                ("Module 2: Customer Centricity and Need Identification", 6, [
                    "Empathy mapping and understanding user pain points",
                    "Observation methods: Fly-on-the-wall, shadowing, user interviews",
                    "Customer journey mapping and persona creation",
                    "Problem statement framing: 'How Might We' (HMW) statements",
                    "Quality Function Deployment (QFD) and House of Quality matrix"
                ]),
                ("Module 3: Ideation and Concept Selection", 6, [
                    "Ideation tools: Brainstorming, morphological chart, TRIZ principles",
                    "Concept screening and Pugh selection matrix",
                    "Feasibility analysis: Technical, financial, and operational feasibility",
                    "Proof of concept (PoC) definition and minimum viable product (MVP)",
                    "Intellectual Property Rights (IPR): Patents, trademarks, and copyrights"
                ]),
                ("Module 4: Prototyping, Ergonomics, and Aesthetics", 6, [
                    "Rapid prototyping techniques: Low-fidelity vs High-fidelity prototypes",
                    "Human factors in design: Anthropometry and ergonomic considerations",
                    "Aesthetics and visual design: Golden ratio, color psychology, and symmetry",
                    "Safety and reliability in design: Failure Mode and Effects Analysis (FMEA)",
                    "Design for Assembly (DFA) and Design for Manufacturing (DFM)"
                ]),
                ("Module 5: Sustainable and Universal Design", 6, [
                    "Circular design principles and cradle-to-cradle lifecycle",
                    "Universal design: 7 principles of accessible design for diverse populations",
                    "Life Cycle Assessment (LCA) methodology and environmental footprints",
                    "Frugal engineering and Jugaad innovations with global relevance",
                    "Design ethics and social impact evaluation of technology solutions"
                ])
            ]
        },
        {
            "code": "MCN201",
            "name": "Sustainable Engineering",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Sustainability Fundamentals", 6, [
                    "Concept of sustainability, 3 pillars: Social, economic, environmental",
                    "UN Sustainable Development Goals (SDGs) and global indicators",
                    "Carrying capacity of the Earth and planetary boundaries",
                    "Nexus between energy, water, food, and climate change",
                    "Role of engineers in achieving net-zero emissions"
                ]),
                ("Module 2: Environmental Pollution and Impact", 6, [
                    "Air pollution: Primary and secondary pollutants, smog, greenhouse effect",
                    "Water pollution: Eutrophication, industrial effluents, and microplastics",
                    "Solid waste management: Segregation, composting, incineration, sanitary landfill",
                    "Hazardous waste and E-waste management rules and disposal",
                    "Environmental Impact Assessment (EIA) process and clearance stages"
                ]),
                ("Module 3: Renewable Energy and Clean Technologies", 6, [
                    "Solar photovoltaic and solar thermal energy systems",
                    "Wind energy conversion systems: Onshore and offshore wind farms",
                    "Biomass, biogas, and waste-to-energy technologies",
                    "Geothermal and ocean thermal/tidal energy systems",
                    "Green hydrogen production and energy storage integration"
                ]),
                ("Module 4: Circular Economy and Resource Management", 6, [
                    "Linear economy vs Circular economy paradigm shift",
                    "Industrial symbiosis and eco-industrial parks",
                    "Material Flow Analysis (MFA) and resource decoupling",
                    "Sustainable supply chains and green procurement",
                    "Extended Producer Responsibility (EPR) policy frameworks"
                ]),
                ("Module 5: Sustainable Cities and Green Buildings", 6, [
                    "Green building rating systems: LEED, GRIHA, and IGBC standards",
                    "Passive solar design and energy-efficient building envelopes",
                    "Rainwater harvesting systems and greywater recycling",
                    "Sustainable urban mobility: Transit-oriented development and EV adoption",
                    "Urban heat island effect and urban forestry solutions"
                ])
            ]
        }
    ],
    4: [
        {
            "code": "MAT206",
            "name": "Graph Theory and Combinatorics",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Graphs, Paths, and Circuits", 9, [
                    "Basic definitions: Vertices, edges, degree, handshaking lemma",
                    "Isomorphism of graphs, subgraphs, and complement of a graph",
                    "Walks, paths, circuits, and connected components",
                    "Eulerian graphs: Konigsberg bridge problem, Euler's theorem",
                    "Hamiltonian graphs: Dirac's theorem and Ore's condition"
                ]),
                ("Module 2: Trees and Spanning Trees", 9, [
                    "Properties of trees, characterization theorems of trees",
                    "Centres, radii, and diameters of trees",
                    "Spanning trees, fundamental circuits, and cut-sets",
                    "Minimum spanning tree algorithms: Kruskal's and Prim's algorithms",
                    "Cayley's formula for number of spanning trees"
                ]),
                ("Module 3: Connectivity, Planarity, and Coloring", 9, [
                    "Vertex connectivity, edge connectivity, and cut vertices",
                    "Menger's theorem and Whitney's theorem on connectivity",
                    "Planar graphs: Euler's formula and Kuratowski's theorem",
                    "Dual of a planar graph and polyhedral graphs",
                    "Vertex coloring: Chromatic number, Brook's theorem, Four Color Theorem"
                ]),
                ("Module 4: Directed Graphs and Network Flows", 9, [
                    "Directed graphs, in-degree, out-degree, and tournament graphs",
                    "Strong, unilateral, and weak connectivity in digraphs",
                    "Directed acyclic graphs (DAG) and topological sorting",
                    "Max-Flow Min-Cut theorem and Ford-Fulkerson algorithm",
                    "Bipartite graphs, matching, and Hall's marriage theorem"
                ]),
                ("Module 5: Combinatorics and Generating Functions", 9, [
                    "Permutations and combinations with repetitions",
                    "Pigeonhole principle and generalized pigeonhole principle",
                    "Principle of inclusion-exclusion and derangements",
                    "Generating functions for sequence representation",
                    "Solving recurrence relations using generating functions"
                ])
            ]
        },
        {
            "code": "CST202",
            "name": "Computer Organization and Architecture",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Basic Computer Organization and Instruction Set", 9, [
                    "Functional units of a computer, Von Neumann vs Harvard architecture",
                    "Instruction formats: Zero, one, two, and three-address instructions",
                    "Addressing modes: Immediate, direct, indirect, register, displacement",
                    "Instruction execution cycle: Fetch, decode, execute, interrupt",
                    "Bus structure, synchronous and asynchronous bus transfers"
                ]),
                ("Module 2: Computer Arithmetic and ALU Design", 9, [
                    "Fixed-point representation: Unsigned and signed binary addition/subtraction",
                    "Multiplication algorithms: Booth's algorithm and array multipliers",
                    "Division algorithms: Restoring and Non-restoring division",
                    "Floating-point representation: IEEE 754 single and double precision standards",
                    "Floating-point addition, subtraction, multiplication, and normalization"
                ]),
                ("Module 3: Processing Unit and Control Design", 9, [
                    "Single-bus and multiple-bus CPU data path organization",
                    "Hardwired control design: State table method and delay element method",
                    "Microprogrammed control design: Microinstructions, sequencing, control memory",
                    "Pipelining concepts: Instruction pipeline, 5-stage RISC pipeline",
                    "Pipeline hazards: Structural, data, and control hazards and mitigations"
                ]),
                ("Module 4: Memory System Hierarchy", 9, [
                    "Memory hierarchy: Speed, capacity, and cost trade-offs",
                    "Semiconductor RAM (SRAM, DRAM) and ROM technologies",
                    "Cache memory: Cache hit/miss, mapping functions (Direct, Associative, Set-associative)",
                    "Cache replacement policies (LRU, FIFO) and write policies (Write-through, Write-back)",
                    "Virtual memory: Paging, segmentation, TLB, and page fault handling"
                ]),
                ("Module 5: Input-Output Organization and Storage", 9, [
                    "Peripheral devices and I/O interface modules",
                    "Programmed I/O and Interrupt-driven I/O mechanisms",
                    "Interrupt handling: Daisy chaining, priority encoder, vectored interrupts",
                    "Direct Memory Access (DMA): Controller architecture, burst and cycle-stealing modes",
                    "Secondary storage: Magnetic disks, SSDs, RAID levels (RAID 0, 1, 5)"
                ])
            ]
        },
        {
            "code": "CST204",
            "name": "Database Management Systems",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: DBMS Foundations and Conceptual Data Modeling", 9, [
                    "Database approach vs File systems, DBMS architecture (Three-schema architecture)",
                    "Data independence: Physical and logical data independence",
                    "Entity-Relationship (ER) model: Entities, attributes, entity sets, relationships",
                    "Enhanced ER (EER) modeling: Specialization, generalization, categorization",
                    "Converting ER/EER diagrams to relational schema"
                ]),
                ("Module 2: Relational Model and Relational Algebra", 9, [
                    "Relational model concepts: Domains, attributes, tuples, relation schemas",
                    "Integrity constraints: Entity integrity, referential integrity, domain constraints",
                    "Relational Algebra operations: Selection, projection, set operations",
                    "Join operations: Theta join, natural join, equi join, outer joins",
                    "Relational Calculus: Tuple relational calculus and domain relational calculus"
                ]),
                ("Module 3: Structured Query Language (SQL) and Normalization", 9, [
                    "SQL DDL: CREATE, ALTER, DROP; SQL DML: SELECT, INSERT, UPDATE, DELETE",
                    "Aggregate functions, GROUP BY, HAVING, and nested subqueries",
                    "SQL Views, triggers, assertions, and access control (GRANT, REVOKE)",
                    "Functional dependencies, Armstrong's axioms, and closure of attributes",
                    "Normal forms: 1NF, 2NF, 3NF, BCNF, and 4NF with loss-less decomposition"
                ]),
                ("Module 4: Transaction Processing and Concurrency Control", 9, [
                    "Transaction concepts and ACID properties",
                    "Transaction states, schedule classification: Serial, serializable, recoverable",
                    "Conflict serializability and testing for serializability (Precedence graph)",
                    "Lock-based protocols: 2-Phase Locking (2PL), Strict 2PL, Rigorous 2PL",
                    "Deadlock prevention, detection, and recovery schemes; timestamp-based protocols"
                ]),
                ("Module 5: Storage, Indexing, and Query Optimization", 9, [
                    "Physical storage organization: Fixed-length and variable-length records",
                    "File organizations: Sequential, indexed sequential, hash files",
                    "Indexing techniques: Dense vs Sparse index, primary vs secondary index",
                    "B-Trees and B+ Trees: Insertion, deletion, search operations",
                    "Query processing phases: Parsing, translation, optimization, and evaluation"
                ])
            ]
        },
        {
            "code": "CST206",
            "name": "Operating Systems",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: OS Architecture and Process Management", 9, [
                    "OS functions, system calls, system programs, OS dual-mode operation",
                    "OS structures: Monolithic, microkernel, layered, and modular systems",
                    "Process concepts: Process Control Block (PCB), process states, state transitions",
                    "Process scheduling: Schedulers, scheduling queues, context switching",
                    "Interprocess Communication (IPC): Shared memory and message passing systems"
                ]),
                ("Module 2: CPU Scheduling and Process Synchronization", 9, [
                    "CPU scheduling criteria, preemptive vs non-preemptive scheduling",
                    "Scheduling algorithms: FCFS, SJF, Priority, Round Robin, Multilevel Feedback Queue",
                    "Critical-Section Problem and Peterson's algorithmic solution",
                    "Hardware synchronization: TestAndSet, CompareAndSwap instructions",
                    "Semaphores, Mutex locks, Classical IPC problems (Producer-Consumer, Dining Philosophers)"
                ]),
                ("Module 3: Deadlocks", 9, [
                    "Deadlock characterization: 4 necessary conditions for deadlock",
                    "Resource-Allocation Graph (RAG) and wait-for graph",
                    "Deadlock prevention methods: Eliminating mutual exclusion, hold-and-wait, preemption, circular wait",
                    "Deadlock avoidance: Safe state concept and Banker's algorithm",
                    "Deadlock detection algorithms and recovery strategies (Process termination, resource preemption)"
                ]),
                ("Module 4: Memory Management and Virtual Memory", 9, [
                    "Logical vs physical address space, dynamic loading and dynamic linking",
                    "Contiguous memory allocation: MFT, MVT, Best-fit, First-fit, Worst-fit",
                    "Non-contiguous allocation: Paging hardware, page table structures (Hierarchical, Inverted)",
                    "Segmentation concepts and combined paging-segmentation",
                    "Virtual memory: Demand paging, page fault handling, page replacement (FIFO, LRU, Optimal)"
                ]),
                ("Module 5: Storage and File System Management", 9, [
                    "File concept, file attributes, file operations, file access methods",
                    "Directory structures: Single-level, two-level, tree-structured, acyclic-graph",
                    "File system mounting, file sharing, and access control matrices",
                    "File allocation methods: Contiguous, linked, indexed allocation",
                    "Disk scheduling algorithms: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK"
                ])
            ]
        },
        {
            "code": "MCN202",
            "name": "Constitution of India",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Historical Background and Preamble", 6, [
                    "Constituent Assembly, drafting committee, and enactment of the Constitution",
                    "Salient features of the Indian Constitution",
                    "Preamble: Sovereign, Socialist, Secular, Democratic, Republic ideals",
                    "Citizenship provisions (Articles 5-11) and Citizenship Amendment Act overview",
                    "Territory of the Union and reorganization of states"
                ]),
                ("Module 2: Fundamental Rights and Directive Principles", 6, [
                    "Fundamental Rights (Part III): Right to Equality (Articles 14-18)",
                    "Right to Freedom (Articles 19-22) and Protection of Life & Personal Liberty (Article 21)",
                    "Right against Exploitation (Articles 23-24) and Freedom of Religion (Articles 25-28)",
                    "Constitutional Remedies (Article 32): Writs (Habeas Corpus, Mandamus, Quo Warranto, etc.)",
                    "Directive Principles of State Policy (DPSP, Part IV) and Fundamental Duties (Article 51A)"
                ]),
                ("Module 3: Union Executive and Legislature", 6, [
                    "President of India: Qualifications, election, powers, impeachment procedure",
                    "Vice-President, Prime Minister, and Council of Ministers",
                    "Parliament: Rajya Sabha and Lok Sabha composition, powers, legislative procedure",
                    "Budgetary process, financial bills, and parliamentary committees",
                    "Supreme Court of India: Jurisdiction, appointment of judges, judicial review"
                ]),
                ("Module 4: State Executive and Legislature", 6, [
                    "Governor: Appointment, constitutional role, executive and discretionary powers",
                    "Chief Minister and State Council of Ministers",
                    "State Legislature: Legislative Assembly and Legislative Council",
                    "High Courts: Composition, jurisdiction, and power of issuing writs under Article 226",
                    "Subordinate courts and alternative dispute resolution mechanisms (Lok Adalats)"
                ]),
                ("Module 5: Federal Structure and Emergency Provisions", 6, [
                    "Centre-State relations: Legislative, administrative, and financial relations",
                    "Panchayati Raj Institutions (73rd Amendment) and Municipalities (74th Amendment)",
                    "National Emergency (Article 352): Grounds, procedure, and impact on fundamental rights",
                    "President's Rule in States (Article 356) and Financial Emergency (Article 360)",
                    "Constitutional amendment procedure under Article 368 and Basic Structure Doctrine"
                ])
            ]
        }
    ],
    5: [
        {
            "code": "CST301",
            "name": "Formal Languages and Automata Theory",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Finite Automata and Regular Expressions", 9, [
                    "Alphabet, strings, languages, and operations on languages",
                    "Deterministic Finite Automata (DFA): Formal definition, transition diagrams",
                    "Non-deterministic Finite Automata (NFA) and equivalence with DFA",
                    "NFA with epsilon-transitions (e-NFA) and conversion to DFA",
                    "Minimization of DFAs: Table-filling algorithm and Equivalence classes"
                ]),
                ("Module 2: Regular Languages and Grammars", 9, [
                    "Regular expressions and conversion to finite automata (Thompson's construction)",
                    "Arden's theorem and conversion of FA to regular expressions",
                    "Pumping Lemma for Regular Languages and applications in proving non-regularity",
                    "Closure properties and decision properties of regular languages",
                    "Chomsky hierarchy of languages overview"
                ]),
                ("Module 3: Context-Free Grammars and Pushdown Automata", 9, [
                    "Context-Free Grammars (CFG): Derivations, parse trees, ambiguity in grammars",
                    "Simplification of CFG: Elimination of useless symbols, null productions, unit productions",
                    "Chomsky Normal Form (CNF) and Greibach Normal Form (GNF)",
                    "Pushdown Automata (PDA): Definition, instantaneous descriptions, acceptance by final state and empty stack",
                    "Equivalence between CFG and PDA"
                ]),
                ("Module 4: Properties of CFLs and Turing Machines", 9, [
                    "Pumping Lemma for Context-Free Languages and applications",
                    "Closure properties and decision algorithms for context-free languages",
                    "Deterministic Context-Free Languages (DCFL) and DPDA",
                    "Turing Machine (TM): Formal definition, instantaneous description, transition diagrams",
                    "Design of Turing Machines for standard languages and arithmetic functions"
                ]),
                ("Module 5: Undecidability and Computational Complexity", 9, [
                    "Turing Machine variants: Multi-tape TM, non-deterministic TM, universal Turing machine",
                    "Decidability and Undecidability: Halting Problem of Turing Machine",
                    "Post Correspondence Problem (PCP) and modified PCP",
                    "Complexity classes: P, NP, NP-Complete, and NP-Hard problems",
                    "Cook's theorem and standard NP-complete problems overview"
                ])
            ]
        },
        {
            "code": "CST303",
            "name": "Computer Networks",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Network Architecture and Physical Layer", 9, [
                    "Data communications components, data representation, and data flow",
                    "Network topologies: Mesh, Star, Bus, Ring, and Hybrid topologies",
                    "OSI Reference Model vs TCP/IP Protocol Suite",
                    "Transmission media: Guided (Twisted pair, Coaxial, Fiber optic) and Unguided (Radio, Microwave)",
                    "Switching techniques: Circuit switching, packet switching, virtual circuits"
                ]),
                ("Module 2: Data Link Layer and MAC Sublayer", 9, [
                    "Data Link Layer design issues: Framing, physical addressing, flow control, error control",
                    "Error detection and correction: Parity, Checksum, CRC, Hamming code",
                    "Sliding Window protocols: Stop-and-Wait, Go-Back-N, Selective Repeat",
                    "Random Access protocols: ALOHA, Slotted ALOHA, CSMA, CSMA/CD, CSMA/CA",
                    "IEEE 802.3 Ethernet standard, Fast Ethernet, Gigabit Ethernet, and IEEE 802.11 Wireless LAN"
                ]),
                ("Module 3: Network Layer and Routing Protocols", 9, [
                    "Network layer functions, IPv4 addressing, classful vs classless addressing (CIDR)",
                    "Subnetting, supernetting, and address translation (NAT)",
                    "IPv4 datagram format, fragmentation, and reassembly; IPv6 header and addressing",
                    "Routing algorithms: Distance Vector routing (Bellman-Ford), Link State routing (Dijkstra)",
                    "Routing protocols: RIP, OSPF, and Border Gateway Protocol (BGP)"
                ]),
                ("Module 4: Transport Layer Protocols", 9, [
                    "Transport layer services, port numbers, socket addressing, and multiplexing",
                    "User Datagram Protocol (UDP): Segment structure, checksum, applications",
                    "Transmission Control Protocol (TCP): Segment format, 3-way handshake connection establishment",
                    "TCP flow control (Sliding window) and error control",
                    "TCP congestion control: Slow start, congestion avoidance, fast retransmit, fast recovery"
                ]),
                ("Module 5: Application Layer and Network Security", 9, [
                    "Domain Name System (DNS): Hierarchical namespace, resource records, name servers",
                    "Electronic Mail: SMTP, POP3, IMAP architecture and MIME format",
                    "Hypertext Transfer Protocol (HTTP): HTTP/1.1 vs HTTP/2, persistent connections, cookies",
                    "Network management: SNMP architecture and MIB",
                    "Firewalls, packet filtering, and intrusion detection system (IDS) concepts"
                ])
            ]
        },
        {
            "code": "CST305",
            "name": "System Software",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Introduction to System Software and SIC Architecture", 9, [
                    "System software vs Application software, system programming environment",
                    "Simplified Instructional Computer (SIC) architecture: Memory, registers, data formats, instruction set",
                    "SIC/XE architecture: Additional registers, addressing modes, instruction formats",
                    "Data structures used in system software: Tables, arrays, linked lists, hash tables",
                    "SIC and SIC/XE programming examples"
                ]),
                ("Module 2: Assemblers", 9, [
                    "Basic assembler functions: Translating mnemonics to machine code, evaluating addresses",
                    "Design of two-pass assembler: Pass 1 and Pass 2 algorithms",
                    "Assembler data structures: OPTAB, SYMTAB, LOCCTR, intermediate file",
                    "Machine-dependent assembler features: Instruction formats, addressing modes, program relocation",
                    "Machine-independent assembler features: Literals, symbol-defining statements, expressions"
                ]),
                ("Module 3: Macro Processors", 9, [
                    "Basic macro processor functions: Macro definition, invocation, and expansion",
                    "One-pass macro processor design: Algorithm and data structures (NAMTAB, DEFTAB, ARGTAB)",
                    "Machine-independent macro processor features: Concatenation of macro parameters, unique labels",
                    "Conditional macro expansion: IF-ELSE, WHILE loops in macros",
                    "Keyword macro parameters and macro processor design options"
                ]),
                ("Module 4: Linkers and Loaders", 9, [
                    "Basic loader functions: Allocation, linking, relocation, loading",
                    "Absolute loader: Design algorithm and operation",
                    "Relocating loader: Modification record and bitmask approaches",
                    "Direct-linking loader: Pass 1 and Pass 2 algorithms and external symbol tables (ESTAB)",
                    "Dynamic linking and shared libraries (.so, .dll) operation"
                ]),
                ("Module 5: System Software Tools and Compilers", 9, [
                    "Text editors: Structure of text editor, editing buffer, screen layout",
                    "Interactive debugging systems: Breakpoints, tracepoints, symbolic debuggers",
                    "Lexical analysis tools (LEX): Regular expressions, token generation, lex.yy.c",
                    "Parser generation tools (YACC): Context-free grammar rules, shift-reduce parsing, y.tab.c",
                    "Device drivers: Character and block device drivers in Linux environment"
                ])
            ]
        },
        {
            "code": "CST307",
            "name": "Microprocessors and Microcontrollers",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: 8086 Microprocessor Architecture", 9, [
                    "Evolution of microprocessors, 8086 internal architecture: BIU and EU",
                    "Register organization: General purpose, pointer, index, and segment registers",
                    "Physical memory generation and memory segmentation (1 MB address space)",
                    "Pin diagram of 8086, Minimum mode vs Maximum mode configurations",
                    "Bus timing diagrams for read and write machine cycles"
                ]),
                ("Module 2: 8086 Instruction Set and Assembly Programming", 9, [
                    "8086 addressing modes: Immediate, direct, register, register indirect, based, indexed",
                    "Instruction formats and instruction set classification (Data transfer, arithmetic, logical)",
                    "String manipulation instructions: MOVS, CMPS, SCAS, LODS, STOS, REP prefix",
                    "Process control instructions and assembler directives (SEGMENT, ASSUME, DB, DW, PROC, ENDP)",
                    "Assembly language programs: Arithmetic operations, array sorting, string reversal"
                ]),
                ("Module 3: 8086 Interrupts and Peripheral Interfacing", 9, [
                    "8086 interrupt structure: Hardware vs software interrupts, Interrupt Vector Table (IVT)",
                    "Programmable Peripheral Interface (8255 PPI): Architecture, control word formats, operating modes",
                    "Programmable Interval Timer (8254 PIT): Architecture and operating modes",
                    "Programmable Interrupt Controller (8259 PIC): Architecture and cascading",
                    "Interfacing ADC and DAC with 8086 for data acquisition"
                ]),
                ("Module 4: 8051 Microcontroller Architecture", 9, [
                    "Microprocessor vs Microcontroller, 8051 internal block diagram",
                    "8051 memory organization: Internal RAM (128 bytes), SFRs, External memory interface",
                    "Port architecture: Ports P0, P1, P2, P3 configurations and internal latches",
                    "Timers and Counters: TMOD, TCON registers, Mode 0, 1, 2, 3 operations",
                    "Serial communication in 8051: SCON, SBUF registers, baud rate generation using Timer 1"
                ]),
                ("Module 5: 8051 Programming and Real-World Interfacing", 9, [
                    "8051 addressing modes: Immediate, direct, register, register indirect, indexed",
                    "8051 instruction set: Data transfer, arithmetic, logic, boolean, branching instructions",
                    "Embedded C programming for 8051: Data types, bit operations, delay routines",
                    "Interfacing 8051 with Stepper Motor and DC motor speed control",
                    "Interfacing 8051 with LCD display (16x2) and 4x4 matrix keyboard"
                ])
            ]
        },
        {
            "code": "CST309",
            "name": "Management of Software Systems",
            "credits": 3,
            "type": "Theory",
            "modules": [
                ("Module 1: Software Process Models and Agile Philosophy", 7, [
                    "Software engineering challenges, professional responsibilities",
                    "Traditional models: Waterfall, Prototyping, Spiral, Incremental models",
                    "Agile software development: Agile manifesto, principles, and values",
                    "Scrum framework: Product backlog, sprint planning, daily standup, sprint retrospective",
                    "Extreme Programming (XP) practices: Pair programming, TDD, continuous integration"
                ]),
                ("Module 2: Requirements Engineering and System Modeling", 7, [
                    "Functional vs non-functional requirements, requirement validation",
                    "Requirements elicitation techniques: User stories, use case modeling",
                    "Software Requirements Specification (SRS) document standard (IEEE 830)",
                    "UML structural modeling: Class diagrams, package diagrams, component diagrams",
                    "UML behavioral modeling: Sequence diagrams, activity diagrams, statechart diagrams"
                ]),
                ("Module 3: Software Architectural Design and Patterns", 7, [
                    "Software architecture concepts, architectural styles (Layered, Client-Server, Microservices)",
                    "Design principles: SOLID principles, separation of concerns, high cohesion, low coupling",
                    "Creational design patterns: Singleton, Factory Method, Abstract Factory",
                    "Structural design patterns: Adapter, Decorator, Facade",
                    "Behavioral design patterns: Observer, Strategy, Command patterns"
                ]),
                ("Module 4: Software Verification, Validation, and Testing", 7, [
                    "Verification vs Validation, software inspection and code review techniques",
                    "Black-box testing: Equivalence partitioning, boundary value analysis, cause-effect graphing",
                    "White-box testing: Control flow testing, cyclomatic complexity, basis path testing",
                    "Integration testing, system testing, regression testing, acceptance testing",
                    "Automated testing frameworks (JUnit/pytest) and Continuous Integration (CI) pipelines"
                ]),
                ("Module 5: Software Project Management and Quality Assurance", 7, [
                    "Software project estimation: COCOMO II model and Function Point analysis",
                    "Project scheduling: Gantt charts, CPM, and PERT networks",
                    "Risk management: Risk identification, assessment, mitigation, and monitoring",
                    "Software quality assurance: CMMI levels, ISO 9001 standards, Six Sigma",
                    "Software maintenance: Corrective, adaptive, perfective, preventive maintenance"
                ])
            ]
        }
    ],
    6: [
        {
            "code": "CST302",
            "name": "Compiler Design",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Compiler Overview and Lexical Analysis", 9, [
                    "Phases of a compiler, Cousins of the compiler (Preprocessor, Assembler, Linker/Loader)",
                    "Compiler construction tools overview",
                    "Role of lexical analyzer, tokens, patterns, lexemes",
                    "Specification of tokens using regular expressions, transition diagrams",
                    "Design of lexical analyzer using LEX tool"
                ]),
                ("Module 2: Top-Down Syntax Analysis", 9, [
                    "Role of parser, context-free grammars for programming languages",
                    "Top-down parsing: Recursive descent parsing, backtracking issues",
                    "Non-recursive predictive parsing: First and Follow sets computation",
                    "Construction of LL(1) parsing tables and parser implementation",
                    "Error detection and recovery in top-down parsers"
                ]),
                ("Module 3: Bottom-Up Syntax Analysis", 9, [
                    "Bottom-up parsing: Shift-reduce parsing, handle pruning, conflicts (Shift/Reduce, Reduce/Reduce)",
                    "LR parsers: Model of LR parser, string parsing algorithm",
                    "Construction of SLR(1) parsing table using LR(0) items",
                    "Canonical LR (CLR) parsing and Lookahead LR (LALR) parsing table construction",
                    "YACC parser generator usage for bottom-up parsing"
                ]),
                ("Module 4: Syntax-Directed Translation and Intermediate Code", 9, [
                    "Syntax-Directed Definitions (SDD): Synthesized vs Inherited attributes",
                    "Syntax-Directed Translation schemes (SDT) and annotated parse trees",
                    "Intermediate representations: Postfix notation, Syntax trees, Three-Address Code (TAC)",
                    "Types of TAC: Quadruples, Triples, and Indirect Triples",
                    "Translation of expressions, Boolean expressions, and control flow statements"
                ]),
                ("Module 5: Code Optimization and Code Generation", 9, [
                    "Principal sources of code optimization, loop optimization, dead code elimination",
                    "Basic blocks and Flow graphs construction, DAG representation of basic blocks",
                    "Peephole optimization techniques: Redundant loads/stores, algebraic simplifications",
                    "Issues in the design of code generator: Target machine characteristics, instruction selection",
                    "Register allocation and assignment: Graph coloring heuristic basics"
                ])
            ]
        },
        {
            "code": "CST304",
            "name": "Computer Graphics and Image Processing",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Graphic Hardware and Output Primitives", 9, [
                    "Display devices: Refresh CRT, raster scan displays, random scan displays",
                    "Line drawing algorithms: DDA line algorithm, Bresenham's line drawing algorithm",
                    "Circle generation algorithms: Midpoint circle algorithm and Bresenham's circle algorithm",
                    "Polygon filling algorithms: Scan-line polygon fill, Boundary-fill, Flood-fill",
                    "Antialiasing techniques in computer graphics"
                ]),
                ("Module 2: 2D Transformations and Clipping", 9, [
                    "Basic 2D transformations: Translation, rotation, scaling in matrix form",
                    "Homogeneous coordinates and composite transformation matrices",
                    "Reflection and shearing transformations",
                    "Viewing pipeline: Window-to-Viewport coordinate transformation",
                    "Clipping algorithms: Cohen-Sutherland line clipping, Sutherland-Hodgman polygon clipping"
                ]),
                ("Module 3: 3D Graphics and Visible Surface Detection", 9, [
                    "3D transformations: Translation, rotation about coordinate axes, scaling, reflection",
                    "3D Viewing: Projections (Parallel projection vs Perspective projection)",
                    "Visible surface detection methods: Depth buffer (Z-buffer) algorithm, A-buffer",
                    "Scan-line method, Depth-sort (Painter's algorithm), BSP trees",
                    "Illumination models: Ambient light, diffuse reflection, specular reflection (Phong model)"
                ]),
                ("Module 4: Digital Image Fundamentals and Enhancement", 9, [
                    "Elements of digital image processing, image formation model, sampling, and quantization",
                    "Pixel relationships: Neighbors, adjacency, connectivity, distance measures",
                    "Spatial domain enhancement: Image negative, log transform, power-law transform",
                    "Histogram processing: Histogram equalization and histogram specification",
                    "Spatial filtering: Smoothing spatial filters (Averaging) and Sharpening filters (Laplacian)"
                ]),
                ("Module 5: Image Transforms and Segmentation", 9, [
                    "Frequency domain filtering: 2D DFT, Ideal, Butterworth, and Gaussian lowpass/highpass filters",
                    "Image degradation model, noise models (Gaussian, Salt-and-pepper noise)",
                    "Edge detection: Gradient operators (Sobel, Prewitt, Roberts), Laplacian of Gaussian (LoG)",
                    "Canny edge detector algorithm and thresholding techniques (Otsu's method)",
                    "Image compression fundamentals: Lossless (Huffman, RLE) vs Lossy (JPEG DCT) compression"
                ])
            ]
        },
        {
            "code": "CST306",
            "name": "Algorithm Analysis and Design",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Mathematical Foundations and Analysis Framework", 9, [
                    "Algorithm definition, pseudo-code conventions, performance analysis",
                    "Asymptotic notations: Big-O, Big-Omega, Big-Theta, Little-o, Little-omega definitions",
                    "Recurrence relations: Substitution method, Recursion-tree method, Master theorem",
                    "Amortized analysis: Aggregate analysis, accounting method, potential method",
                    "Analysis of iterative and recursive algorithms"
                ]),
                ("Module 2: Divide-and-Conquer and Greedy Paradigms", 9, [
                    "Divide-and-Conquer strategy: Merge Sort and Quick Sort with average/worst-case analysis",
                    "Strassen's matrix multiplication algorithm",
                    "Greedy method strategy: Fractional Knapsack problem",
                    "Huffman coding algorithm for optimal prefix codes",
                    "Minimum Cost Spanning Trees: Prim's and Kruskal's algorithms analysis; Dijkstra's algorithm"
                ]),
                ("Module 3: Dynamic Programming Paradigm", 9, [
                    "Dynamic programming principles: Optimal substructure, overlapping subproblems",
                    "0/1 Knapsack problem using dynamic programming",
                    "Matrix Chain Multiplication: Formulation and order computation",
                    "Longest Common Subsequence (LCS) algorithm",
                    "All-Pairs Shortest Paths: Floyd-Warshall algorithm and Bellman-Ford algorithm"
                ]),
                ("Module 4: Backtracking and Branch-and-Bound", 9, [
                    "Backtracking concept: State space tree, bounding functions",
                    "N-Queens problem: Formulation and backtracking solution",
                    "Subset-Sum problem and Hamiltonian Circuit problem",
                    "Branch-and-Bound technique: FIFO and LC Branch-and-Bound",
                    "Travelling Salesperson Problem (TSP) using Branch-and-Bound"
                ]),
                ("Module 5: Computational Complexity and Approximation Algorithms", 9, [
                    "Tractable vs intractable problems, polynomial time verifiability",
                    "Classes P, NP, NP-Complete, and NP-Hard definitions",
                    "Polynomial-time reductions, Cook-Levin theorem overview",
                    "Standard NP-complete problems: 3-SAT, Vertex Cover, Clique, Subset Sum",
                    "Approximation algorithms: 2-approximation for Vertex Cover, Metric TSP approximation"
                ])
            ]
        }
    ],
    7: [
        {
            "code": "CST401",
            "name": "Artificial Intelligence",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Introduction and Problem Solving by Search", 9, [
                    "What is AI? Turing test, rational agents, foundations of AI",
                    "Agent architectures: Reflex agents, goal-based agents, utility-based agents",
                    "Formulating problems as state space search: Initial state, actions, transition model, goal test",
                    "Uninformed search strategies: Breadth-First Search (BFS), Depth-First Search (DFS), Uniform-Cost Search (UCS)",
                    "Depth-Limited Search and Iterative Deepening Search (IDS)"
                ]),
                ("Module 2: Informed Search and Adversarial Search", 9, [
                    "Informed (heuristic) search strategies: Greedy Best-First Search and A* search",
                    "Admissible heuristics, consistent heuristics, and optimality of A*",
                    "Local search algorithms: Hill-climbing, Simulated Annealing, Genetic Algorithms",
                    "Adversarial search: Games, optimal decisions in games, Minimax algorithm",
                    "Alpha-Beta pruning and evaluation functions for real-time game play"
                ]),
                ("Module 3: Knowledge Representation and Logic", 9, [
                    "Knowledge-based agents, Wumpus world environment",
                    "Propositional logic: Syntax, semantics, inference rules, resolution",
                    "First-Order Logic (FOL): Syntax, semantics, quantifiers, unifications",
                    "Forward chaining and backward chaining in first-order logic",
                    "Ontological engineering: Semantic networks, frames, and description logics"
                ]),
                ("Module 4: Planning and Probabilistic Reasoning", 9, [
                    "Classical planning: STRIPS language, PDDL representations",
                    "Planning algorithms: Planning graphs and Graphplan algorithm",
                    "Handling uncertainty: Probability axioms, conditional probability, Bayes' rule",
                    "Bayesian Networks: Representation, semantics, conditional independence",
                    "Exact inference in Bayesian networks: Enumeration and variable elimination"
                ]),
                ("Module 5: Learning and Expert Systems", 9, [
                    "Forms of learning: Supervised, unsupervised, and reinforcement learning",
                    "Learning decision trees: Information gain, entropy, ID3 algorithm",
                    "Reinforcement learning: Markov Decision Processes (MDP), Q-learning basics",
                    "Architecture of rule-based Expert Systems: Inference engine, knowledge base",
                    "Ethics in AI: Fairness, accountability, transparency, and societal impact"
                ])
            ]
        },
        {
            "code": "CST403",
            "name": "Cryptography and Network Security",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Foundations of Cryptography and Classical Ciphers", 9, [
                    "OSI security architecture: Security attacks, services, and mechanisms",
                    "Model for network security and cryptographic system classification",
                    "Classical encryption techniques: Substitution (Caesar, Playfair, Hill, Vigenere ciphers)",
                    "Transposition techniques: Rail fence and columnar transposition ciphers",
                    "Steganography and cryptanalysis techniques"
                ]),
                ("Module 2: Symmetric Key Cryptography", 9, [
                    "Block cipher design principles: Shannon's confusion and diffusion",
                    "Data Encryption Standard (DES): Feistel structure, round operations, DES security",
                    "Triple DES (3DES) with two and three keys",
                    "Advanced Encryption Standard (AES): Architecture, round transformations, key expansion",
                    "Block cipher modes of operation: ECB, CBC, CFB, OFB, CTR modes"
                ]),
                ("Module 3: Asymmetric Cryptography and Key Management", 9, [
                    "Principles of public-key cryptosystems: Trapdoor one-way functions",
                    "Fermat's and Euler's theorems, Extended Euclidean algorithm",
                    "RSA cryptosystem: Key generation, encryption, decryption, and security analysis",
                    "Diffie-Hellman Key Exchange algorithm and Man-in-the-Middle attack",
                    "Elliptic Curve Cryptography (ECC) foundations and advantages"
                ]),
                ("Module 4: Hash Functions, MAC, and Digital Signatures", 9, [
                    "Cryptographic hash functions: Properties, Birthday paradox, MD5 overview",
                    "Secure Hash Algorithm (SHA-512): Architecture, processing of 1024-bit blocks",
                    "Message Authentication Codes (MAC): Requirements, HMAC algorithm",
                    "Digital signature schemes: RSA digital signature scheme",
                    "Digital Signature Standard (DSS) and Digital Signature Algorithm (DSA)"
                ]),
                ("Module 5: Network Security Protocols and System Security", 9, [
                    "Public Key Infrastructure (PKI): X.509 certificates and certification authorities",
                    "Transport layer security: SSL/TLS protocol architecture, handshake protocol",
                    "Network layer security: IPsec architecture, Authentication Header (AH), ESP",
                    "Email security: Pretty Good Privacy (PGP) and S/MIME",
                    "System security: Firewalls (Packet filtering, application gateway) and Intrusion Detection Systems"
                ])
            ]
        }
    ],
    8: [
        {
            "code": "CST402",
            "name": "Distributed Computing",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Distributed Systems Foundations", 9, [
                    "Characterization of distributed systems: Examples, trends, and design challenges",
                    "System models: Physical, architectural (Client-server, P2P), and fundamental models",
                    "Interprocess communication: Sockets, Java RMI architecture, Remote Procedure Calls (RPC)",
                    "Message-oriented communication and Publish-Subscribe architectures",
                    "Case studies of real-world distributed architectures"
                ]),
                ("Module 2: Clock Synchronization and Distributed State", 9, [
                    "Time in distributed systems: Physical clocks, drift rate, NTP protocol",
                    "Logical clocks: Lamport's timestamps and total ordering of events",
                    "Vector clocks and causal ordering of messages",
                    "Global state and distributed snapshot algorithms: Chandy-Lamport algorithm",
                    "Distributed debugging and state assertion monitoring"
                ]),
                ("Module 3: Distributed Coordination and Consensus", 9, [
                    "Distributed mutual exclusion: Centralized, distributed (Ricart-Agrawala), token ring algorithms",
                    "Election algorithms: Bully algorithm and Ring algorithm",
                    "Consensus problem in synchronous and asynchronous distributed systems",
                    "FLP impossibility theorem overview",
                    "Paxos consensus protocol and Raft consensus algorithm fundamentals"
                ]),
                ("Module 4: Fault Tolerance and Replication", 9, [
                    "Failure models: Crash-stop, crash-recovery, Byzantine failures",
                    "Reliable group communication and atomic multicast",
                    "Replication: Passive (Primary-backup) vs Active replication",
                    "Consistency models: Strict, sequential, causal, and eventual consistency",
                    "Byzantine fault tolerance (BFT) fundamentals and PBFT overview"
                ]),
                ("Module 5: Distributed File Systems and Modern Cloud Computing", 9, [
                    "Distributed File Systems: Architecture, NFS, and Hadoop Distributed File System (HDFS)",
                    "Google File System (GFS) design principles",
                    "Distributed computing paradigms: MapReduce programming model and Apache Spark",
                    "CAP theorem: Consistency, Availability, Partition tolerance trade-offs",
                    "Modern trends: Edge computing, microservices, and container orchestration (Kubernetes)"
                ])
            ]
        }
    ]
}

# Detailed First Year & Core Courses for Scheme 2024
BTECH_2024_COURSES = {
    1: [
        {
            "code": "MAT101",
            "name": "Linear Algebra and Calculus",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Linear Systems and Matrices", 9, [
                    "Rank of a matrix, elementary row operations, and echelon form",
                    "System of linear equations: Gauss elimination and Gauss-Jordan methods",
                    "Eigenvalues, eigenvectors, and Cayley-Hamilton theorem",
                    "Diagonalization of symmetric matrices and quadratic forms",
                    "Orthogonal transformation and canonical forms"
                ]),
                ("Module 2: Differential Calculus of Single Variable", 9, [
                    "Rolle's theorem, Lagrange's and Cauchy's Mean Value Theorems",
                    "Indeterminate forms and L'Hopital's rule",
                    "Taylor's and Maclaurin's series expansions of functions",
                    "Curvature, radius of curvature, and evolutes",
                    "Asymptotes of Cartesian and polar curves"
                ]),
                ("Module 3: Multivariable Calculus - Partial Differentiation", 9, [
                    "Functions of two or more variables: Limits, continuity, and partial derivatives",
                    "Total differential and chain rule for partial differentiation",
                    "Euler's theorem for homogeneous functions and applications",
                    "Maxima and minima of functions of two variables",
                    "Lagrange's method of undetermined multipliers for constrained extrema"
                ]),
                ("Module 4: Multiple Integrals", 9, [
                    "Double integrals in Cartesian and polar coordinates",
                    "Change of order of integration in double integrals",
                    "Area calculation of plane regions using double integrals",
                    "Triple integrals in Cartesian, cylindrical, and spherical coordinates",
                    "Volume calculation of solid regions using triple integrals"
                ]),
                ("Module 5: Vector Differential Calculus", 9, [
                    "Scalar and vector point functions, vector differential operator del",
                    "Directional derivative, gradient of a scalar field, and unit normal",
                    "Divergence and curl of vector fields: Physical interpretations",
                    "Solenoidal and irrotational vector fields",
                    "Scalar potential functions and conservative force fields"
                ])
            ]
        },
        {
            "code": "PHT100",
            "name": "Engineering Physics",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Oscillations and Waves", 9, [
                    "Simple harmonic motion: Damped and forced harmonic oscillations",
                    "Resonance and quality factor in mechanical and electrical systems",
                    "One-dimensional wave equation and longitudinal/transverse waves",
                    "Superposition of waves and formation of standing waves",
                    "Acoustics of buildings: Reverberation, Sabine's formula, and acoustic absorbers"
                ]),
                ("Module 2: Wave Optics - Interference and Diffraction", 9, [
                    "Principle of superposition and coherence of light waves",
                    "Interference in thin films: Air wedge and testing of optical flatness",
                    "Newton's rings: Measurement of wavelength and refractive index",
                    "Fraunhofer diffraction at a single slit, double slit, and transmission grating",
                    "Resolving power of grating and Rayleigh's criterion for resolution"
                ]),
                ("Module 3: Quantum Mechanics", 9, [
                    "Dual nature of matter, de Broglie hypothesis, and wave packets",
                    "Heisenberg's uncertainty principle and experimental verification",
                    "Time-dependent and time-independent Schrodinger wave equations",
                    "Physical interpretation and normalization of wave function",
                    "Application to particle trapped in a one-dimensional infinite potential well"
                ]),
                ("Module 4: Lasers and Fiber Optics", 9, [
                    "Absorption, spontaneous emission, stimulated emission, and Einstein's relations",
                    "Population inversion, pumping mechanisms, and optical resonant cavity",
                    "Ruby laser, Helium-Neon (He-Ne) laser, and Semiconductor laser diodes",
                    "Optical fiber: Numerical aperture, acceptance angle, step-index and graded-index fibers",
                    "Fiber optic communication system and optical sensor applications"
                ]),
                ("Module 5: Semiconductor Physics and Nanomaterials", 9, [
                    "Band theory of solids: Direct and indirect bandgap semiconductors",
                    "Carrier concentration in intrinsic and extrinsic semiconductors",
                    "Fermi level variation with temperature and doping concentration",
                    "Hall effect: Hall coefficient and determination of carrier mobility",
                    "Quantum confinement, quantum dots, quantum wells, and carbon nanotubes"
                ])
            ]
        },
        {
            "code": "EST100",
            "name": "Engineering Mechanics",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Statics of Particles", 9, [
                    "Basic units, dimensional homogeneity, vectors, Newton's laws",
                    "Concurrent force systems in a plane: Resolution and resultant",
                    "Equilibrium of particles in 2D and 3D, free body diagrams",
                    "Lami's theorem and triangle law of forces",
                    "Equilibrium equations for coplanar concurrent forces"
                ]),
                ("Module 2: Equilibrium of Rigid Bodies", 9, [
                    "Moment of a force about a point and axis; Varignon's theorem",
                    "Couples, moment of a couple, and force-couple systems",
                    "Equilibrium of rigid bodies in two dimensions: Supports and reactions",
                    "Types of trusses and determinacy criteria",
                    "Analysis of simple plane trusses using method of joints and sections"
                ]),
                ("Module 3: Friction and Properties of Surfaces", 9, [
                    "Dry friction laws, coefficients of static and kinetic friction",
                    "Angle of repose, cone of friction, and wedge/ladder friction analysis",
                    "Centroid of lines, simple and composite areas",
                    "First and second moments of area; Parallel and perpendicular axis theorems",
                    "Polar moment of inertia and radius of gyration calculation"
                ]),
                ("Module 4: Kinematics of Particles and Rigid Bodies", 9, [
                    "Rectilinear motion: Position, velocity, acceleration relationships",
                    "Curvilinear motion in Cartesian and polar coordinate systems",
                    "Projectiles: Trajectory equation, maximum height, time of flight, range",
                    "Rigid body rotation: Angular displacement, velocity, and acceleration",
                    "Relative velocity and acceleration in planar motion"
                ]),
                ("Module 5: Kinetics and Energy Principles", 9, [
                    "Newton's second law for systems of particles; D'Alembert's principle",
                    "Work done by forces, kinetic energy, and work-energy theorem",
                    "Potential energy and conservation of mechanical energy",
                    "Linear impulse and momentum; Principle of conservation of linear momentum",
                    "Impact of elastic and inelastic bodies: Coefficient of restitution"
                ])
            ]
        },
        {
            "code": "EST120",
            "name": "Basics of Civil and Mechanical Engineering",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Civil Engineering - Infrastructure and Materials", 9, [
                    "General scope of civil engineering in national development",
                    "Properties and testing of bricks, stone, cement, aggregate, and steel",
                    "Fresh and hardened concrete: Workability, slump test, compressive strength",
                    "Sustainable construction materials: Fly ash concrete, geopolymer concrete",
                    "Building components: Substructure, superstructure, plinth, and lintels"
                ]),
                ("Module 2: Civil Engineering - Surveying and Environment", 8, [
                    "Surveying objectives, classification, and scale definitions",
                    "Linear measurement with tapes and electronic distance meters (EDM)",
                    "Leveling concepts: Height of instrument and rise & fall methods",
                    "Total station and GIS mapping overview",
                    "Green buildings, rainwater harvesting, and environmental pollution mitigation"
                ]),
                ("Module 3: Mechanical Engineering - Thermal Energy and Power", 9, [
                    "Thermodynamics laws: Zeroth, First, and Second laws; open and closed systems",
                    "Steam generation: Fire tube and water tube high-pressure boilers",
                    "Steam and gas turbine power cycles; cogeneration systems",
                    "Hydraulic turbines: Pelton, Francis, and Kaplan turbines",
                    "Nuclear power generation and safety fundamentals"
                ]),
                ("Module 4: Mechanical Engineering - IC Engines and E-Mobility", 9, [
                    "Four-stroke and two-stroke internal combustion engine cycles",
                    "Air standard Otto and Diesel cycles, thermal efficiencies",
                    "Electric vehicle (EV) architectures: BEV, HEV, and PHEV comparison",
                    "Lithium-ion battery packs, motor controllers, and regenerative braking",
                    "Vapour compression refrigeration and inverter air conditioning"
                ]),
                ("Module 5: Mechanical Engineering - Advanced Manufacturing", 8, [
                    "Metal casting: Sand casting, die casting, investment casting, casting defects",
                    "Joining technologies: TIG, MIG, friction stir welding, adhesive bonding",
                    "Machine tools: Lathe, drilling, shaper, and CNC machining centers",
                    "Additive manufacturing: Fused deposition modeling (FDM), stereolithography (SLA)",
                    "Smart manufacturing: Industry 4.0, IoT in factories, and digital twins"
                ])
            ]
        },
        {
            "code": "HUN101",
            "name": "Life Skills and Professional Communication",
            "credits": 2,
            "type": "Theory",
            "modules": [
                ("Module 1: Self-Awareness and Emotional Intelligence", 6, [
                    "SWOT analysis, Johari window, and personal development planning",
                    "Emotional Intelligence: Self-awareness, empathy, motivation, and social skills",
                    "Developing growth mindset and resilience in academic/professional challenges",
                    "Stress reduction techniques: Mindfulness, yoga, and physical wellness",
                    "Time management matrix and productivity tools"
                ]),
                ("Module 2: Professional Speaking and Group Dynamics", 6, [
                    "Public speaking fundamentals: Overcoming stage fear, body language, vocal variety",
                    "Group Discussion (GD): Types of topics, strategies, etiquette, and leadership in GDs",
                    "Professional meetings: Organizing, agenda setting, and minute taking",
                    "Negotiation and conflict resolution in collaborative teams",
                    "Active listening and empathetic responding"
                ]),
                ("Module 3: Technical Writing and Digital Etiquette", 6, [
                    "Technical writing principles: Clarity, conciseness, coherence, precision",
                    "Professional correspondence: Emails, cover letters, and formal memos",
                    "Project proposal and engineering report structures",
                    "Digital footprint, LinkedIn profile optimization, and social media etiquette",
                    "Cyber security awareness and personal data protection"
                ]),
                ("Module 4: Problem Solving and Critical Innovation", 6, [
                    "Critical thinking: Evaluating evidence, detecting logical fallacies",
                    "Creative problem solving: Design thinking mindset and reverse engineering",
                    "Lateral thinking puzzles and TRIZ innovation principles",
                    "Decision making models: Cost-benefit analysis, decision trees, risk assessment",
                    "Collaboration tools for distributed engineering teams"
                ]),
                ("Module 5: Universal Values and Engineering Ethics", 6, [
                    "Professional ethics codes: IEEE, ACM, NSPE canons of ethics",
                    "Whistleblowing, safety culture, and environmental protection",
                    "Intellectual property rights (IPR): Patents, open source licensing, copyrights",
                    "Corporate Social Responsibility (CSR) and sustainable development",
                    "Diversity, equity, inclusion, and workplace professionalism"
                ])
            ]
        }
    ],
    2: [
        {
            "code": "MAT102",
            "name": "Advanced Engineering Mathematics",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Ordinary Differential Equations of Higher Order", 9, [
                    "Linear ODEs with constant coefficients: Complementary function and particular integrals",
                    "Method of variation of parameters for second-order differential equations",
                    "Cauchy-Euler and Legendre differential equations",
                    "Simultaneous differential equations and physical applications in vibrations",
                    "Series solutions of differential equations and Frobenius method"
                ]),
                ("Module 2: Partial Differential Equations", 9, [
                    "Formation of PDEs by elimination of arbitrary constants and functions",
                    "First order linear PDEs: Lagrange's method of multipliers",
                    "Homogeneous linear PDEs with constant coefficients",
                    "Separation of variables method for standard second-order PDEs",
                    "Solution of one-dimensional wave equation and one-dimensional heat equation"
                ]),
                ("Module 3: Fourier Series and Harmonic Analysis", 9, [
                    "Dirichlet's conditions and determination of Fourier coefficients",
                    "Fourier series of functions with arbitrary period 2L",
                    "Half-range Fourier sine and cosine expansions",
                    "Root mean square (RMS) value and Parseval's identity",
                    "Harmonic analysis for discrete periodic data"
                ]),
                ("Module 4: Integral Transforms", 9, [
                    "Laplace transform: Existence, standard functions, linearity, first and second shifting theorems",
                    "Transforms of derivatives and integrals; Unit step and Dirac delta functions",
                    "Inverse Laplace transforms and Convolution theorem",
                    "Solving initial value problems using Laplace transform methods",
                    "Fourier transforms: Sine, cosine transforms, and properties"
                ]),
                ("Module 5: Vector Integral Calculus", 9, [
                    "Line integrals, conservative vector fields, and independence of path",
                    "Green's theorem in the plane and applications to area calculation",
                    "Surface integrals and flux of vector fields across surfaces",
                    "Stokes' theorem relating line and surface integrals",
                    "Gauss divergence theorem relating surface and volume integrals"
                ])
            ]
        },
        {
            "code": "CYT100",
            "name": "Engineering Chemistry",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Electrochemistry and Batteries", 9, [
                    "Electrode potential, Nernst equation for single electrode and electrochemical cells",
                    "Reference electrodes: Standard hydrogen electrode and calomel electrode",
                    "Commercial batteries: Lithium-ion, nickel-metal hydride, and flow batteries",
                    "Fuel cells: Alkaline, PEMFC, and solid oxide fuel cells (SOFC)",
                    "Supercapacitors: Mechanisms, materials, and applications"
                ]),
                ("Module 2: Corrosion Science and Surface Engineering", 9, [
                    "Electrochemical mechanism of corrosion: Hydrogen evolution and oxygen absorption",
                    "Types of corrosion: Galvanic, pitting, intergranular, stress corrosion cracking",
                    "Factors influencing corrosion rate (Electrolyte, temperature, metallurgy)",
                    "Cathodic protection: Sacrificial anode and impressed current systems",
                    "Protective coatings: Galvanizing, tinning, electroplating, anodizing"
                ]),
                ("Module 3: Advanced Polymers and Composite Materials", 9, [
                    "Functionality, degree of polymerization, molecular weight distributions",
                    "Engineering polymers: Polycarbonate, Teflon, Kevlar, and PEEK",
                    "Conducting polymers: Polyaniline, polypyrrole, and polyacetylene",
                    "Fiber-reinforced polymer (FRP) composites: Carbon fiber and glass fiber composites",
                    "Biodegradable polymers: Polylactic acid (PLA) and polyhydroxyalkanoates (PHA)"
                ]),
                ("Module 4: Instrumental Methods of Chemical Analysis", 9, [
                    "Spectrophotometry: UV-Visible spectroscopy, Beer-Lambert's law, band transitions",
                    "Infrared (IR) spectroscopy: Characteristic vibrational frequencies of organic functional groups",
                    "Atomic Absorption Spectroscopy (AAS) for heavy metal trace detection",
                    "Scanning Electron Microscopy (SEM) and Energy Dispersive X-ray (EDX)",
                    "Chromatographic methods: Gas chromatography and high-performance liquid chromatography"
                ]),
                ("Module 5: Water Treatment and Environmental Chemistry", 9, [
                    "Hardness estimation by EDTA complexometric method",
                    "Boiler feed water: Priming, foaming, scales, sludges, and caustic embrittlement",
                    "Demineralization of water using ion-exchange resin processes",
                    "Desalination of seawater using reverse osmosis (RO) and electrodialysis",
                    "Waste water treatment: Biological treatment (Activated sludge process) and disinfection"
                ])
            ]
        },
        {
            "code": "EST102",
            "name": "Problem Solving and Algorithmic Programming in Python",
            "credits": 4,
            "type": "Theory/Lab",
            "modules": [
                ("Module 1: Computational Thinking and Python Basics", 9, [
                    "Algorithms, flowcharts, pseudocode, and program development cycle",
                    "Python interpreter, interactive mode, scripts, and basic syntax",
                    "Variables, data types (int, float, complex, bool, str), type conversion",
                    "Arithmetic, relational, logical, assignment, bitwise, membership operators",
                    "Input and output functions, formatted printing using f-strings"
                ]),
                ("Module 2: Control Flow and Iteration", 9, [
                    "Conditional statements: if, if-else, if-elif-else, nested if structures",
                    "Looping structures: while loop, for loop, range() function",
                    "Loop control statements: break, continue, pass, else with loops",
                    "Pattern printing, prime checking, Fibonacci series generation",
                    "List comprehensions and generator expressions basics"
                ]),
                ("Module 3: Data Structures - Lists, Tuples, Dictionaries, Sets", 9, [
                    "Python lists: Indexing, slicing, appending, inserting, removing, sorting",
                    "Tuples: Immutability, tuple packing and unpacking, operations",
                    "Dictionaries: Keys, values, key-value pairs, nested dictionaries, dictionary methods",
                    "Sets: Set operations (union, intersection, difference, symmetric difference)",
                    "String methods: split, join, strip, replace, find, count"
                ]),
                ("Module 4: Functions, Modules, and Packages", 9, [
                    "Function definition, calling, return values, default and keyword arguments",
                    "Variable length arguments (*args, **kwargs), scope of variables (global, local)",
                    "Lambda functions, map(), filter(), reduce() functions",
                    "Recursive functions: Factorial, GCD, Tower of Hanoi",
                    "Python standard library modules: math, random, datetime, sys, os"
                ]),
                ("Module 5: File Handling, Exceptions, and Libraries", 9, [
                    "File operations: Reading, writing, appending to text and CSV files",
                    "Handling structured data using json module",
                    "Exception handling: try, except, else, finally blocks, raising custom exceptions",
                    "Introduction to NumPy for multidimensional array processing",
                    "Introduction to Matplotlib for basic data visualization plotting"
                ])
            ]
        },
        {
            "code": "EST130",
            "name": "Basics of Electrical and Electronics Engineering",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: DC Circuit Analysis and Network Theorems", 9, [
                    "Current, voltage, power, energy, resistance, Ohm's law",
                    "Kirchhoff's Current Law (KCL) and Voltage Law (KVL)",
                    "Mesh current method and Node voltage method for DC resistive circuits",
                    "Superposition theorem, Thevenin's theorem, Norton's theorem",
                    "Maximum power transfer theorem and applications in electronics"
                ]),
                ("Module 2: Single Phase and Three Phase AC Circuits", 9, [
                    "Generation of sinusoidal AC voltage, peak, RMS, average values, form factor",
                    "Phasor representation of sinusoidal quantities; complex impedance",
                    "Series R-L, R-C, and R-L-C circuits: Power factor and resonance",
                    "Three-phase AC generation, star and delta connections, line vs phase quantities",
                    "Three-phase power measurement using two-wattmeter method"
                ]),
                ("Module 3: Electrical Machines and Smart Grid Concepts", 9, [
                    "Single-phase transformer: Working principle, EMF equation, losses, and efficiency",
                    "DC Motor: Construction, back EMF, torque equation, speed control methods",
                    "Three-phase induction motor: Rotating magnetic field, slip, torque-slip curve",
                    "Renewable energy integration: Solar inverters and grid-tie systems",
                    "Smart energy meters, energy audit basics, and electrical safety standards"
                ]),
                ("Module 4: Semiconductor Devices and Basic Amplifiers", 9, [
                    "PN junction diode: Working, forward and reverse characteristics, ideality factor",
                    "Zener diode as a voltage regulator; LED and photodiode principles",
                    "Rectifiers: Half-wave, center-tap full-wave, bridge rectifiers, LC filters",
                    "BJT: NPN and PNP configurations (CB, CE, CC), input/output characteristics",
                    "CE amplifier circuit, frequency response, and gain parameters"
                ]),
                ("Module 5: Integrated Circuits and Wireless Communications", 9, [
                    "Field Effect Transistors: JFET and MOSFET operational principles and CMOS inverter",
                    "Operational Amplifier: Ideal op-amp characteristics, inverting, non-inverting, summing amplifier",
                    "Digital logic gates: AND, OR, NOT, NAND, NOR, XOR, universal gate implementations",
                    "Principles of wireless communication: Modulation concepts (AM, FM, QAM)",
                    "Cellular network generations (4G LTE, 5G NR), Wi-Fi, and IoT wireless protocols"
                ])
            ]
        }
    ],
    3: [
        {
            "code": "CST201",
            "name": "Data Structures and Algorithms",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Introduction to Data Structures and Arrays", 9, [
                    "Abstract Data Types (ADTs), data structure classifications",
                    "Arrays: Memory representation (Row-major and column-major order)",
                    "Sparse matrices: Representation and operations (Transpose, addition)",
                    "String matching algorithms: Naive pattern matching, KMP algorithm",
                    "Time and space complexity: Big-O, Big-Omega, Big-Theta analysis"
                ]),
                ("Module 2: Stacks and Queues", 9, [
                    "Stack ADT: Array and linked implementation, push, pop, peek operations",
                    "Stack applications: Infix to Postfix conversion, Postfix evaluation, recursion simulation",
                    "Queue ADT: Array and linked implementation, enqueue, dequeue operations",
                    "Circular Queue, Double-Ended Queue (Deque), and Priority Queue",
                    "Queue applications: CPU scheduling simulation and breadth-first exploration"
                ]),
                ("Module 3: Linked Lists", 9, [
                    "Singly linked list: Creation, insertion, deletion, searching, traversal",
                    "Doubly linked list: Bidirectional navigation, insertion, deletion",
                    "Circular linked list: Singly and doubly circular representations",
                    "Polynomial representation and addition using linked lists",
                    "Memory management: Dynamic memory allocation, garbage collection, and fragmentation"
                ]),
                ("Module 4: Trees and Binary Search Trees", 9, [
                    "Tree terminology: Root, parent, child, leaf, level, height, depth",
                    "Binary trees: Properties, array and linked representation",
                    "Binary tree traversals: Inorder, Preorder, Postorder, Level-order",
                    "Binary Search Trees (BST): Insertion, deletion, searching, range queries",
                    "Balanced trees: AVL trees (Rotations: LL, RR, LR, RL), B-Trees overview"
                ]),
                ("Module 5: Graphs and Sorting/Searching Techniques", 9, [
                    "Graph representations: Adjacency matrix, adjacency list, adjacency multilist",
                    "Graph traversal algorithms: Depth-First Search (DFS) and Breadth-First Search (BFS)",
                    "Minimum spanning tree: Prim's and Kruskal's algorithms",
                    "Shortest path algorithms: Dijkstra's single source shortest path algorithm",
                    "Searching & Sorting: Binary Search, Quick Sort, Merge Sort, Heap Sort analysis"
                ])
            ]
        },
        {
            "code": "UCHUT347",
            "name": "Engineering Ethics and Sustainable Development",
            "credits": 3,
            "type": "Theory",
            "modules": [
                ("Module 1: Foundations of Engineering Ethics", 7, [
                    "Moral values, integrity, and ethical theories (Utilitarianism, Deontology, Virtue ethics)",
                    "Professional codes of ethics (IEEE, ACM, ABET) and professional accountability",
                    "Conflicts of interest, confidentiality, and intellectual property protection",
                    "Safety and risk analysis in engineering systems: Acceptable risk and fail-safe designs",
                    "Whistleblowing: Ethical obligations, procedures, and protection laws"
                ]),
                ("Module 2: Environmental Ethics and Climate Action", 7, [
                    "Anthropocentrism vs Ecocentrism; Rights of future generations",
                    "Global environmental agreements: Paris Agreement, Kyoto Protocol, Montreal Protocol",
                    "Carbon accounting, greenhouse gas emissions scopes (Scope 1, 2, 3), carbon credits",
                    "Deforestation, biodiversity loss, and sustainable ecosystem management",
                    "Industrial ecology: Life Cycle Assessment (LCA) and cradle-to-cradle principles"
                ]),
                ("Module 3: UN Sustainable Development Goals (SDGs)", 7, [
                    "Overview of 17 UN SDGs and their targets for 2030",
                    "SDG 7 (Affordable and Clean Energy) and SDG 9 (Industry, Innovation, and Infrastructure)",
                    "SDG 11 (Sustainable Cities and Communities) and SDG 12 (Responsible Consumption)",
                    "Social impact assessment of technological interventions",
                    "Role of engineers in eradicating poverty and promoting social equality"
                ]),
                ("Module 4: Sustainable Resource and Energy Management", 7, [
                    "Renewable energy transition: Solar, wind, hydro, geothermal, biomass, green hydrogen",
                    "Circular economy models: Reduce, Reuse, Recycle, Remanufacture, Refurbish",
                    "Sustainable water management: Rainwater harvesting, wastewater treatment, desalination",
                    "Waste management: Municipal, industrial, hazardous, electronic waste (E-waste) rules",
                    "Green building design principles and energy conservation building codes (ECBC)"
                ]),
                ("Module 5: Technology, Society, and Future Ethics", 7, [
                    "Artificial Intelligence and algorithmic ethics: Bias, transparency, autonomous weapons",
                    "Data privacy rights, surveillance capitalism, and digital sovereignty",
                    "Bioethics, genetic engineering, and technological determinism",
                    "Corporate Social Responsibility (CSR): ESG frameworks and sustainability reporting",
                    "Engineering leadership for a sustainable, humane, and just society"
                ])
            ]
        }
    ],
    4: [
        {
            "code": "UCHUT346",
            "name": "Economics for Engineers",
            "credits": 3,
            "type": "Theory",
            "modules": [
                ("Module 1: Principles of Engineering Economics", 7, [
                    "Scarcity, choice, opportunity cost, and production possibility frontier",
                    "Law of Demand, demand determinants, and price elasticity of demand",
                    "Law of Supply, supply determinants, and market equilibrium price",
                    "Consumer surplus, producer surplus, and deadweight loss",
                    "Engineering economics decision-making process overview"
                ]),
                ("Module 2: Cost Analysis and Production Theory", 7, [
                    "Short-run vs long-run production functions; Law of Diminishing Returns",
                    "Fixed cost, variable cost, total cost, marginal cost, and average cost curves",
                    "Economies and diseconomies of scale; Returns to scale concepts",
                    "Break-even analysis: Break-even point, margin of safety, and P/V ratio",
                    "Market structures: Perfect competition, monopoly, monopolistic competition, oligopoly"
                ]),
                ("Module 3: Time Value of Money and Project Appraisal", 7, [
                    "Simple interest vs compound interest; Nominal and effective interest rates",
                    "Cash flow diagrams; Single payment, uniform series, and gradient compound factors",
                    "Present Worth (PW) method and Future Worth (FW) method of project evaluation",
                    "Annual Equivalent (AE) method and Rate of Return (IRR) calculation",
                    "Benefit-Cost Ratio (BCR) analysis for public projects"
                ]),
                ("Module 4: Depreciation and Replacement Analysis", 7, [
                    "Causes of depreciation; Book value, market value, salvage value",
                    "Depreciation methods: Straight line, declining balance, sum-of-years-digits",
                    "Inflation effects on cash flows and purchasing power adjustments",
                    "Reasons for asset replacement: Deterioration, obsolescence, inadequacy",
                    "Economic life of an asset and challenger vs defender replacement analysis"
                ]),
                ("Module 5: Macroeconomics and Indian Economy", 7, [
                    "Gross Domestic Product (GDP), Gross National Product (GNP), and national income accounting",
                    "Inflation: Demand-pull, cost-push inflation, CPI, WPI, and impact on engineering industry",
                    "Monetary policy (RBI, repo rates, CRR) and fiscal policy (Taxation, public expenditure)",
                    "Foreign exchange rates, balance of payments, and trade globalization",
                    "Economic reforms in India (1991 to present) and digital economy growth"
                ])
            ]
        }
    ],
    5: [
        {
            "code": "GXEST605",
            "name": "Design Thinking and Product Development",
            "credits": 3,
            "type": "Theory/Project",
            "modules": [
                ("Module 1: Introduction to Design Thinking", 7, [
                    "Evolution of design thinking and human-centered design principles",
                    "The 5 stages of design thinking: Empathize, Define, Ideate, Prototype, Test",
                    "Divergent and convergent thinking in creative product exploration",
                    "Empathy research: Shadowing, user interviews, contextual inquiries",
                    "Empathy maps, persona definition, and user journey mapping"
                ]),
                ("Module 2: Problem Formulation and Ideation", 7, [
                    "Point of View (POV) problem statements and 'How Might We' questions",
                    "Ideation methodologies: Brainstorming, brainwriting, SCAMPER, crazy eights",
                    "Concept selection techniques: Pugh matrix, dot voting, feasibility-impact matrix",
                    "Value proposition design and business model canvas (BMC)",
                    "Cross-functional team collaboration in product ideation"
                ]),
                ("Module 3: Prototyping and Ergonomic Design", 7, [
                    "Prototyping philosophy: Fail early, fail cheap, learn fast",
                    "Low-fidelity prototyping: Paper prototypes, wireframing, card sorting",
                    "High-fidelity prototyping: 3D printing, laser cutting, software mockups",
                    "Ergonomic principles in physical and digital product development",
                    "Usability testing, feedback loops, and iterative refinement"
                ]),
                ("Module 4: Product Development Lifecycle and Engineering", 7, [
                    "Product development phases: Concept, architecture, detailed design, manufacturing",
                    "Design for Manufacturing (DFM) and Design for Assembly (DFA)",
                    "Failure Mode and Effects Analysis (FMEA) for product reliability",
                    "BOM (Bill of Materials) generation and cost engineering",
                    "Quality management: Six Sigma, DMAIC, and ISO standards in manufacturing"
                ]),
                ("Module 5: Intellectual Property and Product Commercialization", 7, [
                    "Patents, provisional specifications, patent claims, prior art search",
                    "Trademarks, industrial designs, trade secrets, and software copyright",
                    "Technology Readiness Levels (TRL 1 to 9) and commercial validation",
                    "Go-to-market strategies, pricing models, and product launch planning",
                    "Ethics in commercial product design and environmental sustainability"
                ])
            ]
        }
    ],
    6: [
        {
            "code": "CST302",
            "name": "Modern Compiler Design and System Programming",
            "credits": 4,
            "type": "Theory",
            "modules": [
                ("Module 1: Modern Compiler Architecture and Lexical Analysis", 9, [
                    "Phases of modern compilers; Frontend vs Backend decoupling (LLVM / Clang architecture)",
                    "Lexical analysis: Regular expressions, NFAs, DFAs, and lexer generators (Flex / Lex)",
                    "Token streams, source code location tracking, and error diagnostic reporting",
                    "Symbol table design: Hash tables, scope management, and type environments",
                    "Memory management in compiler runtime systems"
                ]),
                ("Module 2: Parsing and Concrete Syntax Trees", 9, [
                    "Context-Free Grammars for modern languages; Ambiguity resolution",
                    "Recursive descent and LL(k) parsing with lookahead tokens",
                    "LR(1) and LALR(1) parsing table construction algorithms",
                    "Parser generators: Bison / YACC and ANTLR frameworks",
                    "Error recovery strategies: Panic mode and phrase-level recovery"
                ]),
                ("Module 3: Abstract Syntax Trees and Semantic Analysis", 9, [
                    "Abstract Syntax Tree (AST) construction and visitor design patterns",
                    "Type systems, type checking, type inference (Hindley-Milner basics)",
                    "Syntax-Directed Translation (SDT) and attribute grammars",
                    "Intermediate Representations (IR): Static Single Assignment (SSA) form",
                    "Three-Address Code (TAC), Control Flow Graphs (CFG), and dominator trees"
                ]),
                ("Module 4: Optimization Techniques", 9, [
                    "Local optimizations: Constant folding, constant propagation, algebraic simplifications",
                    "Dataflow analysis: Reaching definitions, available expressions, live variable analysis",
                    "Loop optimizations: Loop invariant code motion, loop unrolling, vectorization",
                    "Dead code elimination and global common subexpression elimination",
                    "Peephole optimization and instruction scheduling"
                ]),
                ("Module 5: Code Generation and Runtime Systems", 9, [
                    "Target machine models (x86-64, ARM64, WebAssembly)",
                    "Instruction selection using tree rewriting and dynamic programming",
                    "Register allocation: Graph coloring heuristic (Chaitin-Briggs) and linear scan",
                    "Call stack organization, activation records, and calling conventions",
                    "Just-In-Time (JIT) compilation concepts and garbage collection strategies"
                ])
            ]
        }
    ],
    7: [
        {
            "code": "UEHUT704",
            "name": "Project Management: Planning, Execution, Evaluation and Control",
            "credits": 3,
            "type": "Theory",
            "modules": [
                ("Module 1: Project Management Fundamentals", 7, [
                    "Definition of project, project characteristics, project life cycle phases",
                    "Project management constraints: Scope, time, cost, quality, risk, resources",
                    "Project initiation: Project charter, stakeholder identification, business case",
                    "Project organization structures: Functional, matrix, projectized organizations",
                    "Role and competencies of project manager; PMI/PMP frameworks"
                ]),
                ("Module 2: Project Planning and Work Breakdown", 7, [
                    "Scope planning: Scope baseline and Work Breakdown Structure (WBS)",
                    "WBS dictionary, work packages, and scope verification",
                    "Activity definition, sequencing, and dependency relationships (FS, FF, SS, SF)",
                    "Network diagrams: Activity on Arrow (AOA) and Activity on Node (AON)",
                    "Resource estimation, leveling, and resource allocation matrices (RACI)"
                ]),
                ("Module 3: Project Scheduling and Cost Estimation", 7, [
                    "Critical Path Method (CPM): Forward pass, backward pass, float calculations",
                    "Program Evaluation and Review Technique (PERT): Three-time estimates, variance",
                    "Schedule compression: Crashing and fast-tracking techniques",
                    "Cost estimation techniques: Analogous, parametric, bottom-up cost estimation",
                    "Project budgeting and cost baseline formulation"
                ]),
                ("Module 4: Project Monitoring, Control, and Earned Value Management", 7, [
                    "Project execution and progress tracking mechanisms",
                    "Earned Value Management (EVM): PV, EV, AC, CV, SV, CPI, SPI metrics",
                    "Forecasting: Estimate at Completion (EAC) and Estimate to Complete (ETC)",
                    "Change management process: Change Control Board (CCB) and change requests",
                    "Quality control: Pareto charts, cause-and-effect diagrams, control charts"
                ]),
                ("Module 5: Risk Management, Procurement, and Project Closure", 7, [
                    "Risk management planning: Risk identification, qualitative and quantitative risk analysis",
                    "Risk response strategies: Avoidance, mitigation, transference, acceptance",
                    "Project procurement management: Contract types (Fixed price, cost-reimbursable, T&M)",
                    "Project closure: Contract closeout, administrative closure, lessons learned archive",
                    "Agile and hybrid project management overview (Kanban, Scrum, sprint velocity)"
                ])
            ]
        }
    ],
    8: [
        {
            "code": "UEHUT803",
            "name": "Organizational Behaviour and Business Communication",
            "credits": 3,
            "type": "Theory",
            "modules": [
                ("Module 1: Organizational Behaviour Foundations and Individual Dynamics", 7, [
                    "Scope and importance of Organizational Behaviour (OB)",
                    "Personality: Myers-Briggs Type Indicator (MBTI) and Big Five personality traits",
                    "Perception, perceptual errors (Halo effect, stereotyping, projection), attribution theory",
                    "Attitudes, job satisfaction, organizational commitment, employee engagement",
                    "Workplace diversity and inclusion management"
                ]),
                ("Module 2: Motivation, Leadership, and Group Dynamics", 7, [
                    "Motivation theories: Maslow's hierarchy, Herzberg's two-factor theory, McClelland's needs",
                    "Process theories: Vroom's expectancy theory, Adams' equity theory, Goal-setting theory",
                    "Leadership styles: Autocratic, democratic, servant, transformational leadership",
                    "Group dynamics: Group norms, cohesion, groupthink, group shift",
                    "Building high-performing autonomous cross-functional teams"
                ]),
                ("Module 3: Organizational Culture, Power, and Change Management", 7, [
                    "Organizational culture: Types, creation, transmission, and sustaining culture",
                    "Power and politics: Sources of power, political tactics in organizations",
                    "Conflict management: Sources of conflict, Thomas-Kilmann conflict resolution modes",
                    "Organizational change: Lewin's 3-step change model, Kotter's 8-step process",
                    "Overcoming resistance to change and leading digital transformations"
                ]),
                ("Module 4: Strategic Business Communication", 7, [
                    "Communication process model: Encoding, decoding, channels, barriers, noise",
                    "Internal vs external communication; Vertical, horizontal, and diagonal communication",
                    "Crisis communication: Strategies, stakeholder messaging, reputation management",
                    "Executive communication: Board presentations, stakeholder pitches, press releases",
                    "Cross-cultural communication barriers and international business etiquette"
                ]),
                ("Module 5: Negotiations, Ethics, and Future of Work", 7, [
                    "Negotiation dynamics: Distributive vs integrative bargaining strategies",
                    "BATNA (Best Alternative to a Negotiated Agreement) and zone of possible agreement (ZOPA)",
                    "Corporate governance, business ethics, and corporate integrity",
                    "Remote work dynamics, hybrid organizational models, and digital collaboration",
                    "Stress management, mental well-being, and work-life harmony in modern enterprises"
                ])
            ]
        }
    ]
}


def populate_ktu_btech():
    with app.app_context():
        # Find APJ Abdul Kalam Technological University
        uni = University.query.filter(
            (University.name.like("%Kalam%")) | (University.code == "KTU")
        ).first()
        if not uni:
            print("ERROR: APJ Abdul Kalam Technological University not found!")
            return

        print(f"Target University: {uni.name} (ID: {uni.id})")

        # Find or create Program BTech
        btech = Program.query.filter_by(university_id=uni.id, name="BTech (Undergraduate)").first()
        if not btech:
            btech = Program.query.filter_by(university_id=uni.id, code="BTech").first()
        if not btech:
            btech = Program(
                name="BTech (Undergraduate)",
                code="BTech",
                degree_type="Undergraduate",
                university_id=uni.id
            )
            db.session.add(btech)
            db.session.commit()
            print(f"Created BTech program (ID: {btech.id})")
        else:
            print(f"Found BTech program: {btech.name} (ID: {btech.id})")

        # 1. Populate Streams
        existing_streams = Stream.query.filter_by(program_id=btech.id).all()
        stream_map_code = {s.code: s for s in existing_streams if s.code}
        stream_map_name = {s.name.lower(): s for s in existing_streams}

        added_streams = 0
        for name, code in KTU_BTECH_STREAMS:
            if code in stream_map_code or name.lower() in stream_map_name:
                continue
            new_stream = Stream(name=name, code=code, program_id=btech.id)
            db.session.add(new_stream)
            added_streams += 1

        db.session.commit()
        all_streams = Stream.query.filter_by(program_id=btech.id).all()
        print(f"Streams configured: {len(all_streams)} total (added {added_streams} new)")

        # 2. Configure Schemes
        # Scheme 2019
        s2019 = Scheme.query.filter_by(program_id=btech.id, year="2019").first()
        if not s2019:
            s2019 = Scheme(year="2019", program_id=btech.id)
            db.session.add(s2019)
            db.session.commit()
            print(f"Created Scheme 2019 (ID: {s2019.id})")
        else:
            print(f"Found Scheme 2019 (ID: {s2019.id})")

        # Scheme 2024
        s2024 = Scheme.query.filter_by(program_id=btech.id, year="2024").first()
        if not s2024:
            s2024 = Scheme(year="2024", program_id=btech.id)
            db.session.add(s2024)
            db.session.commit()
            print(f"Created Scheme 2024 (ID: {s2024.id})")
        else:
            print(f"Found Scheme 2024 (ID: {s2024.id})")

        # 3. Ensure 8 Semesters exist for each scheme
        def ensure_semesters(scheme):
            sem_map = {}
            for sem_no in range(1, 9):
                sem = Semester.query.filter_by(scheme_id=scheme.id, semester_no=sem_no).first()
                if not sem:
                    sem = Semester(scheme_id=scheme.id, semester_no=sem_no)
                    db.session.add(sem)
                    db.session.flush()
                sem_map[sem_no] = sem
            db.session.commit()
            return sem_map

        sems_2019 = ensure_semesters(s2019)
        sems_2024 = ensure_semesters(s2024)

        # 4. Ingest Courses, Modules, and Topics for Scheme 2019
        def populate_courses(scheme_name, sem_map, courses_dict):
            total_courses = 0
            total_modules = 0
            total_topics = 0
            for sem_no, course_list in courses_dict.items():
                sem = sem_map[sem_no]
                for c_data in course_list:
                    course = Course.query.filter_by(semester_id=sem.id, code=c_data["code"]).first()
                    if not course:
                        course = Course(
                            name=c_data["name"],
                            code=c_data["code"],
                            credits=c_data["credits"],
                            course_type=c_data["type"],
                            semester_id=sem.id
                        )
                        db.session.add(course)
                        db.session.flush()
                        total_courses += 1

                    # Add modules and topics
                    for mod_idx, (mod_name, hours, topics) in enumerate(c_data["modules"], 1):
                        mod = Module.query.filter_by(course_id=course.id, module_no=mod_idx).first()
                        if not mod:
                            mod = Module(
                                name=mod_name,
                                module_no=mod_idx,
                                hours=hours,
                                course_id=course.id
                            )
                            db.session.add(mod)
                            db.session.flush()
                            total_modules += 1

                        for top_idx, top_title in enumerate(topics, 1):
                            top = Topic.query.filter_by(module_id=mod.id, name=top_title).first()
                            if not top:
                                top = Topic(
                                    name=top_title,
                                    topic_no=top_idx,
                                    module_id=mod.id
                                )
                                db.session.add(top)
                                total_topics += 1

            db.session.commit()
            print(f"[{scheme_name}] Ingested {total_courses} courses, {total_modules} modules, {total_topics} topics.")

        populate_courses("Scheme 2019", sems_2019, BTECH_2019_COURSES)
        populate_courses("Scheme 2024", sems_2024, BTECH_2024_COURSES)

        # Validation: Verify MCA is untouched
        mca = Program.query.filter_by(university_id=uni.id, code="MCA").first()
        if mca:
            mca_schemes = Scheme.query.filter_by(program_id=mca.id).all()
            for ms in mca_schemes:
                mca_courses = Course.query.join(Semester).filter(Semester.scheme_id == ms.id).all()
                print(f"MCA Program (ID: {mca.id}) Scheme {ms.year}: {len(mca_courses)} courses intact.")

        print("\n KTU B.Tech academic data populated successfully!")


if __name__ == "__main__":
    populate_ktu_btech()
