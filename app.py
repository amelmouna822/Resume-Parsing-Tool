from flask import Flask, render_template, request, redirect, url_for, session
from job_seekers import process_job_seekers
from login import process_login
from companies import process_company
from database import insert_company
from database import create_database, sqlite3
create_database()

app = Flask(__name__)
app.secret_key ='your_secret_key'
def get_db_connection():
    conn = sqlite3.connect('resumes.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def welcome():
    return render_template("index.html")  # صفحة الترحيب


@app.route("/condidat_options")
def condidat_options():
    return render_template("condidat_options.html")  # الصفحة الرئيسية

@app.route("/companies_option")
def companies_option():
    return render_template("companies_option.html")

@app.route("/login_companies", methods=["GET", "POST"])
def login_companies():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        company = conn.execute('SELECT * FROM companies WHERE email = ?', (email,)).fetchone()
        conn.close()
        if company and company['password'] == password:
          session['company_id'] = company['id']
          session['company_name'] = company['name']  # تخزين اسم الشركة
          return redirect(url_for('dashboard_companies')) 
        
    else:
            error = "Email or password is incorrect"
    return render_template("login_companies.html", error=error)

@app.route("/profile_companies")
def profile_companies():
    return render_template("profile_companies.html")

@app.route("/dashboard_companies")
def dashboard_companies():
    if 'company_id' not in session:
        return redirect(url_for('login_companies'))

    conn = get_db_connection()
    company_id = session['company_id']

    # استرجاع العروض السابقة
    offers = conn.execute(
        'SELECT * FROM job_offers WHERE company_id = ?', (company_id,)
    ).fetchall()

    all_results = []

    for offer in offers:
        # الحصول على السير الذاتية المتوافقة من قاعدة البيانات (مثال بسيط بالمطابقة الجزئية)
        matches = conn.execute('''
            SELECT r.name, r.email,
            ROUND((LENGTH(?) * 100.0) / LENGTH(r.text)) AS match_percent
            FROM resumes r
            WHERE  r.text LIKE '%' || ? || '%'
        ''', (offer['description'],  offer['description'])).fetchall()

        all_results.append({
            'id': offer['id'],  # مهم لحذف العرض
            'title': offer['title'],
            'description': offer['description'],
            'matching_cvs': matches
        })

    conn.close()
    return render_template("dashboard_companies.html", previous_offers=all_results, company_name="اسم شركتك")

@app.route("/signup_companies", methods=["GET", "POST"])
def signup_companies():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            insert_company (name, email, password)
            return redirect(url_for("login_companies"))
        except sqlite3.IntegrityError:
            error = "هذا البريد الإلكتروني مسجّل مسبقًا"

    return render_template("signup_companies.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    return process_login(request)
        

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM resumes WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template("profile.html", user=user)

@app.route("/edit_cv", methods=["GET", "POST"])
def edit_cv():
    if "user_id" not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        uploaded_file = request.files["resume"]
        if uploaded_file:
            from utils import process_resume
            resume_text = process_resume(uploaded_file)

            conn = get_db_connection()
            conn.execute("UPDATE resumes SET text = ? WHERE id = ?", (resume_text, session["user_id"]))
            conn.commit()
            conn.close()

            return redirect(url_for("profile"))  # العودة إلى الملف الشخصي بعد التعديل
        
    return render_template("edit_cv.html")


@app.route("/delete_cv", methods=["GET", "POST"])
def delete_cv():
    if "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]

    conn = get_db_connection()
    conn.execute("DELETE FROM resumes WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    session.pop("user_id", None)  # تسجيل خروج المستخدم

    return render_template("delete_cv.html")  # صفحة وداع بسيطة



@app.route("/job_seekers", methods=["GET", "POST"])
def job_seekers():
    return process_job_seekers(request)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/companies", methods=["GET", "POST"])
def companies():
    return process_company(request)  # معالجة البحث عن السير الذاتية

@app.route("/add_job_offer", methods=["POST"])
def add_job_offer():
    if 'company_id' not in session:
        return redirect(url_for('login_companies'))

    title = request.form["job_title"]
    description = request.form["job_description"]
    company_id = session['company_id']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO job_offers (company_id, title, description) VALUES (?, ?, ?)',
        (company_id, title, description)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard_companies'))

@app.route('/delete_offer', methods=['POST'])
def delete_offer():
    if 'company_id' not in session:
        return redirect(url_for('login_companies'))

    offer_id = request.form.get('offer_id')
    company_id = session['company_id']

    if not offer_id:
        return redirect(url_for('dashboard_companies'))

    conn = get_db_connection()
    # حذف العرض فقط إذا كان يخص الشركة الحالية
    conn.execute('DELETE FROM job_offers WHERE id = ? AND company_id = ?', (offer_id, company_id))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard_companies'))


@app.route("/logout")
def logout():
    session.pop("user_id", None)  # إزالة بيانات تسجيل الدخول من الجلسة
    return redirect(url_for("welcome"))  # أو يمكنك توجيهه إلى login مثلاً

if __name__ == "__main__":
    app.run()

