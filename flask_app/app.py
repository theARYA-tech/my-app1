from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import hashlib
from datetime import datetime, timedelta
import os
import random
import threading
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "secretkey"
app.permanent_session_lifetime = timedelta(days=30)

# ======================
# EMAIL CONFIG
# ======================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_16_digit_app_password'
app.config['MAIL_TIMEOUT'] = 10

mail = Mail(app)

# ======================
# DATABASE
# ======================
def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "app.db")
    return sqlite3.connect(db_path, check_same_thread=False)

def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        task TEXT,
        done INTEGER,
        due_date TEXT,
        priority TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        content TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ======================
# HELPERS
# ======================
def send_otp(email, otp):
    try:
        print("=" * 50, flush=True)
        print(f"📧 Sending OTP to: {email}", flush=True)
        print(f"🔑 OTP CODE: {otp}", flush=True)
        print("=" * 50, flush=True)

        msg = Message(
            "Your Verification Code",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Your verification code is: {otp}"

        mail.send(msg)

        print("✅ EMAIL SENT SUCCESSFULLY", flush=True)

    except Exception as e:
        print("❌ EMAIL ERROR:", e, flush=True)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ======================
# AUTH
# ======================
def check_password(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()
    return user

# ======================
# TASKS
# ======================
def get_tasks(user):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user=?", (user,))
    tasks = cursor.fetchall()
    conn.close()

    return [{
        "id": t[0],
        "task": t[2],
        "done": t[3],
        "due_date": t[4],
        "priority": t[5]
    } for t in tasks]

# ======================
# ROUTES
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = check_password(
            request.form.get("username"),
            request.form.get("password")
        )

        if not user:
            return jsonify(success=False, message="Invalid username or password")

        session["user"] = request.form.get("username")
        session.permanent = "remember" in request.form

        return jsonify(success=True)

    return render_template("login.html")

# ======================
# SIGNUP (SESSION-BASED OTP)
# ======================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    try:
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        print("🟡 SIGNUP:", username, email)

        if not username or not email or not password:
            return jsonify(success=False, message="All fields required")

        if len(password) < 6:
            return jsonify(success=False, message="Password too short")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM users WHERE username=? OR email=?",
            (username, email)
        )
        exists = cursor.fetchone()
        conn.close()

        if exists:
            return jsonify(success=False, message="Username or email already exists")

        otp = str(random.randint(100000, 999999))

        # STORE IN SESSION (FIXED)
        session['pending_signup'] = {
            "username": username,
            "email": email,
            "password": hash_password(password),
            "otp": otp,
            "expires": (datetime.now() + timedelta(minutes=5)).isoformat()
        }

        print("🔑 OTP GENERATED:", otp)  # ✅ DEBUG (IMPORTANT)

        send_otp(email, otp)

        return jsonify(success=True, verify=True)

    except Exception as e:
        print("❌ SIGNUP ERROR:", e)
        return jsonify(success=False, message=str(e))

# ======================
# RESEND OTP
# ======================
@app.route("/resend_otp", methods=["POST"])
def resend_otp():
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip()

        pending = session.get('pending_signup')

        if not pending or pending['email'] != email:
            return jsonify(success=False, message="Session expired")

        otp = str(random.randint(100000, 999999))
        pending['otp'] = otp
        pending['expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()

        session['pending_signup'] = pending

        print("🔁 RESENT OTP:", otp)  # ✅ DEBUG

        send_otp(email, otp)

        return jsonify(success=True)

    except Exception as e:
        print("❌ RESEND ERROR:", e)
        return jsonify(success=False, message="Failed to resend OTP")

# ======================
# VERIFY OTP
# ======================
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    email = request.form.get("email", "").strip()
    otp = request.form.get("otp", "").strip()

    print("🔍 VERIFY:", email, otp)

    pending = session.get('pending_signup')

    if not pending or pending['email'] != email:
        return jsonify(success=False, message="Session expired")

    if datetime.fromisoformat(pending['expires']) < datetime.now():
        session.pop('pending_signup')
        return jsonify(success=False, message="OTP expired")

    if pending['otp'] != otp:
        return jsonify(success=False, message="Invalid code")

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (pending['username'], pending['password'], email)
        )

        conn.commit()
        conn.close()

    except sqlite3.IntegrityError:
        return jsonify(success=False, message="Username or email already exists")
    except Exception as e:
        print("❌ DB ERROR:", e)
        return jsonify(success=False, message="Account creation failed")

    session["user"] = pending["username"]
    session.pop('pending_signup')

    print("✅ USER CREATED")

    return jsonify(success=True)

# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    tasks = get_tasks(user)

    total = len(tasks)
    completed = len([t for t in tasks if t["done"]])

    return render_template(
        "dashboard.html",
        user=user,
        tasks=tasks,
        total=total,
        completed=completed,
        pending=total - completed
    )

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)