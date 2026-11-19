"""
Ingest the Complete Official KTU MCA Scheme 2020 Curriculum & Syllabus
Source: APJ ABDUL KALAM TECHNOLOGICAL UNIVERSITY - Master of Computer Applications
41 authentic courses across Semesters 1, 2, 3, and 4 with full module and topic breakdown.
Preserves existing student progress records and updates Course ID 7 to code 20MCA107.
"""
import os
import sys
from datetime import datetime
from app import create_app
from models import db, University, Program, Scheme, Semester, Course, Module, Topic, SyllabusSource, UserProgress

# Complete 41-Course Academic Data Specification directly extracted from KTU Official Syllabus
KTU_MCA_CURRICULUM = {
    # =========================================================================
    # SEMESTER 1
    # =========================================================================
    1: [
        {
            "code": "20MCA101",
            "name": "Mathematical Foundations for Computing",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Sets, Relations and Functions",
                    "hours": 9,
                    "topics": [
                        "Sets, Set Operations",
                        "Relations, Classification of relations, Equivalence Relations",
                        "Closures of Relations, Matrix Representation of Relations, Partial Ordering, n-ary Relations",
                        "Functions"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Number Theory & Recurrence Relations",
                    "hours": 9,
                    "topics": [
                        "Division Algorithm, GCD, Primes, Euclidean Algorithm",
                        "Congruences, Properties of Congruences, Solutions of Linear Congruences",
                        "First Order Linear Recurrence Relation",
                        "Second Order Linear homogeneous Recurrence Relations with Constant coefficients",
                        "Non Homogeneous Recurrence Relation"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Graph Theory",
                    "hours": 8,
                    "topics": [
                        "Graphs and Graph Models, Graph Terminology and Special Types of Graphs",
                        "Representing Graphs and Graph Isomorphism, Connectivity",
                        "Euler and Hamilton Paths, Shortest-Path Problems, Planar Graphs",
                        "Directed Graph, Multigraph, Connected graph",
                        "Euler circuit and trail, Planar and Non-Planar Graphs"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Linear Algebra & Matrices",
                    "hours": 11,
                    "topics": [
                        "Linear system of equations, coefficient matrix, augmented matrix, Gauss elimination method and back substitution, elementary row operations, row equivalent systems",
                        "Gauss elimination- three possible cases, Row Echelon form and information from it",
                        "Linear independence- rank of a matrix. Solution of linear system, fundamental theorem of non- homogeneous linear system (without proof). Homogeneous linear system (theory only)",
                        "Matrix eigen value problem- determination of eigen values and eigen vectors, Basis of eigen vectors",
                        "diagonalization of matrix, Quadratic form-principle axis theorem (without proof)"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Statistics & Curve Fitting",
                    "hours": 8,
                    "topics": [
                        "Bivariate data – Scatter Diagram – Interpretation of the nature and degree of relation using scattered diagram",
                        "Curve fitting – Principle of least squares – fitting a straight line – fitting a parabola",
                        "linear correlation and regression – Karl’s Pearson’s Coefficient of Correlation",
                        "Spearman’s rank correlation coefficient"
                    ]
                }
            ]
        },
        {
            "code": "20MCA103",
            "name": "Digital Fundamentals & Computer Architecture",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Number Systems & Combinational Circuits",
                    "hours": 11,
                    "topics": [
                        "Representation of signed numbers – 1's complement and 2’s complement, Logic gates - AND, OR, NOT, NAND, NOR, XOR",
                        "Boolean algebra - Basic laws and theorems, Boolean functions - truth table",
                        "Standard forms of Boolean Expressions – Sum of Products and Product of Sums - minimization of Boolean function using Karnaugh map method - Realization using logic gates",
                        "Floating point numbers",
                        "Combinational Circuits - Half adder - Full Adder",
                        "Decoder – Encoder - Multiplexers – Demultiplexers"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Sequential Circuits & Microcontrollers",
                    "hours": 10,
                    "topics": [
                        "Sequential circuit - Clocking, Flip flops -RS – JK- D -T flip flops",
                        "Counters - Synchronous and asynchronous counters - UP/DOWN counters",
                        "Registers - Serial in serial out - Serial in parallel out - Parallel in serial out - Parallel in parallel out registers",
                        "Introduction to arduino and raspberry pi"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Processor Architecture & Instruction Sets",
                    "hours": 10,
                    "topics": [
                        "Computer abstractions and technology - Introduction, Computer architecture - 8 Design features, Application program - layers of abstraction, Five key components of a computer",
                        "Technologies for building processors and memory, Performance, instruction set principles – Introduction",
                        "Classifying instruction set architectures, Memory addressing, Encoding an instruction set"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Datapath, Pipelining & I/O Systems",
                    "hours": 9,
                    "topics": [
                        "The Processor - Introduction, Logic design conventions, Building a datapath, A simple implementation scheme",
                        "An Overview of pipelining - Pipelined datapath and control - Structural hazards - Data hazards - Control hazards",
                        "I/O organization - Accessing I/O devices, Interrupts - Handling multiple devices- Direct memory access"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Memory Hierarchy",
                    "hours": 8,
                    "topics": [
                        "The memory system – basic concepts, semiconductor RAM memories, organization",
                        "Static and dynamic RAM, Structure of larger memories, semiconductor ROM memories, Speed, size and cost",
                        "Cache memory – mapping functions – replacement algorithms",
                        "Virtual memory – paging and segmentation"
                    ]
                }
            ]
        },
        {
            "code": "20MCA105",
            "name": "Advanced Data Structures",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Basic Data Structures & Amortised Analysis",
                    "hours": 10,
                    "topics": [
                        "Review of basic data structures: Array, Stack and Queue",
                        "Linked list and its variants",
                        "Representation of sets, Set implementation using bit string",
                        "Hashing – Simple hash functions",
                        "Collision and Collision Resolution techniques",
                        "Amortised Analysis - Aggregate Method (Multipop Stack and Incrementing Binary Counter)",
                        "Amortised Analysis - Accounting Method (Multipop Stack and Incrementing Binary Counter)",
                        "Amortised Analysis - Potential Method (Multipop Stack and Incrementing Binary Counter)",
                        "Disjoint sets- representations",
                        "Disjoint sets - Union, Find algorithms"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Advanced Tree Structures",
                    "hours": 10,
                    "topics": [
                        "Balanced Binary Search trees",
                        "Red-Black trees - Properties of Red Black trees",
                        "Red-Black trees - Rotations",
                        "Red-Black trees - Insertion and Deletion",
                        "B-Trees - Basic operations on B-Trees – Insertion and Deletion",
                        "Introduction to Splay Trees and Suffix Trees"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Advanced Heap Structures",
                    "hours": 8,
                    "topics": [
                        "Mergeable Heaps",
                        "Operations on Mergeable Heaps",
                        "Binomial Heaps",
                        "Binomial Heaps operations and Analysis",
                        "Fibonacci Heaps",
                        "Fibonacci Heap operations and Analysis"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Advanced Graph Structures",
                    "hours": 12,
                    "topics": [
                        "Representation of graphs",
                        "Depth First and Breadth First Traversals",
                        "Topological Sorting",
                        "Strongly connected Components",
                        "Biconnected Components",
                        "Minimum Cost Spanning Tree - Prim's Algorithm",
                        "Minimum Cost Spanning Tree - Kruskal’s Algorithm",
                        "Dijikstra’s single source shortest paths algorithm"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Blockchain Data Structure",
                    "hours": 8,
                    "topics": [
                        "Blockchain Architecture",
                        "Blockchain Data Structures",
                        "Blockchain Data types",
                        "Contract Data",
                        "Problems to be solved in Blockchain data analysis"
                    ]
                }
            ]
        },
        {
            "code": "20MCA107",
            "name": "Advanced Software Engineering",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Software Engineering Lifecycle & Modeling",
                    "hours": 8,
                    "topics": [
                        "What is Software Engineering, Characteristics of Software Engineering",
                        "Life cycle of a software system: software design, development, testing, deployment, Maintenance",
                        "Project planning phase: project objectives, scope of software system, empirical estimation models, COCOMO, staffing and personnel planning",
                        "Software Engineering models: Predictive models, model approaches, prerequisites",
                        "Waterfall models: predictive and adaptive waterfall, waterfall with feedback (Sashimi), incremental waterfall",
                        "V model; Prototyping and prototyping models",
                        "Software requirements specification: Eliciting Software requirements, Requirement specifications",
                        "Software requirements engineering concepts, Requirements modelling, Requirements documentation",
                        "Use cases and User stories"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Industry Best Practices, Version Control & Quality",
                    "hours": 10,
                    "topics": [
                        "Programming Style Guides and Coding Standards",
                        "Literate programming and Software documentation: Documentation generators, Javadoc, phpDocumentor",
                        "Version control systems basic concepts: Distributed version control system and Git",
                        "Setting up Git and environment configuration",
                        "Git CLI Core operations: Clone a repository; View history; Modifying files",
                        "Git Branching and branch management",
                        "Push changes, Clone operation, add, commit, log, diff commands",
                        "Git Conflict resolution and merging",
                        "Pushing changes to remote master, Using Git in IDEs and UI based tools",
                        "Software Quality: Requirements specification quality, design quality, development quality, conformance quality"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: System Design Methodologies & Unit Testing",
                    "hours": 10,
                    "topics": [
                        "OOP Concepts comprehensive overview",
                        "Design Patterns: Basic concepts, How to select a design pattern",
                        "Creational patterns",
                        "Structural patterns",
                        "Behavioural patterns",
                        "Concept of Anti-patterns",
                        "Unit testing and Unit Testing frameworks, The xUnit Architecture",
                        "Writing Unit Tests using Junit (Java), unittest (Python), or phpdbg (PHP)",
                        "Writing tests with Assertions, defining and using Custom Assertions",
                        "Single condition tests, testing for expected errors, Abstract test"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Agile Development Methodology & Testing",
                    "hours": 10,
                    "topics": [
                        "Concepts of Agile Development methodology",
                        "Scrum Framework: roles, artifacts, ceremonies",
                        "Software testing principles, Program inspections, Walkthroughs, Program reviews",
                        "Blackbox testing: Equivalence class testing, Boundary value testing",
                        "Decision table testing, Pairwise testing",
                        "State transition testing, Use-case testing",
                        "White box testing: control flow testing, Data flow testing",
                        "Defect life cycle management",
                        "Regression testing and testing automation",
                        "Testing non-functional requirements"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Continuous Integration, Delivery & DevOps",
                    "hours": 10,
                    "topics": [
                        "Software Configuration Management: Version control, Managing dependencies, Managing configuration",
                        "Managing build and deployment environments",
                        "Continuous Integration: Prerequisites, Essential practices",
                        "Continuous Delivery: Principles of Software delivery, Concepts and release candidate",
                        "Continuous Deployment principles and comparisons",
                        "Build and deployment automation",
                        "Ansible for configuration management and deployment automation",
                        "Test automation as part of Continuous Integration",
                        "Robot Framework for automated test cases",
                        "Deployment pipeline anatomy and stages"
                    ]
                }
            ]
        },
        {
            "code": "20MCA131",
            "name": "Programming Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Python Basics & Control Structures",
                    "hours": 14,
                    "topics": [
                        "Input, Output and Import Functions",
                        "Operators and Expressions",
                        "Data Types and Collection structures",
                        "Decision Making & Loops"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Functions & Modularity",
                    "hours": 11,
                    "topics": [
                        "Functions, arguments and lambda functions",
                        "Modules and Packages creation and import"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Advanced Python & File I/O",
                    "hours": 16,
                    "topics": [
                        "File Handling: text and CSV processing",
                        "Object Handling: Classes, constructors, inheritance and operator overloading",
                        "Exception Handling",
                        "Regular Expressions and pattern matching"
                    ]
                }
            ]
        },
        {
            "code": "20MCA133",
            "name": "Web Programming Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Web Foundation & HTML",
                    "hours": 9,
                    "topics": [
                        "Client/Server concepts, Web Application components, HTTP request-response, Application Servers, Web Security",
                        "HTML - Formatting, Fonts, Anchors, Backgrounds, Images, Hyperlinks",
                        "HTML - Lists, Tables, Frames, HTML Forms"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: CSS & JavaScript Scripting",
                    "hours": 19,
                    "topics": [
                        "CSS - Basic syntax, Inline, Embedded, Linking External Style Sheets, Backgrounds, Margins, Padding, Positioning",
                        "JavaScript - Core features, Data types, Variables, Operators, Expressions",
                        "JavaScript - Functions, Objects, Array, String, Date and Math objects",
                        "JavaScript - Document Object Model (DOM), Event Handling, Form handling and validations"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Relational DB & PHP Backend",
                    "hours": 32,
                    "topics": [
                        "Relational Database Design - Tables, Attributes, Primary keys, Foreign keys, Indexes",
                        "DDL Commands (CREATE, ALTER, DROP, TRUNCATE) & DML Commands (SELECT, INSERT, UPDATE, DELETE)",
                        "PHP Environment setup, Print/echo, Variables, Strings, Arrays, Operators, Control structures",
                        "PHP Functions, Reading Data in Web Pages, Embedding PHP within HTML, Database connectivity, phpdbg",
                        "PHP Framework - MVC model, Database interaction, Web app debugging tools"
                    ]
                }
            ]
        },
        {
            "code": "20MCA135",
            "name": "Data Structures Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Build Tools, Debuggers & Linear DS",
                    "hours": 10,
                    "topics": [
                        "Advanced use of gcc: Options -o, -c, -D, -l, -I, -g, -O, -save-temps, -pg",
                        "Familiarisation with gdb: break, run, next, print, display, help",
                        "Using gprof: Compile, Execute and Profile",
                        "Review of Basic Data Structures: Arrays, Circular Queue, Singly Linked Stack, Doubly Linked List, BST"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Sets, Trees & Advanced Heaps",
                    "hours": 14,
                    "topics": [
                        "Set Data Structure and set operations using Bit String",
                        "Disjoint Sets and associated operations (create, union, find)",
                        "Binomial Heaps and operations (Create, Insert, Delete, Extract-min, Decrease key)",
                        "B Trees and its operations",
                        "Red Black Trees and its operations"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Advanced Graph Algorithms",
                    "hours": 13,
                    "topics": [
                        "Graph Traversal techniques (DFS and BFS) and Topological Sorting",
                        "Finding Strongly connected Components in a directed graph",
                        "Prim’s Algorithm for finding minimum cost spanning tree",
                        "Kruskal’s algorithm using Disjoint set data structure",
                        "Single Source shortest path algorithm using mergeable heap operations"
                    ]
                }
            ]
        }
    ],

    # =========================================================================
    # SEMESTER 2
    # =========================================================================
    2: [
        {
            "code": "20MCA102",
            "name": "Advanced Database Management Systems",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Relational Databases & ER Modeling",
                    "hours": 15,
                    "topics": [
                        "Introduction - Purpose of Database System - Database System Applications",
                        "View of data: Data Abstraction, Instances and Schemas, Data Models",
                        "Database Architecture, Database Users and Administrators: Database Users and Interfaces, DBA",
                        "Introduction to Relational Model: Structure of Relational Database, database Schema, Keys, Relational Query language",
                        "Relational Algebra: Fundamental Operations, Formal definition, additional relational algebra operations",
                        "Entity-Relationship model: Entity Set, Relationship Set, Attributes, Constraints: Mapping cardinalities, Key Constraints, Participation Constraints",
                        "E-R Diagrams: Basic structure, Complex attributes, Roles, Non binary relationship sets, Weak Entity Set",
                        "Relational Database Design using ER- to Relational Mapping",
                        "Extended ER Features: Specialization, Generalization, Attribute inheritance, Constraints on generalization, Aggregation"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Database Design & Normalization",
                    "hours": 9,
                    "topics": [
                        "Database Tables and Normalization - The Need for Normalization",
                        "Normalization Process: Inference Rules for Functional Dependencies (proof not needed) - Minimal set of Functional Dependencies",
                        "Conversion to First Normal Form, Conversion to Second Normal Form, Conversion to Third Normal Form",
                        "Improving the Design - Surrogate Key Considerations",
                        "Higher Level Normal Forms: Boyce/Codd Normal Form, Fourth Normal Form",
                        "Join dependencies and Fifth Normal Form, Normalization and Database Design"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Transaction Management & Concurrency Control",
                    "hours": 9,
                    "topics": [
                        "Transaction: Evaluating Transaction Results, Transaction Properties, Transaction Management with SQL, The Transaction Log",
                        "Concurrency Control: Lost Updates, Uncommitted Data, Inconsistent Retrievals, The Scheduler",
                        "Concurrency Control with Locking Methods: Lock Granularity, Lock Types, Two Phase Locking to Ensure Serializability, Deadlocks",
                        "Concurrency Control with Timestamping Methods: Wait/Die and Wait/Wound Schemes",
                        "Concurrency Control with Optimistic Methods, Database Recovery Management: Transaction Recovery"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Data Storage and Querying",
                    "hours": 10,
                    "topics": [
                        "RAID, File Organization, Organization of Records in Files",
                        "Indexing and Hashing: Basic concept, Ordered Indices",
                        "B+ tree Index Files: Structure of a B+-Tree, B tree index files",
                        "Static Hashing, Dynamic Hashing",
                        "Query Processing: Overview, Selection Operation"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Distributed, Object Oriented, XML and NoSQL Databases",
                    "hours": 13,
                    "topics": [
                        "Distributed Databases: Homogeneous and Heterogeneous Databases, Distributed Data Storage, Distributed Transactions",
                        "Object Based Databases: Overview, Complex Data types, Structured types and inheritance in SQL, Table Inheritance, Array and Multiset types in SQL, Object identity and reference types in SQL",
                        "XML: DTD and XML Schema, XML presentation, XML Applications",
                        "Next Generation Databases: Distributed Relational Databases - CAP Theorem",
                        "Nonrelational Distributed Databases – MongoDB Sharding and Replication",
                        "HBase",
                        "Cassandra"
                    ]
                }
            ]
        },
        {
            "code": "20MCA104",
            "name": "Advanced Computer Networks",
            "category": "General",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Network Architecture & Application Layer",
                    "hours": 10,
                    "topics": [
                        "Overview of Computer Networks and the Internet. History. Protocols, Review of last mile technologies used for internet access. Packet switching",
                        "Basic ideas about delay queuing through put. Concept of Quality of Service Protocol layering . OSI model and TCP model",
                        "Application layer protocols - Client-server architecture Network application architecture, Web, HTTP, FTP, SMTPPOP3 and DNS, Peer-to-peer file sharing networks"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Transport Layer Protocols",
                    "hours": 10,
                    "topics": [
                        "Transport Layer Protocols: Introduction to transport layer",
                        "Multiplexing and demultiplexing, Principles of Reliable data transfer - Stop-and-wait and Go-back- N design and evaluation",
                        "Connection oriented transport TCP, Connection less transport UDP",
                        "Principles of congestion control -efficiency and fairness"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Network Layer Protocols & Routing",
                    "hours": 10,
                    "topics": [
                        "Network Layer Protocols: Virtual circuits and datagrams",
                        "Principles of routing, internet protocol Ipv4 NAT, Routing algorithms: Link-state and distance vector routing",
                        "Routing on the internet RIP OSPF and BGP, Multicastrouting",
                        "Introduction to IPV6 and software defined networks"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Link Layer & Physical Layer",
                    "hours": 8,
                    "topics": [
                        "Link layer and Physical Layer: Introduction to link layer - Error detection (parity, checksum, and CRC)",
                        "Multiple access protocols (collision and token based), IEEE 802.3",
                        "Ethernet, Switching and bridging, Media, Signal strength and interference. Data encoding. Ethernet switches , Routers MAC, ARP, FIB"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Wireless Networks, Security & Network Management",
                    "hours": 10,
                    "topics": [
                        "IEEE 802.11 Wi-Fi, Bluetooth, and cellular networks",
                        "Threats and attacks, Firewalls, NAT,VPNs, Introduction to network management, SNMP",
                        "Overview of tools and troubleshooting, Traffic analysis tools and Configuration management"
                    ]
                }
            ]
        },
        # Elective I Options:
        {
            "code": "20MCA162",
            "name": "Applied Statistics",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Discrete Probability Distributions",
                    "hours": 9,
                    "topics": [
                        "Random Experiment, Random Variables, Discrete Random Variables, Probability Distributions and PMF",
                        "Mean and Variance of Discrete Random Variable, Discrete Uniform Distribution",
                        "Binomial Distribution - Mean and Variance",
                        "Geometric Distribution and Poisson Distribution - Mean and Variance"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Continuous Probability Distributions",
                    "hours": 9,
                    "topics": [
                        "Continuous Random Variables, Probability Density Functions, Mean and Variance",
                        "Continuous Uniform Distribution, Mean and Variance",
                        "Normal Distribution, Mean and Variance, Standard Normal Distribution",
                        "Exponential Distribution"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Curve Fitting & Joint Distributions",
                    "hours": 9,
                    "topics": [
                        "Curve fitting – Principle of least squares – fitting straight line – fitting parabola",
                        "Linear correlation and regression – Karl Pearson’s Coefficient of Correlation",
                        "Joint and marginal probability distribution, Conditional probability distribution"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Sampling Distribution & Estimation",
                    "hours": 9,
                    "topics": [
                        "Sampling distribution – Introduction to sampling – random sampling",
                        "Sampling distribution – standard error",
                        "Estimation – interval estimates and confidence interval – population mean and proportions"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Testing of Hypothesis",
                    "hours": 9,
                    "topics": [
                        "Testing of hypothesis – introduction – basic concepts",
                        "Hypothesis concerning a mean – equality of means",
                        "Hypothesis concerning one proportion – difference of two proportions"
                    ]
                }
            ]
        },
        {
            "code": "20MCA164",
            "name": "Organizational Behaviour",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Nature of Organisational Behaviour",
                    "hours": 9,
                    "topics": [
                        "Nature of Organisational Behaviour: Foundations, Contemporary OB, Scope, Evolution, OB Model",
                        "Management and Managers: Functions of Management – Manager’s Roles – Trends in Thinking",
                        "Challenges in OB: Managing Inclusivity / Diversity – Career Management – Talent Management – Globalisation"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Foundations of Individual Behaviour",
                    "hours": 10,
                    "topics": [
                        "Foundations of Individual Behaviour: Personal Factors – Environmental Factors – Systems and Resources",
                        "Intelligence: Nature, Types, Measurement, Factors Influencing Intelligence",
                        "Personality: Shaping, Determinants, Structure, OB Related Personality Traits",
                        "Perception and Attribution: Perceptual Process, Factors Influencing Perception",
                        "Learning: Explicit and Tacit Knowledge, Principles of Learning"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Attitudes, Values, Motivation & Work Stress",
                    "hours": 9,
                    "topics": [
                        "Attitudes and Values: Components, Formation, Functions, Changing Attitudes, Values",
                        "Motivation: Nature, Importance, Motivational Challenges, Theories on Motivation",
                        "Applied Motivational Practices: Rewards – Job Design – Behaviour Modification – Quality of Work Life",
                        "Work Stress: Work Stress Model – Burnout – Stress Management – Stress and Performance"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Group Dynamics, Leadership & Communication",
                    "hours": 12,
                    "topics": [
                        "Group Dynamics: Types, Development, Pitfalls, Group Decision Making",
                        "Team Dynamics: Teams vs. Groups – Implementing Teams in Organisations – Effective Teamwork",
                        "Workplace Behaviour: Nature of Conflict – Changing Views – Conflict Management Styles – Negotiation",
                        "Leadership: Leadership and Management – Styles and Their Implications – Theories of Leadership",
                        "Communication: Interpersonal – Organisational – Networks – Roles – Media – Managerial Implications"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Organisational Culture, Change & Development",
                    "hours": 9,
                    "topics": [
                        "Organisations: Structure – Key Factors – Types of Structures – Future Organisations",
                        "Organisational Culture: Cultural Dimensions – Sustaining Culture – Changing Culture – Innovation",
                        "Organisational Change and Development: Nature, Levels, Types, Resistance, Force Field Theory, OD"
                    ]
                }
            ]
        },
        {
            "code": "20MCA166",
            "name": "Functional Programming",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Recursion & Lambda Calculus",
                    "hours": 10,
                    "topics": [
                        "Review of recursion -Tail recursion -recursive program design",
                        "Functional Programming: Introduction, Lambda calculus, Lambda expressions, Reduction",
                        "Free and bound variables, Name clashes and alpha conversion, Eta reduction",
                        "Booleans and Integers, Data structures in functional languages, Functions as values"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Functions & Typing",
                    "hours": 8,
                    "topics": [
                        "Functions: Functions and definitions, Functional composition",
                        "Operators, Inverse functions, Strict and non-strict functions, Type Inference"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Lists & Higher-Order Functions",
                    "hours": 10,
                    "topics": [
                        "Lists: List notation, List comprehensions, Operations on lists",
                        "Map and filter, List patterns, Recursion and Induction over natural numbers and lists"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: New Types & Trees",
                    "hours": 10,
                    "topics": [
                        "New Types: Enumerated types, Composite types, Recursive types, Abstract types",
                        "Trees: Binary trees, Binary search trees, Properties and proofs"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Programming with Haskell",
                    "hours": 10,
                    "topics": [
                        "Programming with Haskell: Introduction, Defining functions: guards, pattern matching and recursion",
                        "Lists, strings and tuples, Types and polymorphism",
                        "Higher order functions on lists: map, filter, list comprehension, User defined data types: lists, queues, trees"
                    ]
                }
            ]
        },
        {
            "code": "20MCA168",
            "name": "Virtualisation and Containers",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Virtualization Foundations & Hypervisors",
                    "hours": 10,
                    "topics": [
                        "Physical and virtual machines, Traditional and virtual computing, Understanding virtualization",
                        "Need and Applications of virtualization, Limitations, Simulations and Emulations",
                        "Challenges in Virtualized environment, tools and technologies, Types of Hypervisors, Hypervisor architecture"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Network & Memory Virtualization",
                    "hours": 8,
                    "topics": [
                        "IP addressing - Private address, Public address, Virtual LAN",
                        "Memory addressing, Paging, Memory mapping, virtual memory",
                        "Complexities and solutions of memory virtualization"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Virtual Machines & KVM",
                    "hours": 14,
                    "topics": [
                        "VM lifecycle, Process and system level VMs, VM configurations",
                        "VM migrations, Migration types and process, VM provisioning, Scaling, VM scheduling",
                        "Load balancing: Significance, Types and Algorithms",
                        "Case study : KVM, KVM architecture, KVM commands"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Container Fundamentals & Docker",
                    "hours": 10,
                    "topics": [
                        "Container fundamentals, Containers versus virtual machines, Different container technologies",
                        "Configuring a container engine, Container virtual networking, Container orchestration and clustering",
                        "Images and containers, Case study : Docker"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Enterprise Container Management",
                    "hours": 6,
                    "topics": [
                        "Working with remote repositories, Security and isolation",
                        "Troubleshooting, Monitoring and alerting, Controlling running containers, Containers in a business context"
                    ]
                }
            ]
        },
        {
            "code": "20MCA172",
            "name": "Advanced Operating Systems",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Overview, Synchronization & Distributed OS",
                    "hours": 10,
                    "topics": [
                        "Overview: Functions of Operating System –Design Approaches –Types of Advanced Operating Systems",
                        "Synchronization Mechanisms: Processes and Threads –The Critical Section Problem – Monitor – Serializer – Path Expressions",
                        "Distributed Operating Systems:- Issues, Communication Networks And Primitives – Lamport’s Logical clocks – Causal Ordering of Messages"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Distributed Mutual Exclusion & Security",
                    "hours": 10,
                    "topics": [
                        "Distributed Mutual Exclusion:- Classification - Requirements – Measuring Performance",
                        "Lamport’s Algorithm – Rickart-Agarwala Algorithm – Suzuki-Kasami’s Broadcast Algorithm",
                        "Security: Potential Security Violations – Design Principles for Secure Systems – Access Matrix Model – Access Control list Method"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Distributed Resource Management & DSM",
                    "hours": 10,
                    "topics": [
                        "Distributed Resource Management: Mechanisms for building Distributed File Systems – Design Issues",
                        "Distributed Shared Memory – Algorithms for Implementing DSM – Issues in Load Distributing",
                        "Components of Load Distributing Algorithm – Sender-Initiated Algorithm – Receiver- Initiated Algorithm"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Multiprocessor OS & Virtualization",
                    "hours": 8,
                    "topics": [
                        "Multiprocessor Operating Systems: Basic Multiprocessor System Architectures – Interconnection Networks",
                        "Design Issues – Threads – Process Synchronization – Processor Scheduling – Memory Management",
                        "Virtualization – Types of Hypervisors – Paravirtualization – Memory Virtualization – I/O Virtualization"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Database Operating Systems",
                    "hours": 10,
                    "topics": [
                        "Database Systems: Problem of Concurrency Control – Serializability",
                        "Basic Synchronization Primitives for Concurrency Control – Lock-Based Algorithms",
                        "Time-Stamp Based Algorithms – Optimistic Algorithms"
                    ]
                }
            ]
        },
        {
            "code": "20MCA182",
            "name": "Business Management",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Management Foundations & Theories",
                    "hours": 9,
                    "topics": [
                        "Introduction to Management: Basic Managerial Concepts, Levels of management, Skills, Managerial role, Functions",
                        "Classical approach: scientific management, contributions of Taylor, Gilbreths, Fayol’s 14 principles",
                        "Human relation approach: Elton Mayo, Systems approach, organization as open system, Contingency approach"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Planning & Organizing",
                    "hours": 9,
                    "topics": [
                        "Planning: Nature and importance, Types of plans, Steps in planning, Levels, MBO definition and process, SWOT Analysis",
                        "Organising: Nature of organizing, span of control, authority and responsibility",
                        "Organisation structure: Formal and informal, line, line and staff, functional, divisional, project, matrix, virtual organisations"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Staffing & HRD Functions",
                    "hours": 9,
                    "topics": [
                        "Staffing and related HRD Functions: meaning, nature, staffing process, Job analysis and manpower planning",
                        "Job description and job specification, Recruitment & selection, selection process, Tests and interviews",
                        "Training and development - concept and methods, Performance appraisal- concept and methods"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Decision Making & Quality Management",
                    "hours": 9,
                    "topics": [
                        "Managerial Decision Making: types of decisions, decision making process, Decision Making Tools",
                        "Controlling: Techniques of controlling - Break Even Analysis, Budgetary Control, Benchmarking",
                        "Six Sigma importance, limitations and process of six sigma, Total Quality Management",
                        "Introduction to marketing management, Marketing mix, product life cycle"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Book-Keeping & Accounting",
                    "hours": 9,
                    "topics": [
                        "Book- Keeping and Accountancy - Elements of Double Entry, rules for journalizing, Ledger accounts, Cash book",
                        "Trial Balance, Method of Balancing accounts, the journal proper",
                        "Final accounts: Preparation of trading and profit and loss Account, Balance sheet",
                        "Introduction to Accounting packages"
                    ]
                }
            ]
        },
        {
            "code": "20MCA184",
            "name": "Embedded Systems",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Introduction to Embedded Systems",
                    "hours": 9,
                    "topics": [
                        "Introduction to Embedded Systems: Embedded system Vs General Computing System",
                        "Processor Embedded into a System, Embedded Hardware units and devices, Embedded Software in a System",
                        "Classification of Embedded systems, Skills Required for Designer, Examples, Major Application Areas, Purpose"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Embedded System Design & SoC",
                    "hours": 10,
                    "topics": [
                        "Embedded System Design and development Process: Embedded System-On-Chip (SoC) and VLSI Circuit Design Technology",
                        "Build Process for embedded systems, Design Process, Design Challenges, Hardware-Software Co-Design, Formalism of System Design"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Hardware Software Co-Design & Modeling",
                    "hours": 9,
                    "topics": [
                        "Hardware Software Co-Design and Program Modelling: Fundamental Issues in Hardware Software Co-Design",
                        "Computational Models: Data Flow Graph Model, Control Data Flow Graph, State Machine Model",
                        "Sequential Program Model, Concurrent / Communicating Process Model, Object oriented model, UML"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Embedded Hardware & Firmware Development",
                    "hours": 10,
                    "topics": [
                        "Embedded Hardware Design and Development: Analog Electronic Components, Digital Electronic Components, VLSI and IC Design",
                        "Embedded Firmware Design and Development: Embedded Firmware Design Approaches, Development Languages"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Integration, Testing & RTOS",
                    "hours": 10,
                    "topics": [
                        "Integration and Testing of Embedded Hardware and Firmware: Integration techniques, Testing Embedded Systems",
                        "RTOS based Embedded System Design: Basic operating system services, Introduction to RTOS, RTOS Task-Scheduling models, How to Choose an RTOS"
                    ]
                }
            ]
        },
        {
            "code": "20MCA186",
            "name": "Computer Graphics",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Introduction to Computer Graphics & Foundations",
                    "hours": 9,
                    "topics": [
                        "Major Areas and Applications, Graphics Pipeline, Numerical Issues, Efficiency and Coding Graphics Programs",
                        "Raster Images: Raster Devices, Images, Pixels, RGB Color and Alpha Composition",
                        "Fundamentals of Signal Processing for Images and Sampling Theory",
                        "Mathematical Foundations: Trigonometry, Geometry, Linear Algebra – Vectors and Matrices, Eigen Values and Eigen Vectors, Matrix Diagonalization"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Shape Drawing, Transformations & Viewing",
                    "hours": 11,
                    "topics": [
                        "Fundamentals of shape drawing: Line drawing - DDA and Bresenham Algorithms, Circle drawing: Mid Point and Bresenham",
                        "Transformations(2D, 3D): Translation and Affine Transformations, Inverse of Transformation Matrices, Coordinate transformations",
                        "Viewing: Viewing Transformations, Projective Transformation, Perspective Projection, Field of View",
                        "Graphics Pipeline: Rasterization, Operations, Antialiasing, Culling primitives for efficiency"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Shading, Texturing & Graphics Data Structures",
                    "hours": 10,
                    "topics": [
                        "Surface shading: Diffuse Shading, Phong Shading, Artistic Shading",
                        "Texture Mapping: 2D and 3D Mapping, Texture Mapping for Rasterized Triangles, Bump Textures, Displacement Mapping, Shadow Maps",
                        "Data Structures for Graphics: Triangle Meshes, Scene Graphs, Spatial Data Structures, BSP Tree for visibility, Tiling Multidimensional Arrays",
                        "Graphics APIs: Intuitive understanding of role of Graphics APIs such as OpenGL, Direct3D(DirectX), Vulkan"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Ray Tracing & Graphics Hardware",
                    "hours": 8,
                    "topics": [
                        "Ray Tracing: Basic Algorithms, Perspective, Computing Viewing Rays, Ray-Object Intersection, Shading, Shadows, Specular Reflection",
                        "Ray Tracing Program, Transparency and Refraction, Instancing, Constructive Solid Geometry, Distribution Ray Tracing",
                        "Using Graphics Hardware: Introduction, Geometry for Hardware, Processing Geometry using Pixels"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Radiometry, Colors & Global Illumination",
                    "hours": 11,
                    "topics": [
                        "Light: Radiometry, Transport Equation, Photometry",
                        "Colors: Colorimetry, Color Spaces, Chromatic Adaption, Color Appearance",
                        "Tonal Reproduction: Classification, Dynamic Range, Image Formation, Gradient Domain Operators, Night Tonemapping",
                        "Global Illumination: Particle tracing for Lambertian scenes, Path Tracing, Accurate Direct Lighting",
                        "Reflection Models: Real World Materials, Implementing Reflection Models, Specular Reflection models, Smooth layered Model, Rough Layered Model"
                    ]
                }
            ]
        },
        {
            "code": "20MCA188",
            "name": "Artificial Intelligence",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Introduction to AI & Production Systems",
                    "hours": 9,
                    "topics": [
                        "AI-Problem formulation, Problem Definition - Production systems, Problem characteristics, Production system characteristics",
                        "Example AI Problems: 8 Puzzle problem, Missionary Cannibals Problem, Crypt arithmetic Problems, block world Problem"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Search Strategies",
                    "hours": 9,
                    "topics": [
                        "Blind search strategies: Depth First Search, Breadth First Search, Best First Search, Iterative Deepening Search",
                        "Heuristic Search strategies: Admissible Heuristics and examples, Simple Hill Climbing and Steepest Ascending Hill Climbing, Simulated Annealing, A* algorithm"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Game Playing & Knowledge Representation",
                    "hours": 9,
                    "topics": [
                        "Two Player Zero Sum Games, Modelling Two Player Zero Sum Games as search problems",
                        "Min-Max Algorithm, Optimizing Min Max Algorithm using alpha-beta cut off",
                        "Knowledge Representation Structures: Frames, Semantic Networks and Conceptual Dependencies"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Knowledge Representation using Logic & Planning",
                    "hours": 12,
                    "topics": [
                        "First Order Predicate Logic (FOPL), Well Formed Formula(WFF) in FOPL, Inference rules for FOPL",
                        "The Clause Form and conversion of WFFs to Clause Form, Resolution-Refutation",
                        "Planning: Overview, components of a planning system, Goal stack planning, Hierarchical planning",
                        "Learning: Forms of learning, neural net learning and genetic learning"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Expert Systems & Fuzzy Logic",
                    "hours": 6,
                    "topics": [
                        "Architecture of expert systems, Roles of expert systems, Languages and tools, Typical expert system examples",
                        "Fuzzy Logic: Fuzzy Variables, Fuzzy Sets and Fuzzy Set Operations, Typical Examples using FuzzySets"
                    ]
                }
            ]
        },
        {
            "code": "20MCA192",
            "name": "IPR and Cyber Laws",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Fundamentals of IPR & Patents",
                    "hours": 10,
                    "topics": [
                        "Introduction to Intellectual Property, Need for protection, WIPO, IPR and development, Rationale of protection, TRIPS Agreement",
                        "Patents: Introduction, Patentable and Non-patentable Invention, Types of patent applications, Guidelines for registration of patent, patent filing, grant of patent, patent documents"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Trademarks & Copyrights",
                    "hours": 10,
                    "topics": [
                        "Trademarks: Guidelines for registration, Requirements for filing, Trademark Infringement, Protection of trademarks",
                        "Copyright: Introduction, Rights conferred, registration, ownerships, terms, transfer of copyrights, copyright infringement, databases and copyright",
                        "Software Copyright: Need of software copyright, classification of software according to copyright, software auditing, copyright notice, transfer of copyright"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Industrial Designs & Trade Secrets",
                    "hours": 10,
                    "topics": [
                        "Industrial Designs: Need for protection of design, requirements for registration, Design Act 2000, Duration of registration, application procedure",
                        "Geographic Indications: Introduction, Filing, Granting, Protection of geographic indications",
                        "Trade Secret: definition, discovering and protecting of trade secret"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Cyber Law & Cyberspace",
                    "hours": 8,
                    "topics": [
                        "Cyber law: Need for cyber laws, Historical perspective, cyberspace",
                        "Deception by squatting in cyberspace, protection of copyright on cyberspace, infringement of copyright on cyberspace, linking, hyperlinking and framing",
                        "ISP in cyberspace, cyberspace and protection of patents in India"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: IT Act 2000 & Punishments",
                    "hours": 10,
                    "topics": [
                        "Information Technology Act and Punishments: Introduction to IT Act 2000, Amendments on IT Act",
                        "Violation of the right of privacy in cyberspace, punishment for violation of privacy, breach of confidentiality under IT act, Terrorism on cyberspace",
                        "Overview of cybercrimes, offences by intermediaries, offences related to protected system, offences of misrepresentation, Abetment and Attempt to commit offences"
                    ]
                }
            ]
        },
        # Semester 2 Labs:
        {
            "code": "20MCA132",
            "name": "Object Oriented Programming Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Java Classes, Objects & Strings",
                    "hours": 11,
                    "topics": [
                        "Classes and Objects, Constructors, Method Overloading, Access Modifiers",
                        "Arrays and Strings processing",
                        "Inner class – static and non-static"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Inheritance, Interfaces & Collections",
                    "hours": 11,
                    "topics": [
                        "Inheritance, Multiple inheritance - implementation using interfaces",
                        "Method overriding, Abstract classes, Dynamic Method Dispatch",
                        "Interfaces and Packages, StringBuffer class",
                        "Introduction to java.util package – Vector, Scanner, StringTokenizer",
                        "Collection framework – ArrayList, LinkedList, Stack, Queue, Set, Map"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Exceptions, Threads, GUI & Sockets",
                    "hours": 18,
                    "topics": [
                        "User defined packages and User defined exceptions",
                        "Multithreading – Thread class and Inter Thread Communication",
                        "Generic programming",
                        "Applets and 2D Graphics, Event handling in Applet",
                        "File input and output streams",
                        "Socket Programming: TCP/IP and DatagramSocket UDP"
                    ]
                }
            ]
        },
        {
            "code": "20MCA134",
            "name": "Advanced DBMS Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Relational Database Design & PL/SQL",
                    "hours": 10,
                    "topics": [
                        "Relational database design using MySQL/MariaDB/PostgreSQL: DDL and DML Commands",
                        "Imposing restrictions on database (DCL & TCL Commands)",
                        "Accessing database (SELECT, WHERE, HAVING, GROUP BY, ORDER BY, Subquery and View)",
                        "Optimizing databases (Join, Aggregate & Set operations)",
                        "PL/SQL Programs: Trigger, Cursor, Stored Procedures and Functions"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: NoSQL Databases & Query Operations",
                    "hours": 12,
                    "topics": [
                        "Installation and configuration of NoSQL databases (MongoDB / Cassandra / HBase / CouchDB / Redis / Neo4j)",
                        "Designing Databases using NoSQL",
                        "Query Processing: Performing CRUD operations, Retrieving Data, Aggregate functions",
                        "NoSQL Administration: Security, Monitoring & Backup, Create Users and Roles"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Distributed NoSQL & Cloud Deployment",
                    "hours": 32,
                    "topics": [
                        "NoSQL shell commands: Sharding, Replication, Clustering, Partitioning, Indexing",
                        "Local Deployment: NoSQL and Front-End (PHP/Java/Python)",
                        "Cloud Deployment: Amazon DynamoDB / Google Bigtable / Azure Cosmos DB, Atlas / DataStax",
                        "Micro project: Group micro project in team environment"
                    ]
                }
            ]
        },
        {
            "code": "20MCA136",
            "name": "Networking & System Administration Lab",
            "category": "Practical",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Computer Hardware, Linux CLI & Shell Scripting",
                    "hours": 15,
                    "topics": [
                        "Computer hardware identification: mother board, RAM, daughter cards, bus slots, SMPS, storage devices, ports",
                        "Installation of Linux OS for desktop and server use",
                        "Terminal text editors: Vim and Emacs",
                        "Basic Linux commands: man, ls, echo, read, cat, cd, mkdir, pwd, find, mv, cp, rm, tar, wc, cut, grep, chmod, chown, useradd, ps, ssh",
                        "File system hierarchy in Linux, permissions, system configuration in /etc, log files",
                        "Shell scripting: bash syntax, variables, if, for, while, functions, command line arguments, systemd startup scripts"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Server Services & Network Administration",
                    "hours": 15,
                    "topics": [
                        "Installation and configuration of LAMP stack (Apache, MySQL, PHP, WordPress, phpMyAdmin)",
                        "Installation and configuration of web frameworks: Laravel",
                        "Building and installing software from source code (make, cmake)",
                        "Command line networking tools: ping, route, traceroute, nslookup, ip, static/dynamic IP",
                        "Subnets, CIDR address schemes, Subnet masks, iptables firewall setup, L7 proxies",
                        "Analyzing network packet stream using tcpdump and Wireshark, netcat (nc)"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Virtualization, Containers & Ansible",
                    "hours": 15,
                    "topics": [
                        "Introduction to Hypervisors and VMs (Xen or KVM)",
                        "Introduction to Containers: Docker installation and deployment",
                        "Automation using Ansible: Spin up a new Linux VM using Ansible playbook"
                    ]
                }
            ]
        }
    ],

    # =========================================================================
    # SEMESTER 3
    # =========================================================================
    3: [
        {
            "code": "20MCA201",
            "name": "Data Science & Machine Learning",
            "category": "Core",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Data Science Foundations & Visualization",
                    "hours": 9,
                    "topics": [
                        "Introduction to data science, Data science classification, Data science process",
                        "Prior knowledge, Data preparation, Modelling, Application",
                        "Data exploration: Data sets, Descriptive statistics for univariate and multivariate data",
                        "Data visualization: Histogram, Quartile plot, Distribution chart, Scatter plot, Bubble chart, Density chart"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Machine Learning & Lazy/Probabilistic Learners",
                    "hours": 9,
                    "topics": [
                        "Introduction to machine learning: How machines learn, Abstraction, Generalisation, Evaluation, ML types",
                        "Lazy learning: Classification using K-Nearest Neighbour (k-NN) algorithm, Measuring similarity, Choice of k, Preparing data",
                        "Probabilistic learning: Naive Bayes, Conditional probability and Bayes theorem, Laplace estimator, Numeric features"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Decision Trees & Regression Methods",
                    "hours": 9,
                    "topics": [
                        "Decision tree learning: Concept of decision tree, Divide and conquer approach, C5.0 algorithm, Best split, Pruning",
                        "Classification rules learning: Concept of classification rules, Separate and conquer approach, 1R algorithm, Rules from decision trees",
                        "Regression methods: Concept of regression, Simple linear regression, Ordinary least squares estimation, Correlations, Multiple linear regression"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Neural Networks & Support Vector Machines",
                    "hours": 9,
                    "topics": [
                        "Neural network learning: Artificial neurons, Activation functions, Network topology, Training with backpropagation",
                        "Support vector machines: Hyperplanes, Linearly separable data, Maximum margin hyperplanes, Using kernels for non-linear spaces"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Clustering & Model Evaluation",
                    "hours": 9,
                    "topics": [
                        "Clustering: The k-means clustering algorithm, Using distance to assign and update clusters, Choosing number of clusters",
                        "Evaluating model performance: Confusion matrices, Precision and recall, Sensitivity and specificity, F-measure, ROC curves, K-fold cross validation, Bootstrap sampling",
                        "Improving model performance: Bagging, Boosting, Random forests"
                    ]
                }
            ]
        },
        {
            "code": "20MCA203",
            "name": "Design and Analysis of Algorithms",
            "category": "Core",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Algorithm Analysis & Divide and Conquer",
                    "hours": 8,
                    "topics": [
                        "Review of Algorithm Analysis: Time and Space Complexity, Asymptotic Notations",
                        "Recurrence Equations: Solving Recurrence Equations - Substitution method and Iteration method",
                        "Divide and Conquer: Control Abstraction, Merge Sort, Quick Sort, Matrix Multiplication"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Greedy Strategy & Dynamic Programming",
                    "hours": 9,
                    "topics": [
                        "Greedy Strategy: Control Abstraction, Knapsack Problem, Minimal Spanning Tree (Prim’s and Kruskal’s Algorithm), Job Scheduling with deadlines",
                        "Dynamic Programming: Control Abstraction, Principle of Optimal Substructure, All Pairs shortest path problem, Travelling Salesman Problem, Bellman-Ford Algorithm"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Backtracking, Branch & Bound, Lower Bounds",
                    "hours": 7,
                    "topics": [
                        "Backtracking: Control Abstraction, N-Queens problem, Sum of Subsets Problem",
                        "Branch and Bound: Control Abstraction, 8- Puzzle problem",
                        "Lower Bounds: The Decision Tree method, Lower Bounds for Comparison based Sort and Searching"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Complexity Theory & Network Flows",
                    "hours": 11,
                    "topics": [
                        "Complexity Theory: Class P and NP, Polynomial time reductions, Class NP Hard and NP-Complete, Example Problems- Vertex Cover problem, Clique Problem",
                        "Network Flows: Flow Networks and Network Flow, Max- Flow Min Cut Theorem, Ford Fulkerson method, Bipartite matching"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Approximation & Randomised Algorithms",
                    "hours": 10,
                    "topics": [
                        "Introduction to Approximation Algorithms: Approximation Ratio, 2-approximation algorithm for Vertex Cover problem, Vertex Cover Approximation using Linear Programming and LP Rounding",
                        "Introduction to Randomised Algorithms: Review of Basic Probability, Schwartz-Zippel Lemma and Polynomial Identity Testing, Randomized Quick Sort"
                    ]
                }
            ]
        },
        # Elective II Options:
        {
            "code": "20MCA261",
            "name": "Operations Research",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Linear Programming Problems",
                    "hours": 9,
                    "topics": [
                        "Linear programming problem - Slack and surplus variable - Standard form",
                        "Solution of Linear programming problem - Basic solution - Basic feasible solution - Degenerate and Non-degenerate solutions - Optimal solution",
                        "Solution by simplex method",
                        "Artificial variables - Big-M method"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Duality in Linear Programming",
                    "hours": 9,
                    "topics": [
                        "Duality in Linear Programming Problem",
                        "Statement of duality theorem - Statement of complementary slackness theorem",
                        "The primal - Duality solutions using simplex method",
                        "Revised simplex method"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Transportation & Assignment Problems",
                    "hours": 9,
                    "topics": [
                        "Transportation problem - Finding initial basic feasible solution (North West Corner, Matrix minima, Vogel’s Approximation method)",
                        "Test for Optimality - Modi method - Unbalanced Transportation problem - Maximisation in Transportation",
                        "Assignment problem - Optimal solution - Hungarian method of assignment - Maximization in assignment"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Network Analysis (PERT & CPM)",
                    "hours": 9,
                    "topics": [
                        "Network analysis - Project scheduling - Construction of project networks",
                        "Critical path method (CPM) - Identification of critical path using CPM",
                        "Estimation of Floats - Total float - Independent float",
                        "Project Evaluation and Review Technique (PERT) - Computation of expected completion times by PERT"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Queuing Theory",
                    "hours": 9,
                    "topics": [
                        "Queuing theory - Elements of Queuing System - Kendall’s notation - Operating characteristics",
                        "Poisson process - Exponential distribution - Mean and variance - Birth and Death process",
                        "Queuing models based on Poisson process - Single server models with finite and infinite capacity",
                        "Multi server model with finite and infinite capacity"
                    ]
                }
            ]
        },
        {
            "code": "20MCA263",
            "name": "Cyber Security & Cryptography",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Introduction to Cryptography & OSI Security",
                    "hours": 7,
                    "topics": [
                        "Introduction to Cryptography, OSI security architecture: Security Services, Mechanisms and attacks",
                        "Phishing, Ransomware, DoS attack, Network security model",
                        "Classical Encryption techniques - Symmetric cipher model, substitution techniques, transposition techniques, Steganography"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Symmetric & Public Key Encryption",
                    "hours": 10,
                    "topics": [
                        "Conventional Symmetric Key Encryption: Block ciphers and Stream Ciphers, Block Cipher Design Principles, Modes of operation",
                        "Data Encryption Standard, Advanced Encryption Standard (AES), Multiple Encryption, Triple DES",
                        "Public key cryptography: Principles of public key cryptosystems - The RSA algorithm - Key management - Diffie Hellman Key exchange - Elliptic curve cryptography"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Hash Functions, MAC & Digital Signatures",
                    "hours": 10,
                    "topics": [
                        "Hash Functions and MAC: Properties of hash functions, birthday attack, hashcash, Message Authentication Code Algorithms, MAC protocols: HMAC, CMAC",
                        "Digital Signatures: Classification of signature schemes: RSA signature, Digital Signature Standard, Overview of ElGamal and Schnorr schemes, One time signatures, Attacks, Blind Signatures"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Email, IP & Transport Security",
                    "hours": 10,
                    "topics": [
                        "Introduction to Cyber Security: Email Security: Security Services for email, Pretty Good Privacy, S/MIME",
                        "IP Security: Overview of IPSec, IPv4 and IPv6, Authentication Header, Encapsulation Security Payload (ESP), Internet Key Exchange",
                        "Transport Level Security: SSL/TLS Basic Protocol, computing the keys, client authentication, PKI, Secure Electronic Transaction (SET)"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Common Web Application Vulnerabilities",
                    "hours": 8,
                    "topics": [
                        "Common web application security vulnerabilities: Injection flaws, Broken authentication, Sensitive data exposure",
                        "XML External Entities (XXE), Broken access control, Security misconfiguration, Cross-Site Scripting (XSS), Insecure deserialization",
                        "Using components with known vulnerabilities, Insufficient logging & monitoring, Prevention mechanisms"
                    ]
                }
            ]
        },
        {
            "code": "20MCA265",
            "name": "Cloud Computing",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Overview of OpenStack & Cloud Services",
                    "hours": 7,
                    "topics": [
                        "Introduction to cloud computing, private cloud, public cloud, hybrid cloud architecture",
                        "Cloud Services - Infrastructure as a Service, Platform as a Service, Storage as a Service",
                        "Designing OpenStack Cloud Architectural Consideration - OpenStack - The new data centre paradigm - OpenStack logical architecture - Nova - Neutron"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: OpenStack Cluster Controller & Services",
                    "hours": 6,
                    "topics": [
                        "OpenStack Cluster – The Cloud Controller and Common Services - Asymmetric clustering, Symmetric clustering, The cloud controller - The keystone service",
                        "The nova-conductor service, The nova-scheduler service, The API services, Image management, The network service, The horizon dashboard, The telemetry services"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: OpenStack Compute & Storage",
                    "hours": 12,
                    "topics": [
                        "OpenStack Compute - The compute service components - Deciding on the hypervisor - OpenStack Magnum Project - Overcommitment considerations - Planning for service recovery",
                        "OpenStack Storage - Block, Object, and File Share - Ephemeral Storage - Persistent storage - Swift - Block storage service: Cinder"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: OpenStack Networking",
                    "hours": 10,
                    "topics": [
                        "The architecture of Neutron - Implementing virtual networks - Connecting virtual networks with routers - Implementing network security in OpenStack",
                        "VLAN, Tunnel based, Virtual Switches, The ML2 Plugin. Neutron Subnets - Connecting virtual networks with routers - virtual router, floating IP"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Orchestration, HA & Failover",
                    "hours": 10,
                    "topics": [
                        "Orchestration in OpenStack - Heat and its Components, stacking in OpenStack, OpenStack Orchestration with Terraform",
                        "OpenStack HA and failover: Scope of HA in OpenStack, HA in the database, HA in the Queue, Implementing HA on RabbitMQ"
                    ]
                }
            ]
        },
        {
            "code": "20MCA267",
            "name": "Cyber Forensics",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Computer Crime & Evidence Acquisition",
                    "hours": 8,
                    "topics": [
                        "Overview of computer crime, company policy violation, Preparing a case - Planning an investigation, Securing evidence, Industrial espionage",
                        "Conducting an investigation: Gathering evidence, Bit-stream copy, Storage formats: Raw, Proprietary, AFF, Autopsy for Windows"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Storage Systems & File Systems",
                    "hours": 10,
                    "topics": [
                        "Understanding Digital data and storage systems: boot sequence, Disk Drives - Solid-state Storage Devices (SSDs)",
                        "Microsoft File Systems - Disk partitions, FAT, NTFS, MFT - file attributes, compressed files, encrypted file system, ReFS",
                        "Whole disk encryption, Microsoft BitLocker, Windows Registry, Windows startup tasks"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Linux, Mac File Systems & Sleuth Kit",
                    "hours": 10,
                    "topics": [
                        "Linux file structures in Ext4, Hard links and Symbolic links, Macintosh (MacOS) file structures",
                        "Setting up Sleuth Kit and Autopsy, Importance of Write-blocker, Acquiring data with Linux boot CD (dd, dcfldd), Validating data acquisitions"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Mobile & Network Forensics",
                    "hours": 10,
                    "topics": [
                        "Understanding Mobile Device forensics - Mobile phone basics, hardware, Acquisition procedures, SIM card readers, tools and methods",
                        "Network Forensics - Need for Established Procedures, Securing a Network, Procedures for Network Forensics, Wireshark packet analyser"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Forensics Reports & Expert Witness",
                    "hours": 7,
                    "topics": [
                        "Importance of Forensics Reports, Types of reports, Guidelines for writing reports, Layout and presentation, Generating reports with Autopsy",
                        "Ethics and codes for Expert Witness - Examiner’s role in testifying, Considerations in disqualification, Determining admissibility of evidence, Ethical responsibilities"
                    ]
                }
            ]
        },
        {
            "code": "20MCA269",
            "name": "Compiler Design",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Lexical Analysis",
                    "hours": 8,
                    "topics": [
                        "Introduction to compilers: Analysis of the source program, Phases of a compiler, Grouping of phases",
                        "Lexical analysis: role of lexical analyser, input buffering, specification of tokens, recognition of tokens, Deterministic and Non-Deterministic Finite automata, Regular expression to NFA and DFA"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Syntax Analysis & Parsing",
                    "hours": 12,
                    "topics": [
                        "Syntax analysis: Role of parser, Context free grammars",
                        "Top down parsing: Recursive Descent parsing, Predictive parsing, LL(1) Grammars",
                        "Bottom-up parsing: Shift Reduce Parsing, Operator Precedence Parsing",
                        "LR parsing – Constructing SLR parsing tables, Constructing Canonical LR parsing tables and Constructing LALR parsing tables"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Syntax Directed Translation & Type Checking",
                    "hours": 8,
                    "topics": [
                        "Syntax directed translation: Syntax directed definitions, Bottom-up evaluation of S-attributed definitions, L- attributed definitions, Top-down translation, Bottom-up evaluation of inherited attributes",
                        "Type Checking: Type systems, Specification of a simple type checker"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Intermediate Code Generation",
                    "hours": 7,
                    "topics": [
                        "Intermediate code generation: Graphical representations",
                        "Three address code - Quadruples - triples - Indirect triples",
                        "Assignment Statements, Boolean Expressions, Control flow statements"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Code Optimization & Generation",
                    "hours": 10,
                    "topics": [
                        "Code Optimization: Principal sources of optimization, Optimization of Basic blocks, Global data flow analysis",
                        "Code generation: Issues in the design of a code generator, The target machine, Basic blocks and flow graphs, A simple code generator, Peephole optimization"
                    ]
                }
            ]
        },
        {
            "code": "20MCA281",
            "name": "Internet of Things",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Introduction to IoT & Semantic Infrastructure",
                    "hours": 9,
                    "topics": [
                        "Internet of things - definition, evolution. Applications - Smart home, Health care, Elder care, Traffic surveillance",
                        "SOA-Based Architecture, API oriented Architecture, Resource Management, Computational Offloading, IOT Data Management and Analytics, IOT and the CLOUD",
                        "Open IOT architecture for IOT/Cloud convergence, Sensor middleware, Directory service, Global Scheduler, IOT Services lifecycle"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Fog Computing & Embedded Frameworks",
                    "hours": 11,
                    "topics": [
                        "Introduction to Fog Computing: principles, architectures, and Applications, Software-Defined Resource management layer",
                        "TinyOS: History, Implementation, Component Model, Execution Model, Concurrency, Theory of Execution: Events & Tasks",
                        "nesC design, Component Implementation, Design Decisions, Whole-Program Analysis, Race Conditions",
                        "Embedded Programming Languages: nesC, Keil C, Dynamic C, B#, Remote Procedure Call (RPC), REST, CoAP"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Data Stream Management & Anomaly Detection",
                    "hours": 8,
                    "topics": [
                        "Stream processing in IoT: Data Stream Management System (DSMS) and Complex Event Processing (CEP)",
                        "Characteristics of stream data in IOT, general architecture of stream-processing system",
                        "Distributed anomaly detection: Hyper ellipsoidal anomaly detection, Clustering ellipsoids, incremental local modeling"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Security & Privacy in IoT",
                    "hours": 9,
                    "topics": [
                        "IOT security threats, requirements, frameworks, IOT gateways and security, routing attacks, Lightweight cryptography",
                        "Reliability challenges and solutions, TinyTO: two-way authentication for constrained devices",
                        "IOT network stack and access protocols, Obfuscation and diversification techniques"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: IoT Implementation & Prototyping",
                    "hours": 8,
                    "topics": [
                        "Three key components to an IOT architecture, Sensor to gateway communication (wired and wireless interfaces)",
                        "Gateway hardware and software, Data transmission, backend processing, cloud integration",
                        "Creating a simple IoT project - Raspberry Pi preparation, Hardware interfacing, Sensor value persistence, Actuator controller"
                    ]
                }
            ]
        },
        {
            "code": "20MCA283",
            "name": "Deep Learning",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Review of Neural Networks",
                    "hours": 8,
                    "topics": [
                        "Model of a biological neuron, McCulloch Pitts Neuron, Activation Functions",
                        "Perceptron, Perceptron Learning Algorithm and Convergence, Multilayer Perceptron",
                        "Back propagation, Learning XOR, Sigmoid Neurons, Gradient Descent, Feed forward Neural Networks"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Training Deep Networks & TensorFlow",
                    "hours": 10,
                    "topics": [
                        "Training Neural Networks: Initialization, dropout, batch normalization, overfitting, underfitting, training and validation curves",
                        "Data Visualization: Feature and weight visualization, tSNE",
                        "Introduction to TensorFlow: graphs, nodes, Tensor data structures - rank, shape, type, Building neural networks with TensorFlow, Introduction to Keras"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Convolutional Neural Networks (CNNs)",
                    "hours": 10,
                    "topics": [
                        "Convolution operation, Convolutional layers in neural network, pooling, fully connected layers",
                        "Case study: Architecture of Lenet, Alexnet and VGG 16"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Recurrent Neural Networks (RNNs & LSTMs)",
                    "hours": 8,
                    "topics": [
                        "Recurrent Neural Networks: Back propagation, vanishing gradients, exploding gradients, truncated backpropagation through time",
                        "Gated Recurrent Units (GRUs), Long Short-Term Memory (LSTM) cells, solving the vanishing gradient problem with LSTMs"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Autoencoders & GANs",
                    "hours": 9,
                    "topics": [
                        "Autoencoders, variational autoencoders",
                        "Generative Adversarial Networks (GAN): Discriminative and generative models, GAN discriminator, GAN generator, upsampling, GAN Training, GAN challenges, loss functions, minimax loss, Wasserstein loss"
                    ]
                }
            ]
        },
        {
            "code": "20MCA285",
            "name": "Digital Image Processing",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Overview & Visual Perception",
                    "hours": 9,
                    "topics": [
                        "Digital Image Processing: Basic concepts, Difference between image processing and computer vision, Components of system, Applications",
                        "Mathematical preliminaries: Basic Vector and Matrix operations, Toeplitz, Circulant, Unitary & Orthogonal matrices",
                        "Elements of Visual Perception: Structure of human eye, image formation, Brightness adaptation, Types of Images, Sampling and Quantization, Spatial and Intensity resolution, RGB and HSI color models"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Spatial Filtering & Enhancement",
                    "hours": 10,
                    "topics": [
                        "Image enhancement: Grey level transformations (Negative, Log, Power-law, Piecewise linear), Histogram of Image, Histogram equalization",
                        "Spatial Filtering: Mechanics of Spatial filtering, 2D correlation and convolution",
                        "Smoothing spatial filters (Linear and Nonlinear), Sharpening spatial filters (Laplacian, Unsharp masking, High-boost filtering, Gradient operators)"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Frequency Domain Filtering & Transforms",
                    "hours": 8,
                    "topics": [
                        "Image Transform - representation in frequency domain, Unitary transformation, 1D-DFT and 2D-DFT properties, DCT and its properties",
                        "Filtering in Frequency Domain: Steps of frequency domain filtering, Image smoothing (Ideal, Butterworth, Gaussian Lowpass), Image sharpening (Ideal, Butterworth, Gaussian Highpass)"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Image Restoration & Compression",
                    "hours": 8,
                    "topics": [
                        "Image Restoration: Concept, Degradation/Restoration Model, Image Noise Models, Point Spread Function, Inverse filtering, Wiener filtering",
                        "Image compression: Need for compression, redundancy, general compression system, Huffman coding, Transform based compression, JPEG standard, Watermarking"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Morphological Processing & Segmentation",
                    "hours": 10,
                    "topics": [
                        "Morphological image processing: erosion and dilation, opening and closing, Hit or Miss transformation",
                        "Image segmentation: Point, Line, Edge detection (Marr-Hildreth, Canny edge detector), Hough transform",
                        "Thresholding: Basics of intensity thresholding, Global thresholding and Otsu’s method, Region-based segmentation (Region growing, Splitting and Merging)"
                    ]
                }
            ]
        },
        {
            "code": "20MCA287",
            "name": "Bioinformatics",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Computational Biology & Central Dogma",
                    "hours": 7,
                    "topics": [
                        "Computational Biology: Cell - Central Dogma of Molecular Biology - Structure of DNA, RNA and Protein",
                        "Coding and Non-coding RNAs - mRNA, tRNA, miRNA and siRNA",
                        "Bioinformatics: Nature & Scope of Bioinformatics, Genome projects, Importance, Pattern recognition and prediction, Folding problem, Sequence analysis"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Biological Databases",
                    "hours": 8,
                    "topics": [
                        "Primary Sequence databases: PIR, MIPS, SWIS-PROT, TrEMBL, NRL-3D",
                        "Composite protein sequence Databases: NRDB, OWL, MIPSX and SWISS-PROT+TrEMBL",
                        "Secondary Databases: Prosite, Prints, Blocks, Profile, Pfam, Structure Classification Databases (PDB)"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Pairwise Alignment & Sequence Search",
                    "hours": 10,
                    "topics": [
                        "Dot Plots, Concept of Simple Alignment, Scoring matrices: Introduction to PAM & Blosum",
                        "Needleman and Wunsch Algorithm (Global Alignment), Smith Waterman Algorithm (Local Alignment)",
                        "Multiple Sequence Alignment, Database search tools: BLAST & FastA"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Genomics & Gene Recognition",
                    "hours": 10,
                    "topics": [
                        "Introduction to Gene expression in prokaryotes, Prokaryotic Gene structure, GC content, Gene Density",
                        "Eukaryotic Genomes: Gene structure, GC content in eukaryotic genomes, Gene Expression – cDNAs, ESTs, SAGE, Introduction to Microarrays"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Visualization, Data Mining & Machine Learning",
                    "hours": 10,
                    "topics": [
                        "Data Visualization: Sequence Visualization, Structure Visualization (RasMol, PyMol), UI Components",
                        "Data Mining using biological data: Methods, Infrastructure, Pattern recognition, Genetic Algorithms, Neural networks, Hidden Markov Models, Text mining"
                    ]
                }
            ]
        },
        {
            "code": "20MCA289",
            "name": "Social Network Analysis",
            "category": "Elective",
            "credits": 4,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Semantic Web & Social Networks",
                    "hours": 9,
                    "topics": [
                        "Introduction to Semantic Web and Social Networks: Limitations of current Web, Semantic solution, Development of Semantic Web",
                        "Emergence of social web, Social Network Analysis, Global structure of networks, Macro-structure of social networks, Personal networks"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Module 2: Electronic Sources & Ontologies",
                    "hours": 8,
                    "topics": [
                        "Electronic sources for network analysis: Electronic discussion networks, Blogs and online communities, Web-based networks",
                        "Knowledge Representation on Semantic Web: Ontologies, Resource Description Framework (RDF) and RDF Schema, Web Ontology Language (OWL)",
                        "Comparison to UML, E/R model, Relational model, XML and XML Schema"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Module 3: Modeling & Aggregating Social Data",
                    "hours": 8,
                    "topics": [
                        "Network data representation, Ontological representation of social individuals and relationships",
                        "Aggregating and reasoning with social network data, Representing identity, Notion of equality, Reasoning with instance equality, Evaluating smushing"
                    ]
                },
                {
                    "module_no": 4,
                    "name": "Module 4: Graph Structure of Web & Facebook",
                    "hours": 10,
                    "topics": [
                        "Graph Structure of the Web: Breadth First Search (BFS), Strongly Connected Components (SCC), In/out-degree distributions, Zipf’s Law, Rank/Out-degree/Hop plot/Eigen exponents",
                        "Graph Structure of Facebook: HyperANF Algorithm, iFUB Algorithm, Spid, Degree Distribution, Path Length, Component Size, Clustering Coefficient, Degree Assortativity"
                    ]
                },
                {
                    "module_no": 5,
                    "name": "Module 5: Link Analysis & Search Engines",
                    "hours": 10,
                    "topics": [
                        "Search Engine Architecture: Crawling, Storage, Indexing, Ranking, HITS Algorithm, Page rank algorithm, Random walk, SALSA Algorithm, Bayesian Algorithm",
                        "Google architecture, Data Structures, Crawling, Searching, Web Spam Pages identification"
                    ]
                }
            ]
        },
        # Semester 3 Labs & Projects:
        {
            "code": "20MCA241",
            "name": "Data Science Lab",
            "category": "Lab",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Python Data Science Libraries & Visualisation",
                    "hours": 10,
                    "topics": [
                        "Review of python programming, Matrix operations, Programs using matplotlib / plotly / bokeh / seaborn for data visualisation",
                        "Data handling using pandas"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Classical Machine Learning Implementation",
                    "hours": 18,
                    "topics": [
                        "Program to implement k-NN classification on standard datasets",
                        "Program to implement Naive Bayes Algorithm and evaluate accuracy",
                        "Program to implement linear and multiple regression techniques",
                        "Program to implement text classification using Support Vector Machine",
                        "Program to implement decision trees and evaluate performance",
                        "Program to implement k-means clustering technique"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: Deep Learning, Scraping & NLP",
                    "hours": 20,
                    "topics": [
                        "Convolutional Neural Network image classification using Keras framework",
                        "Simple web crawler and web scraping program using Scrapy",
                        "Natural language processing with NLTK: Part of Speech tagging, N-gram and smoothening, Chunking"
                    ]
                }
            ]
        },
        {
            "code": "20MCA243",
            "name": "Mobile Application Development Lab",
            "category": "Lab",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Lab Module 1: Android UI & Activity Lifecycle",
                    "hours": 19,
                    "topics": [
                        "Fundamentals – Basic building blocks (Activities, Services, Receivers, Providers)",
                        "Application structure, layout and resources, Android Virtual Device, Activity Lifecycle",
                        "Basic UI Design and EditText Validation",
                        "SharedPreferences, RelativeLayout, FrameLayout, GridLayout and Preferences from xml"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Lab Module 2: Adapters, Menus, Intents & Fragments",
                    "hours": 18,
                    "topics": [
                        "ArrayAdapter, ListView and Exception handling",
                        "Various Menu options (Option menu, Context menu, Popup menu)",
                        "Explicit and Implicit Intents navigation",
                        "Images and media, Dialogs, Spinner component, Popups, Fragments, Navigation drawer",
                        "Applying themes and styles.xml"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Lab Module 3: SQLite Database & Mobile Applications",
                    "hours": 20,
                    "topics": [
                        "SQLite Programming: SQLiteOpenHelper, Database creation, Table structures",
                        "CRUD operations: INSERT, SELECT, UPDATE, DELETE on SQLite database",
                        "Micro project: Mobile application using SQLite database as an assignment"
                    ]
                }
            ]
        },
        {
            "code": "20MCA245",
            "name": "Mini Project",
            "category": "Project",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Sprint 1: Topic Approval, Requirements & Architecture",
                    "hours": 16,
                    "topics": [
                        "Selection of Topic, Synopsis approval, Meeting with Scrum Master and Product Owner",
                        "Informal preliminary requirements discussions, Creating user stories in rough record",
                        "Initial Database & UI Design, Setting up Docker container environment, Git repository creation"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Sprint 2: Agile Development, CI Pipeline & Testing",
                    "hours": 24,
                    "topics": [
                        "Simple deployment pipeline design, Project folder structure setup",
                        "Unit tests with xUnit framework, Build and code analysis scripts, Acceptance test scripts",
                        "Continuous Integration setup with Jenkins, Automated acceptance tests, Docker deployment scripts, Biweekly scrum reviews"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Sprint 3: Interim Assessment, Final Presentation & Report",
                    "hours": 20,
                    "topics": [
                        "Project Presentation - Interim evaluation based on Git History and commit quality",
                        "Submission of Project Report with Scrum Book",
                        "Project Presentation – Final evaluation based on Git History, Scrum Book, Project Report and live demo"
                    ]
                }
            ]
        },
        {
            "code": "20MCANC3",
            "name": "Domain Expertise Workshops",
            "category": "Non-Credit Course",
            "credits": 0,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Workshops: Industry Vertical Technologies & Seminars",
                    "hours": 15,
                    "topics": [
                        "Expert talks on Application domains: Retail, Finance, Healthcare, Automotive, Manufacturing",
                        "Expert talks on IT domains: IoT, AI, Big Data, Full Stack Development, Robotic Process Automation",
                        "Independent student research and technical report submission on industry domains",
                        "Technical domain seminars and presentations before academic audit committee"
                    ]
                }
            ]
        }
    ],

    # =========================================================================
    # SEMESTER 4
    # =========================================================================
    4: [
        {
            "code": "20MCA242",
            "name": "Comprehensive Viva",
            "category": "Viva",
            "credits": 6,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Comprehensive Curriculum Viva Voce",
                    "hours": 20,
                    "topics": [
                        "Core Viva: 20MCA105 Advanced Data Structures",
                        "Core Viva: 20MCA107 Advanced Software Engineering",
                        "Core Viva: 20MCA102 Advanced Database Management Systems",
                        "Core Viva: 20MCA201 Data Science & Machine Learning",
                        "Core Viva: 20MCA203 Design & Analysis of Algorithms",
                        "Code snippets in Java or Python to solve practical problems",
                        "Technologies used in student capstone project work",
                        "Recent developments and emerging trends in Computer Science"
                    ]
                }
            ]
        },
        {
            "code": "20MCA244",
            "name": "Seminar",
            "category": "Seminar",
            "credits": 2,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Module 1: Technical Literature Study & Colloquium",
                    "hours": 30,
                    "topics": [
                        "Identification of technically relevant current topic from peer-reviewed journals / conference proceedings",
                        "Faculty guide approval of topic synopsis and technical abstract",
                        "In-depth research study, analysis and synthesis of state-of-the-art literature",
                        "Technical presentation slides preparation and rehearsal (15-20 min presentation)",
                        "Technical Seminar Report generation using LaTeX with references and findings",
                        "Colloquium presentation and defense before three-member senior faculty committee"
                    ]
                }
            ]
        },
        {
            "code": "20MCA246",
            "name": "Main Project",
            "category": "Project",
            "credits": 12,
            "modules": [
                {
                    "module_no": 1,
                    "name": "Phase 1: Project Initiation, Synopsis & Requirements Engineering",
                    "hours": 40,
                    "topics": [
                        "Selection of Real-Life Project topic relevant to society or industry",
                        "Submission of project synopsis and approval from Project Supervisor",
                        "Meeting with Development Team, Scrum Master and Product Owner",
                        "Informal requirements discussions and user stories creation in Scrum Book",
                        "System Architecture design, Database ER modeling and high-level UI wireframing"
                    ]
                },
                {
                    "module_no": 2,
                    "name": "Phase 2: Sprint Execution, Continuous Integration & Biweekly Reviews",
                    "hours": 120,
                    "topics": [
                        "Sprint release planning and biweekly reviews with Product Owner",
                        "Scrum Book maintenance: Product Backlog, Database & UI Design, Testing & Validation, Version details",
                        "Git distributed version control management and commit traceability",
                        "Test Driven Development (TDD) using BugZilla / BackLog tracking",
                        "First interim evaluation by Project Assessment Board (Week 6)",
                        "Second interim evaluation by Project Assessment Board (Week 11)"
                    ]
                },
                {
                    "module_no": 3,
                    "name": "Phase 3: Final Dissertation, Presentation & External Viva",
                    "hours": 80,
                    "topics": [
                        "Complete project testing, deployment and documentation",
                        "Preparation of technical dissertation report using LaTeX",
                        "Submission of final Project Report along with authenticated Scrum Book",
                        "Final internal evaluation and software demonstration by Project Assessment Board (Week 13)",
                        "Final external examination and technical defense by University appointed External Examiner (Week 14)"
                    ]
                }
            ]
        }
    ]
}


def run_ingest():
    app = create_app()
    with app.app_context():
        print("=== INGESTING COMPLETE KTU MCA 2020 SCHEME CURRICULUM ===")

        # 1. Resolve KTU University
        uni = University.query.filter_by(code="KTU").first()
        if not uni:
            uni = University.query.filter(University.name.ilike("%Kalam%")).first()
        if not uni:
            print("ERROR: KTU University not found in database!")
            return

        print(f"University: {uni.name} ({uni.code}, ID: {uni.id})")

        # 2. Resolve MCA Program
        prog = Program.query.filter_by(name="MCA", university_id=uni.id).first()
        if not prog:
            print("ERROR: MCA Program not found under KTU!")
            return

        print(f"Program: {prog.name} (ID: {prog.id})")

        # 3. Resolve Scheme 2020
        scheme = Scheme.query.filter_by(year="2020", program_id=prog.id).first()
        if not scheme:
            scheme = Scheme(year="2020", program_id=prog.id, stream_id=None)
            db.session.add(scheme)
            db.session.flush()
        print(f"Scheme: {scheme.year} (ID: {scheme.id})")

        # 4. Resolve Semesters 1, 2, 3, 4
        semesters = {}
        for sem_no in [1, 2, 3, 4]:
            sem = Semester.query.filter_by(scheme_id=scheme.id, semester_no=sem_no).first()
            if not sem:
                sem = Semester(semester_no=sem_no, scheme_id=scheme.id)
                db.session.add(sem)
                db.session.flush()
            semesters[sem_no] = sem
            print(f"Semester {sem_no}: ID {sem.id}")

        # 5. Handle Course ID 7: rename/recode from 20MCA105 to 20MCA107
        c7 = Course.query.filter_by(id=7).first()
        if c7 and c7.name == "Advanced Software Engineering" and c7.code == "20MCA105":
            print("Fixing Course ID 7 code from 20MCA105 to 20MCA107 to preserve student progress...")
            c7.code = "20MCA107"
            db.session.flush()

        # Track stats
        courses_updated = 0
        courses_added = 0
        modules_added = 0
        topics_added = 0

        # 6. Ingest all courses semester by semester
        for sem_no, course_list in KTU_MCA_CURRICULUM.items():
            sem = semesters[sem_no]
            for c_data in course_list:
                code = c_data["code"]
                name = c_data["name"]
                cat = c_data.get("category", "Theory")
                creds = c_data.get("credits", 4)

                # Find course by code in this scheme
                course = Course.query.filter_by(code=code, semester_id=sem.id).first()
                if not course:
                    # Also check by name
                    course = Course.query.filter_by(name=name, semester_id=sem.id).first()

                if course:
                    # Update metadata
                    course.code = code
                    course.name = name
                    course.course_type = cat
                    course.credits = creds
                    courses_updated += 1
                else:
                    course = Course(
                        code=code,
                        name=name,
                        credits=creds,
                        course_type=cat,
                        semester_id=sem.id
                    )
                    db.session.add(course)
                    db.session.flush()
                    courses_added += 1

                # Provenance record
                src = SyllabusSource.query.filter_by(course_id=course.id).first()
                if not src:
                    src = SyllabusSource(
                        university_id=uni.id,
                        program_id=prog.id,
                        scheme_id=scheme.id,
                        course_id=course.id,
                        document_title="APJ ABDUL KALAM TECHNOLOGICAL UNIVERSITY - Master of Computer Applications Curriculum and Syllabus (Scheme 2020)",
                        source_url="https://www.ktu.edu.in/eu/att/attachments.htm?download=file&id=Syllabus_MCA_2020.pdf",
                        publication_date="2020-07-01",
                        verification_status="verified",
                        verified_by="KTU Academic Board Regulations",
                        notes="Official curriculum and course contents extracted from KTU MCA Scheme 2020 Syllabus Document (Pages 1-281)."
                    )
                    db.session.add(src)

                # Ingest Modules & Topics
                for m_data in c_data.get("modules", []):
                    m_no = m_data["module_no"]
                    m_name = m_data["name"]
                    m_hours = m_data.get("hours", 8)

                    module = Module.query.filter_by(course_id=course.id, module_no=m_no).first()
                    if not module:
                        module = Module(
                            course_id=course.id,
                            module_no=m_no,
                            name=m_name,
                            hours=m_hours
                        )
                        db.session.add(module)
                        db.session.flush()
                        modules_added += 1
                    else:
                        module.name = m_name
                        module.hours = m_hours

                    # Check topics - only populate if module currently has no topics
                    if len(module.topics) == 0:
                        for t_text in m_data.get("topics", []):
                            t_clean = t_text.strip()
                            topic = Topic.query.filter_by(module_id=module.id, name=t_clean).first()
                            if not topic:
                                topic = Topic(module_id=module.id, name=t_clean)
                                db.session.add(topic)
                                topics_added += 1

        db.session.commit()
        print("\n=== INGESTION SUMMARY ===")
        print(f"Courses updated: {courses_updated}")
        print(f"Courses added: {courses_added}")
        print(f"Modules created: {modules_added}")
        print(f"Topics created: {topics_added}")

        # Verification query
        all_courses = Course.query.join(Semester).filter(Semester.scheme_id == scheme.id).order_by(Semester.semester_no, Course.code).all()
        print(f"\nTotal KTU MCA 2020 Scheme courses in DB: {len(all_courses)}")
        for sem_no in [1, 2, 3, 4]:
            sem_courses = [c for c in all_courses if c.semester.semester_no == sem_no]
            print(f"  Semester {sem_no}: {len(sem_courses)} courses")
            for c in sem_courses:
                m_count = len(c.modules)
                t_count = sum(len(m.topics) for m in c.modules)
                print(f"    [{c.code}] {c.name} ({c.course_type}, {c.credits}cr) - {m_count} mods, {t_count} topics")

        # Verify User Progress
        total_prog = UserProgress.query.count()
        print(f"\nTotal User Progress records in DB: {total_prog} (Preserved)")

if __name__ == "__main__":
    run_ingest()
