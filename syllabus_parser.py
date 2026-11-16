"""
TrackMyCourse — Official Syllabus Document Extraction Engine
Supports PDF, DOCX, XLSX, CSV, and JSON curriculum documents.
Extracts structured academic hierarchies with full source provenance.
"""
import os
import re
import json
from datetime import datetime

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None

try:
    import openpyxl
except ImportError:
    openpyxl = None


class SyllabusParser:
    """
    Intelligent curriculum document parser that extracts hierarchical
    academic structures: University -> Program -> Scheme -> Semester -> Course -> Module -> Topic.
    """

    ALLOWED_EXTENSIONS = {"pdf", "docx", "xlsx", "csv", "json"}

    @staticmethod
    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in SyllabusParser.ALLOWED_EXTENSIONS

    @classmethod
    def parse_file(cls, file_path, file_type=None, metadata=None):
        if not file_type:
            file_type = file_path.rsplit(".", 1)[-1].lower()

        metadata = metadata or {}
        extracted_text = ""

        if file_type == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        elif file_type == "pdf":
            extracted_text = cls._extract_from_pdf(file_path)

        elif file_type == "docx":
            extracted_text = cls._extract_from_docx(file_path)

        elif file_type in ("xlsx", "csv"):
            return cls._extract_from_spreadsheet(file_path, file_type, metadata)

        else:
            raise ValueError(f"Unsupported document format: {file_type}")

        # Parse the structured text into hierarchical academic JSON
        return cls._structure_academic_text(extracted_text, metadata)

    @classmethod
    def _extract_from_pdf(cls, file_path):
        if not PdfReader:
            raise RuntimeError("pypdf is required to parse PDF curriculum documents.")
        reader = PdfReader(file_path)
        full_text = []
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n".join(full_text)

    @classmethod
    def _extract_from_docx(cls, file_path):
        if not docx:
            raise RuntimeError("python-docx is required to parse DOCX curriculum documents.")
        doc = docx.Document(file_path)
        lines = []
        for p in doc.paragraphs:
            if p.text.strip():
                lines.append(p.text.strip())
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    lines.append(row_text)
        return "\n".join(lines)

    @classmethod
    def _extract_from_spreadsheet(cls, file_path, file_type, metadata):
        courses_map = {}
        if file_type == "xlsx" and openpyxl:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                return {"semesters": []}
            header = [str(c).lower().strip() if c else "" for c in rows[0]]
            
            # Map column indices
            col_map = {
                "course_name": next((i for i, h in enumerate(header) if "course" in h or "subject" in h), 0),
                "course_code": next((i for i, h in enumerate(header) if "code" in h), None),
                "semester": next((i for i, h in enumerate(header) if "sem" in h), None),
                "module": next((i for i, h in enumerate(header) if "module" in h or "unit" in h), 1),
                "topic": next((i for i, h in enumerate(header) if "topic" in h or "content" in h), 2),
                "hours": next((i for i, h in enumerate(header) if "hour" in h), None),
                "credits": next((i for i, h in enumerate(header) if "credit" in h), None),
            }

            for row in rows[1:]:
                if not any(row):
                    continue
                c_name = str(row[col_map["course_name"]]).strip() if row[col_map["course_name"]] else "General Course"
                c_code = str(row[col_map["course_code"]]).strip() if col_map["course_code"] is not None and row[col_map["course_code"]] else ""
                sem_no = int(row[col_map["semester"]]) if col_map["semester"] is not None and str(row[col_map["semester"]]).isdigit() else int(metadata.get("semester_no", 1))
                mod_name = str(row[col_map["module"]]).strip() if row[col_map["module"]] else "Module 1"
                topic_name = str(row[col_map["topic"]]).strip() if row[col_map["topic"]] else ""
                hours = int(row[col_map["hours"]]) if col_map["hours"] is not None and str(row[col_map["hours"]]).isdigit() else 8

                if not topic_name:
                    continue

                if c_name not in courses_map:
                    courses_map[c_name] = {
                        "name": c_name,
                        "code": c_code,
                        "semester_no": sem_no,
                        "modules": {}
                    }
                
                if mod_name not in courses_map[c_name]["modules"]:
                    courses_map[c_name]["modules"][mod_name] = {
                        "name": mod_name,
                        "hours": hours,
                        "topics": []
                    }
                courses_map[c_name]["modules"][mod_name]["topics"].append(topic_name)

        # Build hierarchy
        semesters_dict = {}
        for c_data in courses_map.values():
            s_no = c_data["semester_no"]
            if s_no not in semesters_dict:
                semesters_dict[s_no] = {"semester_no": s_no, "courses": []}
            
            c_entry = {
                "name": c_data["name"],
                "code": c_data["code"],
                "credits": 4,
                "course_type": "Theory",
                "modules": list(c_data["modules"].values())
            }
            semesters_dict[s_no]["courses"].append(c_entry)

        return {
            "university": metadata.get("university_name", "Academic University"),
            "program": metadata.get("program_name", "Degree Program"),
            "scheme": metadata.get("scheme_year", "2024"),
            "semesters": list(semesters_dict.values()),
            "provenance": {
                "source_doc_title": metadata.get("document_title", os.path.basename(file_path)),
                "source_url": metadata.get("source_url", ""),
                "extracted_at": datetime.utcnow().isoformat()
            }
        }

    @classmethod
    def _structure_academic_text(cls, text, metadata):
        """
        Regex and rule-based parser that identifies Courses, Modules/Units,
        Hours, and Topics from text.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        current_course = None
        current_module = None
        courses = []
        
        default_sem = int(metadata.get("semester_no", 1))

        # Patterns
        course_pattern = re.compile(r"^(?:COURSE|SUBJECT|PAPER)?\s*([A-Z0-9]{5,10})?\s*[-:–]?\s*([A-Z][A-Za-z0-9\s&,/-]{4,80})$")
        module_pattern = re.compile(r"^(?:MODULE|UNIT)\s*([0-9IVXLCDM]+)[\s:–-]*(.*)$", re.IGNORECASE)
        hours_pattern = re.compile(r"(\d+)\s*(?:HOURS|HRS)", re.IGNORECASE)

        for line in lines:
            # Check for Module or Unit heading
            mod_match = module_pattern.match(line)
            if mod_match:
                mod_num = mod_match.group(1)
                mod_title = mod_match.group(2).strip()
                hours_match = hours_pattern.search(line)
                hours = int(hours_match.group(1)) if hours_match else 8

                if not current_course:
                    current_course = {
                        "name": metadata.get("course_name", "Curriculum Course"),
                        "code": metadata.get("course_code", ""),
                        "credits": 4,
                        "course_type": "Theory",
                        "modules": []
                    }
                    courses.append(current_course)

                current_module = {
                    "name": f"Module {mod_num}" + (f": {mod_title}" if mod_title else ""),
                    "module_no": int(mod_num) if mod_num.isdigit() else len(current_course["modules"]) + 1,
                    "hours": hours,
                    "topics": []
                }
                current_course["modules"].append(current_module)
                continue

            # Check for course heading if in all-caps or preceded by course code
            c_match = course_pattern.match(line)
            if c_match and len(line) < 90 and not mod_match and not line.startswith("-"):
                code = c_match.group(1) or ""
                name = c_match.group(2).strip()
                if any(w in name.upper() for w in ["DATA", "NETWORKS", "PROGRAMMING", "ENGINEERING", "MATHEMATICS", "SYSTEM", "INTELLIGENCE", "MANAGEMENT", "ALGORITHMS"]):
                    current_course = {
                        "name": name,
                        "code": code,
                        "credits": 4,
                        "course_type": "Theory",
                        "modules": []
                    }
                    courses.append(current_course)
                    current_module = None
                    continue

            # Otherwise, treat as topic under current module
            if current_module:
                # Clean bullet points, numbering, etc.
                cleaned = re.sub(r"^[\d\.\-\*•]+\s*", "", line).strip()
                if len(cleaned) > 3 and not hours_pattern.search(cleaned):
                    # Check if comma-separated subtopics
                    if len(cleaned.split(",")) > 3 and len(cleaned) > 60:
                        parts = [p.strip() for p in cleaned.split(",") if len(p.strip()) > 3]
                        current_module["topics"].extend(parts)
                    else:
                        current_module["topics"].append(cleaned)

        # Fallback if no modules detected
        if not courses:
            courses.append({
                "name": metadata.get("course_name", "Curriculum Document"),
                "code": metadata.get("course_code", ""),
                "credits": 4,
                "course_type": "Theory",
                "modules": [
                    {
                        "name": "General Syllabus Module",
                        "module_no": 1,
                        "hours": 10,
                        "topics": [l for l in lines if len(l) > 10][:20]
                    }
                ]
            })

        return {
            "university": metadata.get("university_name", "APJ Abdul Kalam Technological University"),
            "program": metadata.get("program_name", "MCA"),
            "scheme": metadata.get("scheme_year", "2021"),
            "semesters": [
                {
                    "semester_no": default_sem,
                    "courses": courses
                }
            ],
            "provenance": {
                "source_doc_title": metadata.get("document_title", "Official Syllabus Document"),
                "source_url": metadata.get("source_url", ""),
                "extracted_at": datetime.utcnow().isoformat(),
                "verification_status": "pending_verification"
            }
        }
