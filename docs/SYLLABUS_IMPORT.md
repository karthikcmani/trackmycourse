# TrackMyCourse — Syllabus Ingestion & Document Extraction

## 1. Purpose

The Syllabus Ingestion Engine enables administrators and scholars to import official university curriculum documents into the academic catalogue without manual database entry.

---

## 2. Supported Formats

| Format | Parsing Engine | Extraction Strategy |
| :--- | :--- | :--- |
| **PDF** | `pypdf` | Full text extraction across document pages; regex segmentation into Course Codes, Module/Unit numbers, hours, and bulleted/numbered topic items. |
| **DOCX** | `python-docx` | Structured paragraph and table cell inspection, identifying Module and Topic delineations. |
| **XLSX / CSV** | `openpyxl` | Column mapping for Course Name, Course Code, Semester, Module Name, Hours, and Topic Content. |
| **JSON** | Native | Direct ingestion of standardized academic hierarchy JSON files. |

---

## 3. Two-Stage Extraction & Publishing Workflow

```
[Upload Document]
        │
        ▼
[SyllabusParser.parse_file]
        │
        ▼
[Saved in syllabus_import table (Status: 'preview')]
        │
        ▼
[Admin Review & JSON Tree Preview in Admin Portal]
        │
        ├─> [Reject / Edit]
        │
        ▼
[Approve & Publish]
        │
        ▼
[Idempotent DB Insert: University -> Program -> Scheme -> Semester -> Course -> Module -> Topic]
        │
        ▼
[SyllabusSource Provenance Citation Created]
```

1. **Extraction**:
   The uploaded document is saved to `instance/uploads/` with a sanitized timestamped name and parsed into a normalized academic hierarchy JSON dictionary.
2. **Review**:
   The extracted tree is presented in the Admin Portal for visual inspection before any database records are created.
3. **Publication**:
   Upon approval, the ingestion engine checks for existing entities and creates missing entities idempotently, attaching a verified `SyllabusSource` provenance citation.
