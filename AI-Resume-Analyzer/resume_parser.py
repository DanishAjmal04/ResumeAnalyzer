# resume_parser.py
import io
import base64
import re
from pathlib import Path

import pandas as pd
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter

try:
    from pyresparser import ResumeParser
except Exception:
    ResumeParser = None


def pdf_reader(file_path):
    """Extract text from PDF file"""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text


def _extract_name(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:12]:
        if re.fullmatch(r"[A-Z][A-Za-z.' -]{2,50}", line) and len(line.split()) <= 4:
            if not re.search(r"resume|cv|summary|experience|skills|education|profile|contact", line, re.I):
                return line

    match = re.search(r"(?im)^(?:Mr|Ms|Mrs|Dr|Prof)\.?\s+[A-Z][A-Za-z.' -]+$", text)
    if match:
        return match.group(0).strip()

    return "Unknown"


def _extract_email(text: str):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0).strip() if match else ""


def _extract_mobile(text: str):
    match = re.search(r"(?:\+?\d[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})", text)
    return match.group(0).strip() if match else ""


def _extract_skills(text: str):
    lower_text = text.lower()
    keywords_file = Path(__file__).with_name("keywords.csv")
    skills = []

    if keywords_file.exists():
        try:
            df = pd.read_csv(keywords_file)
            keywords = df["keyword"].dropna().astype(str).tolist()
            for skill in keywords:
                normalized = skill.strip().lower()
                if normalized and normalized in lower_text:
                    skills.append(skill.strip())
        except Exception:
            pass

    if not skills:
        fallback_terms = [
            "python", "sql", "machine learning", "data science",
            "java", "javascript", "react", "docker", "aws",
            "communication", "problem solving"
        ]
        skills = [term for term in fallback_terms if term.lower() in lower_text]

    unique_skills = []
    seen = set()
    for skill in skills:
        key = skill.lower()
        if key not in seen:
            unique_skills.append(skill)
            seen.add(key)
    return unique_skills


def _extract_resume_data_from_text(text: str):
    text = text or ""
    return {
        "name": _extract_name(text),
        "email": _extract_email(text),
        "mobile_number": _extract_mobile(text),
        "skills": _extract_skills(text),
        "no_of_pages": max(1, round(len(re.findall(r"\S+", text)) / 500)),
        "certifications": [],
        "summary": text[:500]
    }


def parse_resume(file_path):
    """Parse resume using pyresparser when available, with a fallback parser for broken installs."""
    if ResumeParser is not None:
        try:
            data = ResumeParser(file_path).get_extracted_data()
            if isinstance(data, dict) and data:
                return data
        except Exception as exc:
            print(f"pyresparser failed, using fallback parser: {exc}")

    try:
        text = pdf_reader(file_path)
    except Exception as exc:
        print(f"PDF reading failed in fallback parser: {exc}")
        text = ""

    return _extract_resume_data_from_text(text)


def show_pdf(file_path):
    """Display PDF in Streamlit"""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'