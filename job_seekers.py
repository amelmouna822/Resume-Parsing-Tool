from flask import render_template, request, redirect, url_for
from utils import process_resume
from database import insert_resume
from database import verify_email_exists
def process_job_seekers(request):
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        uploaded_file = request.files["resume"]
        
        if uploaded_file and name and email and phone and password:
            if verify_email_exists(email):
                return render_template("job_seekers.html", error_message="البريد الإلكتروني مسجل مسبقًا.")
            resume_text = process_resume(uploaded_file)
            insert_resume(name, email, phone, password, resume_text)
            return redirect(url_for("success"))

    return render_template("job_seekers.html")
