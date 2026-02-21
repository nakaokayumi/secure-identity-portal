from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
import os
import psycopg2
from psycopg2.extras import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
# Change this secret key in your Render Environment Variables!
app.secret_key = os.environ.get('SECRET_KEY', 'super-secret-dev-key')
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# --- DATABASE CONNECTION ---
def get_conn():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        # This will show a clearer error in the logs if the variable is missing
        print("ERROR: DATABASE_URL environment variable is not set!")
        return None
    return psycopg2.connect(db_url, cursor_factory=DictCursor)

def log_event(event_name, email, ip):
    """Restored your audit logging system"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit_logs (event, email, ip) VALUES (%s, %s, %s)",
        (event_name, email, ip)
    )
    conn.commit()
    cur.close()
    conn.close()

def current_user_email():
    return session.get("user_email")

# --- CORE ROUTES ---

@app.route("/")
def home():
    return render_template("index.html") # This would show index.html first

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# --- AUTHENTICATION ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        
        pw_hash = generate_password_hash(password)
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                (full_name, email, pw_hash)
            )
            conn.commit()
            log_event("REGISTER_SUCCESS", email, request.remote_addr)
            flash("Account created! Please log in.")
            return redirect(url_for("login"))
        except Exception:
            conn.rollback()
            flash("That email is already registered.")
        finally:
            cur.close()
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "")

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            cur.execute("UPDATE users SET last_login = NOW() WHERE email = %s", (email,))
            conn.commit()
            session["user_email"] = user["email"]
            log_event("LOGIN_SUCCESS", email, request.remote_addr)
            cur.close()
            conn.close()
            return redirect(url_for("dashboard"))
        else:
            log_event("LOGIN_FAILED", email, request.remote_addr)
            cur.close()
            conn.close()
            flash("Invalid email or password.")
    return render_template("login.html")

# --- PASSWORD RESET & SECURITY ---

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        conn.close()
        if user:
            return redirect(url_for("reset_password", email=email))
        flash("If an account exists, a reset link has been sent.")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email") or request.form.get("email")
    if request.method == "POST":
        new_password = request.form.get("new_password")
        pw_hash = generate_password_hash(new_password)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (pw_hash, email))
        conn.commit()
        conn.close()
        log_event("PASSWORD_RESET_SUCCESS", email, request.remote_addr)
        flash("Password updated. Please log in.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", email=email)

# --- USER PROFILE & DASHBOARD ---

@app.route("/dashboard")
def dashboard():
    email = current_user_email()
    if not email:
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT full_name, last_login, created_at FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        session.clear()
        flash("Account not found. Please log in again.")
        return redirect(url_for("login"))

    cur.execute("""
        SELECT event, ip, created_at
        FROM audit_logs
        WHERE email = %s
        ORDER BY created_at DESC
        LIMIT 5
    """, (email,))
    logs = cur.fetchall()

    cur.close()
    conn.close()

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    return render_template(
        "dashboard.html",
        name=user["full_name"],
        greeting=greeting,
        last_login=user["last_login"],
        member_since=user["created_at"],
        logs=logs
    )

@app.route("/profile")
def profile():
    email = current_user_email()
    if not email: return redirect(url_for("login"))
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT full_name, email, created_at FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("profile.html", user=user)

# --- ACCOUNT DELETION ---

@app.route("/delete_account", methods=["POST"])
def delete_account():
    email = current_user_email()
    if not email: return redirect(url_for("login"))
    
    log_event("ACCOUNT_DELETED", email, request.remote_addr)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email = %s", (email,))
    conn.commit()
    conn.close()
    session.clear()
    flash("Your account has been permanently deleted.")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    email = current_user_email()
    if email: log_event("LOGOUT", email, request.remote_addr)
    session.clear()
    return redirect(url_for("login"))

@app.route("/game")
def game():
    email = current_user_email()
    if not email:
        return redirect(url_for("login"))
    return render_template("game.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)











