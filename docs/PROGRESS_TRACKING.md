# TrackMyCourse — Course Progress Tracking System

## 1. Core Principles

TrackMyCourse's progress tracking engine is designed around verifiable, topic-level completion:

1. **Course Progress Formula**:
   $$\text{Course Progress (\%)} = \text{round}\left(\frac{\text{Completed Topics}}{\text{Total Topics}} \times 100\right)$$

2. **Zero-Topic Edge Case Handling**:
   If a course currently has no registered topics in the syllabus ($\text{Total Topics} = 0$), the system strictly returns `0.0%` (or `0%`). The frontend never evaluates $0/0$ and never displays `NaN%`.

3. **Persistent Asynchronous Updates**:
   Toggling any topic checkbox immediately triggers an asynchronous `fetch` call to `POST /api/progress`, updating the database and logging the activity with an updated timestamp.

4. **Multi-User Isolation**:
   Student progress is keyed on `(user_id, topic_id)` with a unique constraint. Multiple students viewing the same course syllabus receive only their own completion states.

---

## 2. Regression Scenario Verification

The primary regression scenario mandated in the product specification was validated:

- **Hierarchy**: KTU $\rightarrow$ MCA $\rightarrow$ Scheme 2020 $\rightarrow$ Semester 1 $\rightarrow$ Advanced Software Engineering (Course Code: `20MCA105`). *(Note: Previously mislabeled as Scheme 2021 in early seed data; corrected to official KTU Scheme 2020 Regulations).*
- **Module Count**: 5 Modules
  - Module 1 (8 Hours): 9 topics
  - Module 2 (10 Hours): 10 topics
  - Module 3 (10 Hours): 10 topics
  - Module 4 (10 Hours): 10 topics
  - Module 5 (10 Hours): 10 topics
- **Total Topics**: 49 topics
- **Completed Topics for Scholar**: 43 completed topics
- **Verified Percentage**: $\text{round}\left(\frac{43}{49} \times 100\right) = 87.8\% \rightarrow \mathbf{88\%}$.

All regression criteria pass seamlessly in automated test suite `tests/test_trackmycourse.py`.
