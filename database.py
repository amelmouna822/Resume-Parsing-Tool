import sqlite3

def create_database():
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            text TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS job_offers (
            id INTEGER PRIMARY KEY,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            specialization TEXT,
            FOREIGN KEY(company_id) REFERENCES companies(id)
        )
    """)
    conn.commit()
    conn.close()

def insert_resume(name, email, phone, password, text):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("INSERT INTO resumes (name, email, phone, password, text) VALUES (?, ?, ?, ?, ?)", (name, email, phone, password, text))
    conn.commit()
    conn.close()

def insert_company(name, email, password):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("INSERT INTO companies (name, email, password) VALUES (?, ?, ?)",(name, email, password))
    conn.commit()
    conn.close()

def insert_job_offer(company_id, title, description, specialization=None):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("INSERT INTO job_offers (company_id, title, description, specialization) VALUES (?, ?, ?, ?)",(company_id, title, description, specialization))
    conn.commit()
    conn.close()

def get_all_resumes():
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("SELECT name, email, phone, password, text FROM resumes")
    data = [{"name": row[0], "email": row[1], "phone": row[2], "text": row[3]} for row in c.fetchall()]
    conn.close()
    return data

def get_company_offers(company_id):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM job_offers WHERE company_id=?", (company_id,))
    offers = c.fetchall()
    conn.close()
    return offers


def verify_resumes(email, password):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_company(email, password):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM companies WHERE email=? AND password=?", (email, password))
    company = c.fetchone()
    conn.close()
    return company


def verify_email_exists(email):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM resumes WHERE email = ?", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists   

create_database()

