from flask import Flask, render_template, request, redirect, url_for, session
from database import create_database, sqlite3
create_database()
def get_db_connection():
    conn = sqlite3.connect('resumes.db')
    conn.row_factory = sqlite3.Row
    return conn

def process_login(request):
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM resumes WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and user['password'] == password:
          session['user_id'] = user['id']
          return redirect(url_for('profile'))
        else:
            error = "email or password in coract"
    return render_template("login.html", error=error)
        
