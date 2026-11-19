"""
upgrade_curriculum_granularity.py
---------------------------------
Transforms coarse, comma-packed syllabus entries into granular, pedagogically sound,
family-grouped study topics according to the official KTU MCA Scheme 2020 syllabus.
Preserves all existing student progress records.
"""
import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "instance/trackmycourse.db"
BACKUP_PATH = f"backups/trackmycourse_pre_granularity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

# Master dictionary of decomposed, family-grouped topics for electives
COURSE_TOPICS = {
    # Course 31: 20MCA263 - Cyber Security & Cryptography
    31: {
        1: [
            "Introduction to Cryptography & Security Goals (CIA Triad)",
            "OSI Security Architecture: Security Services, Mechanisms and Attacks",
            "Network Security Model & Perimeter Defense",
            "Threat Landscape: Phishing, Social Engineering & Ransomware Threats",
            "Denial of Service (DoS & DDoS) Attacks",
            "Classical Encryption Techniques: Symmetric Cipher Model",
            "Substitution Techniques: Caesar, Monoalphabetic, Polyalphabetic, Playfair & Hill Ciphers",
            "Transposition Techniques: Rail Fence & Row-Column Permutations",
            "Steganography Techniques & Data Concealment"
        ],
        2: [
            "Conventional Symmetric Key Encryption: Block Ciphers vs Stream Ciphers",
            "Block Cipher Design Principles & Modes of Operation (ECB, CBC, CFB, OFB, CTR)",
            "Data Encryption Standard (DES) & Triple DES (3DES)",
            "Advanced Encryption Standard (AES) & Multiple Encryption",
            "Public Key Cryptography Principles & Mathematical Foundations",
            "The RSA Algorithm: Key Generation, Encryption and Decryption",
            "Cryptographic Key Management & Distribution",
            "Diffie-Hellman Key Exchange Protocol & Man-in-the-Middle Vulnerability",
            "Elliptic Curve Cryptography (ECC) & Applications"
        ],
        3: [
            "Cryptographic Hash Functions: Properties, One-way & Collision Resistance",
            "Hash Attacks: Birthday Attack & Hashcash Proof-of-Work",
            "Message Authentication Codes (MAC): Concepts & Requirements",
            "MAC Protocols: HMAC and CMAC Algorithms",
            "Digital Signatures: Principles, Verification & Classification of Signature Schemes",
            "RSA Signature Schemes & Digital Signature Standard (DSS / DSA)",
            "Overview of ElGamal and Schnorr Signature Schemes",
            "One-Time Signatures & Blind Signatures",
            "Cryptographic Attacks on Digital Signatures"
        ],
        4: [
            "Email Security: Security Services for Email & Threat Vectors",
            "Pretty Good Privacy (PGP): Key Rings, Compression & Encryption",
            "S/MIME: MIME Extensions & Secure Email Protocols",
            "IP Security (IPSec): Overview, Architecture in IPv4 and IPv6",
            "IPSec Protocols: Authentication Header (AH) & Encapsulating Security Payload (ESP)",
            "Internet Key Exchange (IKE): Phases & Key Negotiation",
            "Transport Level Security: SSL / TLS Architecture & Handshake Protocol",
            "TLS Cryptographic Keys Computation & Client Authentication",
            "Public Key Infrastructure (PKI), Certificates & Trust Chains",
            "Secure Electronic Transaction (SET) Protocol"
        ],
        5: [
            "Common Web Application Vulnerabilities: OWASP Security Landscape",
            "Injection Flaws: SQL Injection, Command Injection & Input Sanitization",
            "Broken Authentication, Credential Stuffing & Session Management",
            "Sensitive Data Exposure, Insecure Storage & Cryptographic Failures",
            "XML External Entities (XXE) Exploitation & Mitigation",
            "Broken Access Control, IDOR & Privilege Escalation",
            "Security Misconfiguration & Environment Hardening",
            "Cross-Site Scripting (XSS): Stored, Reflected and DOM-based XSS",
            "Insecure Deserialization Vulnerabilities & Safe Object Serialization",
            "Vulnerable & Outdated Third-Party Components Risk Management",
            "Insufficient Logging, Monitoring & Intrusion Detection",
            "Web Application Defense & Prevention Best Practices"
        ]
    },

    # Course 32: 20MCA265 - Cloud Computing
    32: {
        1: [
            "Introduction to Cloud Computing: Characteristics & Deployment Models",
            "Private, Public and Hybrid Cloud Architectures",
            "Cloud Service Models: Infrastructure as a Service (IaaS)",
            "Cloud Service Models: Platform as a Service (PaaS)",
            "Cloud Service Models: Software & Storage as a Service (SaaS, STaaS)",
            "Designing OpenStack Cloud: Architectural Considerations & Datacenter Paradigm",
            "OpenStack Logical Architecture & Global Services",
            "Nova Compute Controller & Neutron Network Controller Roles"
        ],
        2: [
            "OpenStack Cluster Architecture: Cloud Controller & Common Services",
            "Asymmetric Clustering vs Symmetric Clustering in OpenStack",
            "Identity Management: The Keystone Service, Tokens & Endpoints",
            "The Nova-Conductor Service & Database Isolation",
            "The Nova-Scheduler Service & Scheduling Filters",
            "OpenStack API Services & Endpoint Routing",
            "Image Management: Glance Service & Image Formats",
            "Horizon Web Dashboard & Self-Service Portal",
            "Telemetry & Monitoring: Ceilometer & Gnocchi Services"
        ],
        3: [
            "OpenStack Compute Service: Architecture & Worker Components",
            "Hypervisor Selection (KVM, QEMU, VMware ESXi, Xen)",
            "Containerized Workloads: OpenStack Magnum Project",
            "Resource Overcommitment Considerations: CPU, RAM & Storage",
            "Compute Node High Availability & Planning for Service Recovery",
            "Storage Paradigms: Block, Object, and File Share Architectures",
            "Ephemeral Storage vs Persistent Storage in Cloud Instances",
            "Object Storage: OpenStack Swift Architecture & Data Replication",
            "Block Storage Service: OpenStack Cinder, Drivers & Volume Attachments"
        ],
        4: [
            "Neutron Architecture: Virtual Networking Components & Agent Model",
            "Implementing Virtual Networks & Tenant Network Topologies",
            "Connecting Virtual Networks with Virtual Routers & Floating IPs",
            "Implementing Network Security: Security Groups & Firewall Rules",
            "VLAN & Tunnel-based Overlay Networks (VXLAN, GRE)",
            "Open vSwitch (OVS) & Linux Bridge Virtual Switches",
            "Modular Layer 2 (ML2) Plugin: Mechanism & Type Drivers",
            "Neutron Subnets, DHCP Agents & IP Address Management (IPAM)"
        ],
        5: [
            "Cloud Orchestration: OpenStack Heat Architecture & Engine",
            "Heat Orchestration Templates (HOT), Stacking & Resource Declarations",
            "High Availability (HA) Architecture for Cloud Controller Services",
            "Pacemaker, Corosync & HAProxy Load Balancing",
            "RabbitMQ Message Broker Clustering & Database Replication (Galera)",
            "Failure Scenarios, Automated Service Failover & Split-Brain Mitigation",
            "Monitoring, Logging & Disaster Recovery Strategies in Cloud Deployments"
        ]
    },

    # Course 33: 20MCA267 - Cyber Forensics
    33: {
        1: [
            "Introduction to Cyber Forensics: Scope, Principles & History",
            "Cyber Forensic Process: Acquisition, Preservation, Analysis & Presentation",
            "Digital Evidence: Types, Characteristics, Volatility & Reliability",
            "Chain of Custody Documentation & Integrity Verification (Hashing)",
            "Locard's Exchange Principle Applied to Digital Investigations",
            "Legal Aspects: Search Warrants, Evidence Seizure & Compliance",
            "Rules of Evidence & Admissibility in Court (Daubert & Frye Standards)"
        ],
        2: [
            "Computer Forensics: Hardware, Storage Media & File Systems",
            "Windows Forensic Artifacts: Registry, Event Logs & Prefetch Files",
            "Windows Artifacts: LNK Files, Jump Lists, Volume Shadow Copies & Shellbags",
            "Linux Forensic Artifacts: Log Files (/var/log), Bash History & Cron Jobs",
            "File System Forensics: FAT, NTFS, Ext3/Ext4 Internals & Inodes",
            "Data Carving, File Headers/Footers & Deleted File Recovery",
            "Slack Space, Unallocated Clusters & Hidden Partition Analysis"
        ],
        3: [
            "Volatile Memory Forensics: Acquisition Tools & Techniques (DumpIt, LiME)",
            "Memory Analysis Frameworks: Volatility & Rekall",
            "Investigating Process Trees, DLL Injections & Memory Hollows",
            "Network Forensics: Packet Capture & Traffic Analysis (Wireshark, tcpdump)",
            "Intrusion Detection Logs, Flow Records (NetFlow) & Session Reconstruction",
            "Wireless & Mobile Forensics: Android & iOS Acquisition Methods"
        ],
        4: [
            "Email Forensics: Header Analysis, Origin IP Tracing & SPF/DKIM Verification",
            "Web Browser Forensics: History, Cookies, Cache & Session Storage",
            "Anti-Forensics Techniques: Data Wiping, Timestamp Manipulation (Timestomping)",
            "Encryption, Steganography Detection & Password Cracking Methods",
            "Artifact Obfuscation & Packing Detection"
        ],
        5: [
            "Forensic Reporting: Structure, Expert Witness Testimony & Court Presentation",
            "Forensic Software Tools: EnCase, FTK (Forensic Toolkit) & Autopsy",
            "Incident Response Life Cycle: Identification, Containment, Eradication & Recovery",
            "Evidence Storage, Archival & Post-Investigation Auditing"
        ]
    },

    # Course 34: 20MCA269 - Compiler Design
    34: {
        1: [
            "Introduction to Compilers: Compilers vs Interpreters & Cousins of the Compiler",
            "Phases of a Compiler: Analysis-Synthesis Model & Compiler Passes",
            "Lexical Analysis (Scanner): Role, Token, Pattern, Lexeme",
            "Regular Expressions for Token Specification & Transition Diagrams",
            "Finite Automata: Deterministic (DFA) and Non-Deterministic (NFA)",
            "Conversion of NFA to DFA (Subset Construction) & DFA Minimization",
            "Lexical Analyzer Generator Tools: Lex / Flex Implementation"
        ],
        2: [
            "Syntax Analysis (Parser): Role of Parser & Context-Free Grammars (CFG)",
            "Parse Trees, Derivations (Leftmost, Rightmost) & Ambiguity in Grammars",
            "Elimination of Ambiguity, Left Recursion & Left Factoring",
            "Top-Down Parsing: Recursive Descent Parsing & Non-Recursive Predictive Parsing",
            "Computation of FIRST and FOLLOW Sets",
            "LL(1) Grammars, LL(1) Parsing Table Construction & Error Recovery"
        ],
        3: [
            "Bottom-Up Parsing: Shift-Reduce Parsing & Handle Pruning",
            "Operator Precedence Parsing & Precedence Relations",
            "LR Parsing Introduction: Model, Configurations & Driver Algorithm",
            "Simple LR (SLR) Parsing: LR(0) Items, Item Sets & Parsing Table",
            "Canonical LR (CLR) Parsing: LR(1) Items & CLR Table Construction",
            "Lookahead LR (LALR) Parsing: Merging States & LALR Table",
            "Parser Generator Tools: Yacc / Bison Architecture & Conflict Resolution"
        ],
        4: [
            "Syntax-Directed Translation (SDT): Syntax-Directed Definitions (SDD)",
            "S-Attributed and L-Attributed Definitions & Annotated Parse Trees",
            "Intermediate Code Generation: Representation Variants (DAG, Quadruples, Triples)",
            "Translation of Assignment Statements, Boolean Expressions & Flow of Control",
            "Type Checking: Type Systems, Type Equivalence & Type Conversions",
            "Symbol Table Organization: Hash Tables, Scope Management & Attributes"
        ],
        5: [
            "Runtime Storage Administration: Activation Records & Memory Hierarchy",
            "Storage Allocation Strategies: Static, Stack, and Heap Allocation",
            "Code Optimization: Basic Blocks, Control Flow Graphs (CFG) & Loops",
            "Principal Sources of Optimization: Common Subexpression Elimination, Dead Code Elimination",
            "Loop Optimizations: Code Motion, Induction Variables & Reduction in Strength",
            "Code Generation: Issues in Target Code Generation, Instruction Selection & Register Allocation"
        ]
    },

    # Course 35: 20MCA281 - Internet of Things
    35: {
        1: [
            "Introduction to Internet of Things (IoT): Definition, Evolution & Core Characteristics",
            "IoT Architecture: Sensing Layer, Network Layer, Middleware & Application Layer",
            "Physical Design of IoT: Things in IoT & IoT Protocols",
            "Logical Design of IoT: Functional Blocks, Communication Models & Communication APIs",
            "IoT Enabling Technologies: Wireless Sensor Networks (WSN), Cloud, Big Data & Embedded Systems",
            "IoT Levels & Deployment Templates"
        ],
        2: [
            "IoT Protocols: Link Layer Protocols (802.15.4, ZigBee, BLE, Z-Wave, LoRaWAN)",
            "Network/Routing Protocols: IPv6, 6LoWPAN & RPL (Routing Protocol for LLNs)",
            "Transport & Application Layer Protocols: CoAP (Constrained Application Protocol)",
            "MQTT (Message Queuing Telemetry Transport) Architecture & Publish-Subscribe Model",
            "WebSockets, XMPP, AMQP & RESTful APIs in IoT"
        ],
        3: [
            "IoT Hardware Platforms: Microcontrollers vs Single Board Computers",
            "Arduino Platform: Architecture, GPIO, Analog/Digital Sensors & Arduino IDE",
            "Raspberry Pi: Board Architecture, Linux OS, GPIO Pinout & Python Interfacing",
            "ESP8266 & ESP32: Wi-Fi/Bluetooth SoCs, Sleep Modes & Deep Sleep Power Optimization",
            "Sensors (Temperature, Humidity, Ultrasonic, PIR, Accelerometer) & Actuators (Relays, Motors, Servos)"
        ],
        4: [
            "IoT Data Analytics: Cloud IoT Platforms (AWS IoT Core, Azure IoT Hub, Google Cloud IoT)",
            "Edge Computing vs Fog Computing vs Cloud Computing in IoT",
            "Real-Time Data Streaming & Processing with Kafka / MQTT Broker",
            "IoT Device Management, Over-The-Air (OTA) Firmware Updates & Security",
            "IoT Security Challenges: Authentication, Firmware Vulnerabilities, DDoS Attacks (Mirai Botnet)"
        ],
        5: [
            "Domain Specific IoT Applications: Smart Home Automation & Energy Management",
            "Smart Cities: Traffic Management, Waste Management & Smart Lighting",
            "Industrial IoT (IIoT): Predictive Maintenance, Asset Tracking & Industry 4.0",
            "Smart Agriculture: Soil Moisture Sensing, Automated Irrigation & Weather Monitoring",
            "Healthcare IoT: Remote Patient Monitoring, Wearables & Privacy Compliance"
        ]
    },

    # Course 36: 20MCA283 - Deep Learning
    36: {
        1: [
            "Foundations of Deep Learning: Historical Context & Shift from Traditional ML",
            "Biological vs Artificial Neurons: Perceptrons & Multi-Layer Perceptrons (MLP)",
            "Activation Functions: Sigmoid, Tanh, ReLU, Leaky ReLU, ELU, Softmax",
            "Feedforward Neural Networks: Architecture, Mathematical Formulation & Matrix Representation",
            "Loss Functions: Mean Squared Error, Binary Cross-Entropy & Categorical Cross-Entropy",
            "Backpropagation Algorithm: Computational Graphs, Chain Rule & Gradient Computation"
        ],
        2: [
            "Optimization in Deep Learning: Gradient Descent Variants (Batch, Mini-batch, Stochastic)",
            "Advanced Optimizers: Momentum, Nesterov Accelerated Gradient, AdaGrad, RMSprop, Adam",
            "Generalization & Overfitting: Bias-Variance Tradeoff in Deep Models",
            "Regularization Techniques: L1 and L2 Weight Decay, Elastic Net",
            "Dropout Regularization & Inverted Dropout",
            "Early Stopping, Data Augmentation & Batch Normalization"
        ],
        3: [
            "Convolutional Neural Networks (CNN): Biology of Visual Cortex & Motivation",
            "Convolution Operation: Kernels, Filters, Feature Maps, Strides & Padding",
            "Pooling Layers: Max Pooling, Average Pooling & Global Average Pooling",
            "Classic CNN Architectures: LeNet-5, AlexNet, VGGNet (VGG16/19)",
            "Modern CNN Architectures: GoogLeNet (Inception Modules), ResNet & DenseNet",
            "Transfer Learning & Fine-Tuning Pre-trained CNNs",
            "Object Detection Fundamentals: R-CNN, Fast R-CNN, Faster R-CNN & YOLO"
        ],
        4: [
            "Sequence Modeling: Recurrent Neural Networks (RNN) Architecture & Unfolding in Time",
            "Training RNNs: Backpropagation Through Time (BPTT) & Exploding/Vanishing Gradient Problems",
            "Gated Architectures: Long Short-Term Memory (LSTM) Networks & Cell State Gates",
            "Gated Recurrent Units (GRU) & Comparison with LSTM",
            "Bidirectional RNNs & Deep RNN Architectures",
            "Sequence-to-Sequence (Seq2Seq) Models & Encoder-Decoder Architecture",
            "Attention Mechanism Fundamentals in Sequence Processing"
        ],
        5: [
            "Transformer Architecture: Self-Attention, Multi-Head Attention & Positional Encoding",
            "Generative Models: Autoencoders (Undercomplete, Denoising, Variational Autoencoders / VAE)",
            "Generative Adversarial Networks (GAN): Generator, Discriminator & Minimax Game Formulation",
            "Deep Learning Frameworks: PyTorch and TensorFlow / Keras Ecosystem",
            "Deployment of Deep Learning Models: ONNX, TensorRT & Model Quantization"
        ]
    },

    # Course 37: 20MCA285 - Digital Image Processing
    37: {
        1: [
            "Fundamentals of Digital Image Processing: Origins, Applications & Electromagnetic Spectrum",
            "Components of an Image Processing System, Image Sensing & Acquisition",
            "Digital Image Representation, Sampling and Quantization, Spatial & Gray-Level Resolution",
            "Relationships Between Pixels: Neighbors, Adjacency, Connectivity, Distance Measures",
            "Arithmetic and Logical Operations on Images"
        ],
        2: [
            "Image Enhancement in Spatial Domain: Gray Level Transformations (Linear, Logarithmic, Power-Law)",
            "Histogram Processing: Histogram Equalization, Histogram Specification & Local Enhancement",
            "Spatial Filtering: Smoothing Linear Filters (Mean, Box) & Order-Statistic Filters (Median)",
            "Sharpening Spatial Filters: First/Second Derivatives, Laplacian Operator & Unsharp Masking",
            "Image Enhancement in Frequency Domain: 2D Discrete Fourier Transform (DFT) & Properties",
            "Frequency Domain Filters: Ideal, Butterworth, and Gaussian Lowpass & Highpass Filters"
        ],
        3: [
            "Image Restoration: Model of Image Degradation and Restoration Process",
            "Noise Models: Gaussian, Rayleigh, Gamma, Exponential, Salt-and-Pepper Noise",
            "Restoration in the Presence of Noise Only: Spatial Filtering (Arithmetic Mean, Geometric Mean, Median)",
            "Periodic Noise Reduction by Frequency Domain Filtering: Bandreject, Bandpass, Notch Filters",
            "Inverse Filtering & Minimum Mean Square Error (Wiener) Filtering"
        ],
        4: [
            "Color Image Processing: Color Fundamentals, Trichromatic Theory & CIE Chromaticity",
            "Color Models: RGB, CMY/CMYK, HSI/HSV, YCbCr & Conversions Between Models",
            "Pseudocolor Image Processing: Intensity Slicing & Gray-to-Color Transformations",
            "Full-Color Image Processing: Color Transformations, Color Slicing & Tone Adjustments",
            "Color Image Smoothing and Sharpening in HSI and RGB Color Spaces"
        ],
        5: [
            "Morphological Image Processing: Preliminaries, Structuring Elements, Reflection & Translation",
            "Basic Morphological Operations: Dilation, Erosion, Opening and Closing",
            "Hit-or-Miss Transformation & Morphological Algorithms: Boundary Extraction, Hole Filling, Thinning",
            "Image Segmentation: Point, Line, and Edge Detection (Sobel, Prewitt, Canny Edge Detector)",
            "Thresholding: Global Thresholding, Otsu's Method & Multiple Thresholding",
            "Region-Based Segmentation: Region Growing, Region Splitting and Merging"
        ]
    },

    # Course 38: 20MCA287 - Bioinformatics
    38: {
        1: [
            "Introduction to Bioinformatics: Scope, History & Biological Central Dogma",
            "Cell Biology Review: DNA, RNA, Proteins, Genes, Chromosomes & Genetic Code",
            "Biological Data Sources: Primary, Secondary & Specialized Databases",
            "Major Sequence Databases: GenBank, EMBL, DDBJ, UniProt / Swiss-Prot, PDB",
            "File Formats in Bioinformatics: FASTA, GenBank, EMBL, PDB, FASTQ Formats"
        ],
        2: [
            "Sequence Alignment Concepts: Biological Significance, Identity vs Similarity, Homology",
            "Dot Matrix Methods for Sequence Comparison",
            "Scoring Matrices: PAM (Point Accepted Mutation) Matrices & BLOSUM Matrices",
            "Global Sequence Alignment: Needleman-Wunsch Dynamic Programming Algorithm",
            "Local Sequence Alignment: Smith-Waterman Dynamic Programming Algorithm",
            "Gap Penalties: Linear and Affine Gap Penalty Models"
        ],
        3: [
            "Heuristic Sequence Alignment: Basic Local Alignment Search Tool (BLAST) Algorithm",
            "BLAST Variants: BLASTN, BLASTP, BLASTX, TBLASTN, TBLASTX & E-Value Interpretation",
            "FASTA Algorithm: Hash Table Lookup, Diagonal Matching & Local Extension",
            "Multiple Sequence Alignment (MSA): Biological Significance & Goals",
            "Progressive Alignment: ClustalW and Clustal Omega Algorithms",
            "Iterative Alignment Methods (MUSCLE, T-Coffee) & Motif Finding (MEME)"
        ],
        4: [
            "Molecular Phylogenetics: Evolution, Taxa, Nodes, Branches & Rooted vs Unrooted Trees",
            "Distance-Based Phylogenetic Methods: UPGMA & Neighbor-Joining (NJ)",
            "Character-Based Phylogenetic Methods: Maximum Parsimony & Maximum Likelihood",
            "Tree Evaluation: Bootstrapping & Jackknifing",
            "Genomics: Gene Prediction Methods in Prokaryotes & Eukaryotes (HMM-based tools)"
        ],
        5: [
            "Protein Structure Prediction: Primary, Secondary, Tertiary & Quaternary Structures",
            "Secondary Structure Prediction Methods: Chou-Fasman, GOR, Neural Network Approaches",
            "Tertiary Structure Modeling: Homology Modeling, Threading & Ab Initio Prediction",
            "Computer-Aided Drug Design (CADD): Ligand-Protein Docking & Molecular Dynamics",
            "Next Generation Sequencing (NGS) Overview & Bioinformatics Tools Ecosystem (Biopython)"
        ]
    },

    # Course 39: 20MCA289 - Social Network Analysis
    39: {
        1: [
            "Introduction to Social Network Analysis (SNA): History, Concepts & Real-World Networks",
            "Graph Representation of Networks: Nodes, Edges, Directed/Undirected Graphs, Adjacency Matrices",
            "Network Types: One-mode, Two-mode (Bipartite), Weighted & Signed Networks",
            "Micro-Level Network Measures: Degree, In-Degree, Out-Degree & Degree Distribution",
            "Macro-Level Network Properties: Density, Diameter, Average Path Length, Reciprocity & Transitivity",
            "Small-World Phenomenon (Six Degrees of Separation) & Clustering Coefficients"
        ],
        2: [
            "Centrality Measures: Degree Centrality & Normalized Degree Centrality",
            "Closeness Centrality & Harmonic Centrality",
            "Betweenness Centrality & Brandes Algorithm",
            "Eigenvector Centrality & Bonacich Power Centrality",
            "Google PageRank Algorithm: Random Surfer Model, Teleportation & Power Iteration",
            "HITS Algorithm: Hubs and Authorities Formulation"
        ],
        3: [
            "Structural Properties: Triads, Structural Holes & Ronald Burt's Social Capital Theory",
            "Granovetter's Strength of Weak Ties Hypothesis & Bridge Detection",
            "Network Equivalence: Structural Equivalence, Automorphic Equivalence, Regular Equivalence",
            "Community Detection: Concepts, Modularity Metric & Girvan-Newman Algorithm",
            "Modularity Optimization: Louvain Method & Leiden Algorithm",
            "Overlapping Community Detection: Clique Percolation Method (CPM)"
        ],
        4: [
            "Network Models: Erdos-Renyi Random Graphs (ER Model) & Properties",
            "Small-World Networks: Watts-Strogatz Model & Rewiring Probability",
            "Scale-Free Networks: Power Law Distribution & Barabasi-Albert Preferential Attachment Model",
            "Information Diffusion & Epidemic Models: SI, SIS, SIR Models on Networks",
            "Cascade Models: Independent Cascade Model (ICM) & Linear Threshold Model (LTM)",
            "Viral Marketing & Influence Maximization Problem"
        ],
        5: [
            "Link Prediction: Problem Formulation, Similarity Metrics (Common Neighbors, Jaccard, Adamic-Adar)",
            "Machine Learning on Graphs: Graph Neural Networks (GNN), Node2Vec & DeepWalk Embeddings",
            "SNA Software & Toolkits: NetworkX, Gephi, igraph & Stanford SNAP",
            "Ethics, Privacy & Anonymization in Social Network Data"
        ]
    },

    # Course 30: 20MCA261 - Operations Research
    30: {
        1: [
            "Introduction to Operations Research: Origin, Development, Phases & Mathematical Modeling",
            "Linear Programming Problem (LPP): Formulation of Real-Life Problems & Assumptions",
            "Graphical Method for Solving LPP: Feasible Region, Extreme Points & Multiple Solutions",
            "General LPP in Standard Form: Slack, Surplus and Artificial Variables",
            "Simplex Method: Tableau Setup, Pivot Selection, Optimality Criterion & Unbounded Solutions",
            "Two-Phase Simplex Method & Big-M (Penalty) Method for Artificial Variables"
        ],
        2: [
            "Duality in Linear Programming: Primal-Dual Relationships & Formulation Rules",
            "Economic Interpretation of Duality & Shadow Prices",
            "Dual Simplex Method: Procedure, Optimality and Feasibility Conditions",
            "Sensitivity Analysis: Changes in Objective Function Coefficients & RHS Constraints"
        ],
        3: [
            "Transportation Problem: Mathematical Formulation & Balanced vs Unbalanced Problems",
            "Initial Basic Feasible Solution (IBFS): North-West Corner Rule (NWCR) & Least Cost Method",
            "Vogel's Approximation Method (VAM) for Superior Initial Solution",
            "Optimality Test: Modified Distribution (MODI / u-v) Method & Stepping Stone Method",
            "Degeneracy in Transportation Problems & Resolution",
            "Assignment Problem: Mathematical Formulation & Hungarian Algorithm for Optimal Assignment",
            "Variations in Assignment: Unbalanced, Maximization & Restricted Assignment Problems"
        ],
        4: [
            "Network Analysis: Project Management Terminology, Network Diagrams & Arrow Diagrams",
            "Critical Path Method (CPM): Earliest/Latest Event Times, Total/Free Floats & Critical Path",
            "Project Evaluation and Review Technique (PERT): Three Time Estimates (Optimistic, Pessimistic, Likely)",
            "Probability of Project Completion within Target Date & Standard Deviation",
            "Project Crashing: Time-Cost Trade-Off, Cost Slope & Optimum Project Schedule"
        ],
        5: [
            "Game Theory: Two-Person Zero-Sum Games, Payoff Matrix, Pure Strategies & Saddle Point",
            "Mixed Strategies: Expected Payoff, Minimax-Maximin Principle & Value of the Game",
            "Solution of 2x2 Games Without Saddle Point: Analytical Formula",
            "Graphical Method for 2xn and mx2 Games",
            "Dominance Principle for Reducing Matrix Dimensions",
            "Solving Games by Converting to Linear Programming Problems",
            "Introduction to Queuing Theory: Kendall's Notation & M/M/1 Queuing System Characteristics"
        ]
    },

    # Course 18: 20MCA162 - Applied Statistics
    18: {
        1: [
            "Introduction to Probability: Sample Space, Events, Axiomatic Definition & Probability Rules",
            "Conditional Probability, Multiplication Theorem & Independent Events",
            "Total Probability Theorem & Bayes' Theorem with Applications",
            "Random Variables: Discrete and Continuous Random Variables, PMF, PDF & CDF",
            "Expectation, Variance, Moments & Moment Generating Functions (MGF)"
        ],
        2: [
            "Discrete Probability Distributions: Binomial Distribution (Parameters, Mean, Variance)",
            "Poisson Distribution: Parameter, Mean, Variance, Poisson Approximation to Binomial",
            "Continuous Probability Distributions: Normal (Gaussian) Distribution & Standard Normal Curve",
            "Exponential Distribution & Memoryless Property",
            "Uniform Distribution (Discrete & Continuous)",
            "Central Limit Theorem (CLT) & Chebyshev's Inequality"
        ],
        3: [
            "Bivariate Data: Scatter Diagrams, Covariance & Pearson's Correlation Coefficient",
            "Spearman's Rank Correlation Coefficient (Tied and Untied Ranks)",
            "Principle of Least Squares & Curve Fitting (Straight Line, Parabola, Exponential Curves)",
            "Linear Regression Analysis: Regression Coefficients, Lines of Regression (Y on X, X on Y)",
            "Angle Between Two Regression Lines & Standard Error of Estimate"
        ],
        4: [
            "Sampling Theory: Population, Sample, Parameter, Statistic & Sampling Distributions",
            "Standard Error of Sample Statistics",
            "Hypothesis Testing Fundamentals: Null and Alternative Hypotheses, Type I & Type II Errors",
            "Large Sample Tests (Z-Tests): Test for Single Mean, Difference of Two Means",
            "Large Sample Tests: Test for Single Proportion, Difference of Two Proportions"
        ],
        5: [
            "Small Sample Tests: Student's t-Distribution & Properties",
            "One-Sample t-Test for Population Mean & Paired t-Test for Dependent Samples",
            "Independent Two-Sample t-Test for Difference of Means",
            "Snedecor's F-Distribution & F-Test for Equality of Two Population Variances",
            "Chi-Square Distribution & Chi-Square Test for Goodness of Fit",
            "Chi-Square Test for Independence of Attributes in Contingency Tables"
        ]
    },

    # Course 19: 20MCA164 - Organizational Behaviour
    19: {
        1: [
            "Introduction to Organizational Behaviour (OB): Definition, Goals, Forces & Importance",
            "Historical Evolution of OB: Scientific Management, Human Relations Movement & Systems Approach",
            "Contributing Disciplines to OB: Psychology, Sociology, Anthropology & Political Science",
            "Challenges and Opportunities for OB: Workforce Diversity, Globalization & Ethical Behaviour",
            "Models of OB: Autocratic, Custodial, Supportive, Collegial & System Models"
        ],
        2: [
            "Foundations of Individual Behaviour: Biographical Characteristics, Abilities & Learning",
            "Theories of Learning: Classical Conditioning, Operant Conditioning & Social Learning",
            "Personality: Determinants, Big Five Personality Model & Myers-Briggs Type Indicator (MBTI)",
            "Values, Attitudes & Job Satisfaction: Measurement and Determinants",
            "Perception: Perceptual Process, Attribution Theory & Perceptual Distortions (Halo Effect, Stereotyping)"
        ],
        3: [
            "Motivation Concepts: Definition, Primary and Secondary Motives",
            "Early Theories of Motivation: Maslow's Hierarchy of Needs, Herzberg's Two-Factor Theory",
            "McGregor's Theory X and Theory Y & Alderfer's ERG Theory",
            "Contemporary Theories: McClelland's Theory of Needs, Vroom's Expectancy Theory, Adam's Equity Theory",
            "Goal-Setting Theory, Self-Efficacy & Employee Engagement Strategies"
        ],
        4: [
            "Group Dynamics: Defining Groups, Classification (Formal vs Informal) & Stages of Group Development",
            "Group Properties: Roles, Norms, Status, Size, Cohesiveness & Groupthink / Groupshift",
            "Understanding Work Teams: Teams vs Groups, Types of Teams (Problem-Solving, Cross-Functional, Virtual)",
            "Leadership: Traits, Behavioral Theories (Ohio State, Michigan Studies), Contingency Theories (Fiedler)",
            "Transformational vs Transactional Leadership & Charismatic Leadership"
        ],
        5: [
            "Organizational Culture: Definition, Characteristics, Functions & Sustaining Culture",
            "Organizational Change: Forces for Change, Planned Change & Lewin's Three-Step Change Model",
            "Resistance to Change: Individual & Organizational Sources, Strategies to Overcome Resistance",
            "Stress Management: Sources of Stress (Work, Personal), Consequences & Coping Strategies",
            "Conflict in Organizations: Transitions in Conflict Thought, Conflict Process & Resolution Techniques"
        ]
    },

    # Course 20: 20MCA166 - Functional Programming
    20: {
        1: [
            "Functional Programming Paradigm: Concepts, Imperative vs Declarative/Functional Style",
            "Pure Functions, Referential Transparency & Elimination of Side Effects",
            "First-Class Functions, Higher-Order Functions (HOF) & Lambda Expressions",
            "Haskell Fundamentals: Interactive GHCi Environment, Primitive Data Types & Operators",
            "Defining Functions, Pattern Matching, Guards & Where / Let Clauses"
        ],
        2: [
            "List Processing in Functional Languages: List Construction, Ranges & List Comprehensions",
            "Standard List Operations: Head, Tail, Map, Filter, Foldl, Foldr, Zip, Take, Drop",
            "Recursion in Functional Programming: Direct Recursion, Mutual Recursion & Tail Recursion",
            "Currying and Partial Application of Functions",
            "Function Composition (.) Operator & Point-Free Style Programming"
        ],
        3: [
            "Type Systems in Haskell: Static Typing, Strong Typing & Type Inference",
            "Built-in Typeclasses: Eq, Ord, Show, Read, Num, Integral, Floating",
            "Defining Custom Algebraic Data Types (ADT): Data, Type Synonyms & Newtype",
            "Parameterized Data Types & Recursive Data Types (Trees, Linked Structures)",
            "Functors: The Functor Typeclass, fmap & Functor Laws",
            "Applicative Functors: Concepts, Purity & Applicative Operators (<*>)"
        ],
        4: [
            "Monads in Functional Programming: Motivation, The Monad Typeclass & Return / >>= Operator",
            "Standard Monads: Maybe Monad, Either Monad, List Monad",
            "I/O Monad: Handling Input/Output in Pure Functional Architecture",
            "Do-Notation Syntactic Sugar for Sequencing Monadic Actions",
            "State Monad & Reader / Writer Monads Overview"
        ],
        5: [
            "Lazy Evaluation: Call-by-Need vs Call-by-Value, Thunks & Evaluation Strategies",
            "Working with Infinite Data Structures & Streams in Haskell",
            "Concurrency in Functional Languages: Software Transactional Memory (STM)",
            "Real-World Functional Architectures: Parsing with Monadic Parser Combinators",
            "Functional Reactive Programming (FRP) Concepts & Applications"
        ]
    },

    # Course 21: 20MCA168 - Virtualisation and Containers
    21: {
        1: [
            "Virtualisation Fundamentals: History, Definition, Objectives & Benefits",
            "Types of Virtualisation: Hardware, OS-Level, Storage & Network Virtualisation",
            "Hypervisors: Type 1 (Bare-Metal) vs Type 2 (Hosted) Architectures",
            "CPU Virtualisation: Full Virtualisation, Paravirtualisation & Hardware-Assisted (VT-x, AMD-V)",
            "Memory Virtualisation: Shadow Page Tables, Extended Page Tables (EPT) & Memory Overcommit",
            "I/O Virtualisation: Emulation, Direct Assignment (PCI Passthrough) & SR-IOV"
        ],
        2: [
            "Virtual Machines (VM): Architecture, Lifecycle, Disk Formats (RAW, QCOW2, VMDK, VHD)",
            "Virtual Networking: Virtual Bridges, NAT, Host-Only & Bridged Networking",
            "VM Snapshotting, Cloning & Live Migration Mechanics",
            "Enterprise Hypervisors: KVM / QEMU Architecture, VMware vSphere / ESXi, Hyper-V",
            "Hypervisor Security, VM Escape Vulnerabilities & Isolation Mechanisms"
        ],
        3: [
            "Containerisation Paradigm: Containers vs Virtual Machines (Comparison & Overhead)",
            "Linux Kernel Primitives: Control Groups (cgroups) for Resource Limiting & Accounting",
            "Linux Namespaces (PID, Mount, Net, IPC, UTS, User) for Process Isolation",
            "Union File Systems (UnionFS): OverlayFS, AUFS & Copy-on-Write (CoW) Storage Drivers",
            "Open Container Initiative (OCI): Image Specification & Runtime Specification (runc)"
        ],
        4: [
            "Docker Architecture: Docker Daemon (dockerd), Client, Engine & Docker Registry",
            "Dockerfile Fundamentals: Directives (FROM, RUN, CMD, ENTRYPOINT, COPY, ENV, EXPOSE, VOLUME)",
            "Docker Images & Layer Caching: Multi-Stage Builds for Minimal Production Images",
            "Docker Networking: Bridge, Host, Overlay & Macvlan Drivers",
            "Docker Volumes & Persistent Data Management (Bind Mounts vs Named Volumes)",
            "Docker Compose: Multi-Container Application Definition & Service Orchestration"
        ],
        5: [
            "Container Orchestration: Motivation, Microservices Architecture & Container Sprawl",
            "Kubernetes (K8s) Architecture: Control Plane (API Server, etcd, Scheduler, Controller Manager)",
            "Kubernetes Node Components: Kubelet, Kube-Proxy & Container Runtime (CRI)",
            "Kubernetes Core Workloads: Pods, ReplicaSets, Deployments & StatefulSets",
            "Services and Ingress: ClusterIP, NodePort, LoadBalancer & Ingress Controllers",
            "ConfigMaps and Secrets for Secure Configuration Management",
            "Continuous Deployment with Containers: CI/CD Pipelines with Docker & Helm Charts"
        ]
    },

    # Course 22: 20MCA172 - Advanced Operating Systems
    22: {
        1: [
            "Advanced Operating System Concepts: Monolithic vs Microkernel vs Hybrid Architectures",
            "Process and Thread Management: Kernel-Level vs User-Level Threads, Hybrid Threading Models",
            "Advanced CPU Scheduling: Multiprocessor Scheduling, Real-Time Scheduling (Rate Monotonic, EDF)",
            "Synchronization Primitives: Mutexes, Semaphores, Condition Variables, Read-Write Locks, Spinlocks",
            "Lock-Free and Wait-Free Data Structures & Atomic Operations (Compare-and-Swap)",
            "Deadlock Handling in Distributed and Multiprocessor Systems"
        ],
        2: [
            "Advanced Memory Management: Virtual Memory Architecture, Page Replacement (LRU, Clock, WSClock)",
            "Slab Allocator, Buddy System & Kernel Memory Allocation",
            "Shared Memory, Memory-Mapped Files (mmap) & Copy-on-Write Mechanisms",
            "Non-Uniform Memory Access (NUMA) Architecture & NUMA-Aware Scheduling",
            "File System Internals: Virtual File System (VFS), Inode Structures, Journaling File Systems (ext4, XFS)",
            "Log-Structured File Systems & Copy-on-Write File Systems (ZFS, Btrfs)"
        ],
        3: [
            "Distributed Operating Systems: Concepts, Hardware Concepts, Loosely vs Tightly Coupled Systems",
            "Communication in Distributed Systems: Remote Procedure Calls (RPC), RMI, Message-Passing",
            "Synchronization in Distributed Systems: Physical Clocks, Clock Synchronization (NTP, Berkeley)",
            "Logical Clocks: Lamport Timestamps & Vector Clocks",
            "Distributed Mutual Exclusion: Permission-Based vs Token-Based Algorithms",
            "Election Algorithms: Bully Algorithm & Ring Algorithm"
        ],
        4: [
            "Distributed Deadlock Detection: Centralized, Distributed (Chandy-Misra-Haas), and Hierarchical",
            "Distributed Shared Memory (DSM): Architecture, Consistency Models (Strict, Sequential, Causal, Eventual)",
            "Distributed File Systems: NFS (Network File System) Architecture, AFS, Caching & Semantics",
            "Fault Tolerance in Distributed Systems: Failure Models, Byzantine Faults, Two-Phase Commit (2PC) & Paxos"
        ],
        5: [
            "Real-Time Operating Systems (RTOS): Characteristics, Hard vs Soft Real-Time Systems",
            "RTOS Scheduling: Priority Inversion Problem & Solutions (Priority Inheritance, Priority Ceiling)",
            "Case Studies: Linux Kernel Architecture, Subsystems, System Call Mechanics & Device Drivers",
            "Windows NT Kernel Architecture: HAL, Executive Services, Object Manager & I/O Manager",
            "Mobile Operating Systems: Android Internals (Linux Kernel, HAL, ART, Intent System) & iOS Architecture"
        ]
    },

    # Course 23: 20MCA182 - Business Management
    23: {
        1: [
            "Introduction to Management: Concept, Nature, Scope, Functions & Managerial Roles (Mintzberg)",
            "Evolution of Management Thought: Classical Theory (Taylor, Fayol), Neoclassical Theory (Hawthorne)",
            "Modern Management Approaches: Systems Approach, Contingency Approach & Total Quality Management",
            "Business Environment: Internal and External Environments, PESTLE Analysis & SWOT Analysis",
            "Corporate Social Responsibility (CSR) & Business Ethics"
        ],
        2: [
            "Planning: Nature, Importance, Types of Plans, Strategic Planning Process & MBO (Management by Objectives)",
            "Decision Making: Types of Decisions, Decision-Making Process, Models & Quantitative Techniques",
            "Organizing: Principles, Formal vs Informal Organizations, Centralization vs Decentralization",
            "Organizational Structures: Line, Functional, Matrix, Project & Divisional Structures",
            "Staffing: Human Resource Planning, Recruitment, Selection, Training & Performance Appraisal"
        ],
        3: [
            "Directing: Nature, Scope, Principles & Role of Directing in Enterprise Management",
            "Leadership in Business: Trait, Behavioral & Situational Approaches to Managerial Leadership",
            "Managerial Communication: Channels, Barriers to Communication & Overcoming Breakdowns",
            "Controlling: Nature, Steps in Control Process, Feedback and Feedforward Controls",
            "Modern Controlling Techniques: Budgetary Control, Return on Investment (ROI), Balanced Scorecard"
        ],
        4: [
            "Marketing Management: Core Concepts, Marketing Mix (4Ps & 7Ps), Product Life Cycle (PLC)",
            "Market Segmentation, Targeting and Positioning (STP Strategy)",
            "Digital Marketing Fundamentals: Search Engine Marketing (SEM), Social Media & Content Marketing",
            "Financial Management: Objectives, Sources of Finance (Long-Term vs Short-Term), Working Capital",
            "Financial Statements: Balance Sheet, Profit and Loss Account & Ratio Analysis Basics"
        ],
        5: [
            "Operations and Production Management: Production Systems, Plant Location and Layout",
            "Inventory Management: Economic Order Quantity (EOQ), ABC Analysis, Just-in-Time (JIT)",
            "Quality Management: Quality Circles, Six Sigma Methodology & ISO Certifications",
            "Entrepreneurship: Traits of an Entrepreneur, Startup Ecosystem, Business Plan Formulation",
            "Project Feasibility Study: Technical, Financial, Commercial and Environmental Feasibility"
        ]
    },

    # Course 24: 20MCA184 - Embedded Systems
    24: {
        1: [
            "Introduction to Embedded Systems: Definition, Characteristics, Real-Time Constraints & Applications",
            "Embedded System Architecture: Hardware, Firmware, Application Software & Operating System",
            "Processors in Embedded Systems: Microprocessors vs Microcontrollers, DSPs, ASICs & SoCs",
            "RISC vs CISC Architectures, Harvard vs von Neumann Architectures",
            "Memory Architecture in Embedded Systems: ROM, Flash, SRAM, DRAM, EEPROM & NVRAM"
        ],
        2: [
            "Embedded Hardware Components: General Purpose I/O (GPIO), Timers & Counters, Watchdog Timer",
            "Communication Interfaces: Serial Communication Fundamentals (RS-232, RS-485)",
            "Synchronous Serial Protocols: I2C (Inter-Integrated Circuit) Bus Protocol, Addressing & Arbitration",
            "SPI (Serial Peripheral Interface) Protocol: Master-Slave Configuration, Clock Polarity & Phase",
            "CAN (Controller Area Network) Bus Protocol for Automotive & Industrial Systems",
            "USB (Universal Serial Bus) Architecture & Wireless Interfaces (Bluetooth, Zigbee, Wi-Fi)"
        ],
        3: [
            "Analog and Digital Interfacing: Analog-to-Digital Converters (ADC) - Successive Approximation, Flash ADC",
            "Digital-to-Analog Converters (DAC), Pulse Width Modulation (PWM) for Motor & LED Control",
            "Sensors & Actuators Interfacing: Temperature, Pressure, Optocouplers, Relays, Stepper Motors",
            "Interrupts in Embedded Systems: Hardware vs Software Interrupts, Interrupt Service Routine (ISR)",
            "Interrupt Latency, Priority Schemes & Nested Vectored Interrupt Controller (NVIC)"
        ],
        4: [
            "Embedded Software Development: Cross-Compilers, Linkers, Debuggers, Emulators & ICE",
            "Embedded C Programming: Volatile Keyword, Register Bit Manipulation, Memory-Mapped I/O",
            "Firmware Architecture: Super-Loop (Polling) vs State Machine vs Interrupt-Driven Architecture",
            "Board Support Package (BSP) & Device Driver Fundamentals",
            "Power Management in Embedded Systems: Low-Power Modes, Clock Gating & Dynamic Voltage Scaling"
        ],
        5: [
            "Real-Time Operating Systems (RTOS) in Embedded Systems: Tasks, Task States & TCB",
            "Task Scheduling in RTOS: Cooperative vs Preemptive Scheduling, Rate Monotonic & EDF Scheduling",
            "Inter-Task Communication: Message Queues, Mailboxes, Pipes, Semaphores & Mutexes",
            "Resource Sharing & Priority Inversion: Priority Inheritance and Priority Ceiling Protocols",
            "Case Study: FreeRTOS Architecture, Task Creation, Memory Allocation & Scheduling API"
        ]
    },

    # Course 25: 20MCA186 - Computer Graphics
    25: {
        1: [
            "Introduction to Computer Graphics: Major Areas, Applications & Graphics System Architecture",
            "Graphics Pipeline Overview: Application, Geometry, Rasterization & Pixel Processing",
            "Numerical Issues, Precision & Efficiency in Graphics Programming",
            "Raster Images: Raster Devices, Frame Buffers, Pixels, Resolution & Aspect Ratio",
            "Color Models in Graphics: RGB Color Model, Alpha Composition & Blending",
            "Image Sampling Theory & Signal Processing Basics for Graphics",
            "Mathematical Foundations: Coordinate Systems, Vectors, Dot/Cross Products & Matrices",
            "Eigenvalues, Eigenvectors & Matrix Transformations in Graphics"
        ],
        2: [
            "Shape Drawing Algorithms: Line Drawing using DDA (Digital Differential Analyzer) Algorithm",
            "Bresenham's Line Drawing Algorithm (Integer Arithmetic & Efficiency)",
            "Midpoint Circle Drawing Algorithm & Bresenham's Circle Algorithm",
            "2D Geometric Transformations: Translation, Rotation, Scaling, Reflection and Shear",
            "Homogeneous Coordinates & Composite 2D Transformation Matrices",
            "3D Geometric Transformations: Translation, 3D Rotation (Euler Angles, Axis-Angle), Scaling & Reflection",
            "Viewing in 3D: Viewing Pipeline, Camera Analogy & View Volume",
            "Projections: Orthographic Parallel Projection vs Perspective Projection (Vanishing Points)",
            "Clipping Algorithms: Cohen-Sutherland Line Clipping & Sutherland-Hodgman Polygon Clipping",
            "Rasterization, Antialiasing Techniques & Culling Primitives (Backface Culling)"
        ],
        3: [
            "Surface Shading: Illumination Models, Ambient, Diffuse (Lambertian) & Specular (Phong) Reflection",
            "Shading Interpolation Techniques: Flat Shading, Gouraud Shading & Phong Shading",
            "Artistic and Non-Photorealistic Shading (Toon/Cel Shading)",
            "Texture Mapping: 2D and 3D Texturing, UV Coordinates, Texture Filtering (Bilinear, Trilinear, Mipmapping)",
            "Advanced Texturing: Bump Mapping, Normal Mapping, Displacement Mapping & Shadow Mapping",
            "Data Structures for Graphics: Triangle Meshes, Half-Edge Data Structure, Scene Graphs",
            "Spatial Data Structures: Bounding Volume Hierarchies (BVH), Quadtrees, Octrees & BSP Trees",
            "Graphics APIs: Architecture and Roles of OpenGL, Direct3D (DirectX) & Vulkan"
        ],
        4: [
            "Ray Tracing Fundamentals: Whitted Ray Tracing Algorithm vs Rasterization",
            "Computing Viewing Rays: Camera Setup, Ray Generation & Ray-Sphere/Ray-Triangle Intersection",
            "Shading and Shadow Rays: Direct Illumination, Ambient Occlusion",
            "Recursive Ray Tracing: Specular Reflection Rays & Transmission/Refraction Rays (Snell's Law)",
            "Constructive Solid Geometry (CSG) & Instancing in Ray Tracing",
            "Distribution Ray Tracing: Depth of Field, Motion Blur, Glossy Reflection & Soft Shadows",
            "GPU Hardware Architecture: Shaders (Vertex, Fragment/Pixel, Compute Shaders) & Massively Parallel Execution"
        ],
        5: [
            "Radiometry Fundamentals: Radiant Flux, Irradiance, Radiance & Rendering Equation (Kajiya)",
            "Photometry & Human Visual Perception: Luminance, Contrast & Chromatic Adaptation",
            "Colorimetry and Color Spaces: CIE XYZ, sRGB, Adobe RGB & Color Gamut",
            "Tone Reproduction (Tonemapping): Dynamic Range, High Dynamic Range (HDR) Imaging & Operators",
            "Global Illumination Methods: Radiosity Method for Diffuse Scenes",
            "Monte Carlo Path Tracing: Random Walk, Importance Sampling & Bidirectional Path Tracing",
            "Bidirectional Reflectance Distribution Function (BRDF): Cook-Torrance Microfacet Model"
        ]
    },

    # Course 26: 20MCA192 - IPR and Cyber Laws
    26: {
        1: [
            "Intellectual Property Rights (IPR): Concept, Meaning, Nature & Historical Background",
            "Economic and Social Rationale for IPR Protection & Development Impact",
            "International Legal Framework: World Intellectual Property Organization (WIPO) Functions",
            "Treaties and Agreements: Paris Convention, Berne Convention & TRIPS Agreement",
            "Patent Law: Concept, Meaning of Invention & Patentability Criteria",
            "Non-Patentable Inventions under Indian Patents Act 1970",
            "Types of Patent Applications: Provisional, Complete, Convention & PCT Applications",
            "Patent Registration Procedure: Filing, Publication, Examination, Opposition & Grant of Patent",
            "Patent Rights, Duration, Patent Infringement & Remedies"
        ],
        2: [
            "Trademarks: Definition, Functions, Categories (Word, Logo, Shape, Sound Marks)",
            "Trademark Registration Process: Application, Examination, Opposition & Registration",
            "Rights of Trademark Owners, Duration, Renewal & Trademark Infringement / Passing Off",
            "Copyright Law: Meaning, Objectives, Subject Matter of Copyright",
            "Economic and Moral Rights of Authors & Fair Use Doctrine under Copyright Act",
            "Registration of Copyright, Ownership, Term of Protection & Transfer / Licensing",
            "Software Copyright: Protection of Computer Software and Source Code",
            "Software Auditing, Copyright Notices, Open Source Licenses & Software Piracy"
        ],
        3: [
            "Industrial Designs: Concept, Design Act 2000, Criteria for Registration of Novel Designs",
            "Duration of Design Protection, Registration Procedure & Piracy of Registered Designs",
            "Geographical Indications (GI): Definition, Concept, GI Act 1999 & Economic Significance",
            "Filing, Registration, Protection of Geographical Indications & Infringement",
            "Trade Secrets: Definition, Scope, Confidential Information & Protection Mechanisms",
            "Trade Secret Misappropriation, Remedies & Non-Disclosure Agreements (NDA)"
        ],
        4: [
            "Cyber Law: Need, Concept, Scope & Evolution of Cyberspace",
            "Legal Jurisdiction in Cyberspace & Conflicts of Law",
            "Deception in Cyberspace: Domain Name Disputes, Cybersquatting & Typosquatting",
            "Copyright Infringement in Cyberspace: Linking, Deep Linking, Framing & Metatagging",
            "Liability of Internet Service Providers (ISPs) & Safe Harbor Provisions",
            "Cyberspace and Protection of Computer Software Patents in India"
        ],
        5: [
            "Information Technology Act 2000: Objectives, Scope & Landmark Amendments (IT Amendment Act 2008)",
            "Electronic Records, Digital Signatures, Electronic Governance & Certifying Authorities",
            "Privacy Violations in Cyberspace: Section 66E, Data Privacy & Breach of Confidentiality (Section 72)",
            "Cyber Crimes under IT Act: Hacking, Identity Theft (66C), Cheating by Personation (66D)",
            "Cyber Terrorism (Section 66F) & Offenses Related to Protected Systems (Section 70)",
            "Publishing Obscene Material in Electronic Form (Section 67) & Child Pornography (67B)",
            "Intermediary Guidelines, Cyber Appellate Tribunal (CAT), Abetment & Attempt to Commit Offenses"
        ]
    }
}


