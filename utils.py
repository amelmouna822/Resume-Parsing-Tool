from PyPDF2 import PdfReader


from PyPDF2 import PdfReader
import docx2txt

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def process_resume(file):
    if file.mimetype == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    else:
        return "صيغة الملف غير مدعومة!"

def match_resume_to_job(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    common_words = resume_words.intersection(job_words)
    match_percentage = (len(common_words) / len(job_words)) * 100 if job_words else 0
    return match_percentage

