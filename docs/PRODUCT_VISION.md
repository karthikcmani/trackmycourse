# TrackMyCourse — Product Vision & Philosophy

## 1. Product Identity

- **Product Name**: TrackMyCourse
- **Category**: Unified Academic Progress Management & Learning Organization Platform
- **Audience**: University students, college scholars, educators, and academic administrators across multiple universities, faculties, and schemes.

---

## 2. Product Mission

Higher education curriculum structures are traditionally fragmented across dense syllabus PDFs, complex semester regulations, and opaque credit frameworks. Students frequently struggle to answer fundamental questions:

1. *What am I studying?*
2. *What subjects and courses do I have this semester?*
3. *What is the complete official syllabus?*
4. *Which specific modules and topics have I completed?*
5. *How much of my curriculum is remaining before examinations?*
6. *What should I study next to maintain learning consistency?*
7. *Where are my personal revision notes and learning resources?*
8. *How can I track my actual study hours over time?*

TrackMyCourse answers all nine questions on a single unified canvas.

---

## 3. Core Architectural Pillars

```
                                TrackMyCourse
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
  Verified Academic             Private Student                Academic Content
    Catalogue Space              Workspace                     Administration
• Multi-university           • Isolated progress            • Official document
  support                      records                        ingestion (PDF/DOCX)
• Reusable official          • Study task planner           • Syllabus review &
  syllabi                    • Logged study sessions          approval workflow
• Transparent primary        • Course notes & links         • Version & provenance
  source provenance          • Academic goals                 management
```

1. **Shared, Reusable Academic Hierarchy**:
   Academic entities (universities, programs, streams, schemes, semesters, courses, modules, topics) do not belong to an individual student. A verified syllabus is shared across students enrolled in that curriculum.

2. **Isolated Student Privacy**:
   Every student's topic completions, notes, study logs, and goals are strictly private. Progress updates never leak across accounts.

3. **Verifiable Primary Sources (No Mock Data)**:
   TrackMyCourse adheres to a zero-mock-data principle. Every academic syllabus maps directly to an official university document or Board of Studies regulation with recorded provenance.

4. **Extensible & Format-Agnostic Ingestion**:
   When an institution's curriculum is not yet indexed, administrators and students can upload official PDFs, DOCX files, or spreadsheets. The ingestion engine parses the document into a structured hierarchy for review and approval.