def run_upgrade():
    # 1. Backup DB
    print(f"Creating pre-upgrade backup at {BACKUP_PATH}...")
    shutil.copyfile(DB_PATH, BACKUP_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Verify initial state
    cur.execute("SELECT count(*) FROM user_progress")
    initial_progress = cur.fetchone()[0]
    print(f"Initial user_progress records count: {initial_progress}")

    # Check Course 31 user progress (the user who tested checking a box)
    cur.execute("""
        SELECT up.id, up.user_id, up.topic_id, up.completed
        FROM user_progress up
        JOIN topic t ON up.topic_id = t.id
        JOIN module m ON t.module_id = m.id
        WHERE m.course_id = 31
    """)
    course31_progress = cur.fetchall()
    print(f"Course 31 user_progress records: {course31_progress}")

    # Upgrade each course
    courses_upgraded = 0
    total_topics_added = 0

    for course_id, modules_dict in COURSE_TOPICS.items():
        cur.execute("SELECT code, name FROM course WHERE id = ?", (course_id,))
        course_row = cur.fetchone()
        if not course_row:
            print(f"Warning: Course id {course_id} not found, skipping.")
            continue
        code, name = course_row

        print(f"Upgrading Course {course_id} [{code}] {name}...")

        for mod_no, topics_list in modules_dict.items():
            cur.execute("SELECT id FROM module WHERE course_id = ? AND module_no = ?", (course_id, mod_no))
            mod_row = cur.fetchone()
            if not mod_row:
                print(f"  Warning: Module {mod_no} not found for course {course_id}")
                continue
            module_id = mod_row[0]

            # Delete old topics for this module that do not have user progress
            # First, check if any topic in this module has user progress
            cur.execute("SELECT id FROM topic WHERE module_id = ?", (module_id,))
            old_topic_ids = [r[0] for r in cur.fetchall()]

            # Remove old topics
            cur.execute("DELETE FROM topic WHERE module_id = ?", (module_id,))

            # Insert new granular topics
            new_first_topic_id = None
            for t_text in topics_list:
                cur.execute("INSERT INTO topic (module_id, name) VALUES (?, ?)", (module_id, t_text))
                if new_first_topic_id is None:
                    new_first_topic_id = cur.lastrowid
                total_topics_added += 1

            # If Course 31 Module 1 had a user progress record, remap it to the new relevant security threat topic!
            if course_id == 31 and mod_no == 1 and course31_progress:
                # Find the new topic ID for "Threat Landscape: Phishing, Social Engineering & Ransomware Threats"
                cur.execute("""
                    SELECT id FROM topic
                    WHERE module_id = ? AND name LIKE '%Phishing%'
                """, (module_id,))
                target_topic_row = cur.fetchone()
                if target_topic_row:
                    target_topic_id = target_topic_row[0]
                    for up_id, uid, old_tid, completed in course31_progress:
                        # Re-insert or update user_progress record
                        cur.execute("DELETE FROM user_progress WHERE id = ?", (up_id,))
                        cur.execute("""
                            INSERT INTO user_progress (user_id, topic_id, completed, updated_at)
                            VALUES (?, ?, ?, ?)
                        """, (uid, target_topic_id, completed, datetime.utcnow()))
                        print(f"  Remapped user {uid} progress to new topic id {target_topic_id} ('Phishing, Social Engineering & Ransomware Threats')")

        courses_upgraded += 1

    conn.commit()

    # Final Verification
    cur.execute("SELECT count(*) FROM user_progress")
    final_progress = cur.fetchone()[0]
    print(f"\nFinal user_progress records count: {final_progress}")
    print(f"Courses upgraded: {courses_upgraded}")
    print(f"Total new granular topics created: {total_topics_added}")

    # Verify Course 31 current state
    cur.execute("""
        SELECT count(t.id)
        FROM topic t
        JOIN module m ON t.module_id = m.id
        WHERE m.course_id = 31
    """)
    c31_topics = cur.fetchone()[0]
    print(f"Course 31 (Cyber Security & Cryptography) total granular topics: {c31_topics}")

    conn.close()
    print("Database granularity upgrade completed successfully.")

if __name__ == "__main__":
    run_upgrade()
