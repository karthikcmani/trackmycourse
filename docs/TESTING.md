# TrackMyCourse — Quality Assurance & Testing Suite

## 1. Running Automated Tests

The automated test suite is powered by `pytest`. To execute all unit, integration, and regression tests:

```powershell
.\venv\Scripts\python.exe -m pytest tests/ -v
```

---

## 2. Test Coverage Matrix

| Test Function | Target Feature | Validation Criteria |
| :--- | :--- | :--- |
| `test_academic_dropdown_hierarchy` | Multi-tier Academic Selection | Verifies University $\rightarrow$ Program $\rightarrow$ Stream $\rightarrow$ Scheme $\rightarrow$ Semester $\rightarrow$ Course cascade returns valid JSON and handles optional streams. |
| `test_regression_ase_scenario` | KTU MCA S1 ASE Progress | Verifies that Advanced Software Engineering (`20MCA105`) loads 5 modules, 49 topics, and maintains ~88% completion (43 of 49 topics). |
| `test_regression_maths_and_s2_courses` | Pre-existing Course Data | Verifies that Maths S1 (78.4%), ADBMS S2 (50.8%), ACN S2 (34.1%), and AI S2 (79.2%) progress survived migration without corruption. |
| `test_zero_topic_course_summary` | Empty Syllabus Handling | Verifies that placeholder courses with 0 topics safely return `0.0%` rather than `NaN%`. |
| `test_user_progress_persistence_and_isolation` | Multi-User Data Isolation | Verifies topic completion persistence and validates that queries are scoped strictly to the authenticated user ID. |
| `test_study_planner_and_sessions` | Study Planner & Time Tracking | Verifies task creation, toggle status, and logging of study sessions. |
| `test_notes_resources_and_goals` | Student Notes, Resources & Goals | Tests creating topic-linked notes, saving resource links, and setting academic completion targets. |
| `test_authentication_login_flow` | Security & Session Management | Validates password hashing verification, invalid credential rejection, login redirects, and logout. |
| `test_syllabus_parser_extraction` | Ingestion Engine | Tests extraction of course codes, module headings, hours, and topics from curriculum text. |
