from flask import render_template, request
from utils import match_resume_to_job
from database import get_all_resumes

def process_company(request):
    if request.method == "POST":
        job_description = request.form["job_description"]
        resumes = get_all_resumes()
        results = []

        for resume in resumes:
            match = match_resume_to_job(resume["text"], job_description)
            results.append((resume["name"], resume["email"], resume["phone"], match))

        sorted_results = sorted(results, key=lambda x: x[3], reverse=True)
        return render_template("results.html", results=sorted_results)
           

    return render_template("companies.html")

