from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import sqlite3
from database import init_db, get_conn, log_event
from security import is_valid_email, is_strong_password, hash_password, verify_password
import os

# This finds the absolute path to the folder where app.py sits
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'super-secret-key-don-not-tell-anyone' # Add this line!
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

# initialise database when app starts
init_db()

# When deployed with HTTPS later, we will also set:
# app.config["SESSION_COOKIE_SECURE"] = True

def current_user_email():
    return session.get("user_email")

def login_required():
    if not current_user_email():
        abort(403)

@app.route("/")
def home():
    if current_user_email():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("new_password")

        if is_strong_password(new_password):
            pw_hash = hash_password(new_password)
            
            conn = get_conn()
            cur = conn.cursor()
            # Update the user's password in the database
            cur.execute("UPDATE users SET password_hash = ? WHERE email = ?", (pw_hash, email))
            conn.commit()
            conn.close()
            
            log_event("PASSWORD_RESET_SUCCESS", email, request.remote_addr)
            flash("Your password has been updated. Please log in.")
            return redirect(url_for("login"))
        else:
            flash("Password is too weak.")
            return render_template("reset_password.html", email=email)

    # This part would normally be triggered by an email link
    email = request.args.get("email")
    return render_template("reset_password.html", email=email)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 1. Define variables at the start of the POST block
        full_name = (request.form.get("full_name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        phone = (request.form.get("phone") or "").strip()
        password = request.form.get("password") or ""
        consent = 1 if request.form.get("consent") == "on" else 0

        # ... (your validation checks for if not full_name, etc.) ...

        pw_hash = hash_password(password)

        conn = None # Initialize conn to None for safety
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(full_name, email, phone, password_hash, consent) VALUES(?,?,?,?,?)",
                (full_name, email, phone, pw_hash, consent)
            )
            conn.commit()
            log_event("REGISTER_SUCCESS", email, request.remote_addr)
            flash("Account created. Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("That email is already registered.")
            return render_template("register.html")

        except Exception as e:
            print(f"Error: {e}") # This will show you the real error in the terminal
            flash("An error occurred. Please try again.")
            return render_template("register.html")

        finally:
            if conn:
                conn.close()

    # Handles the initial GET request
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        conn = get_conn()
        cur = conn.cursor()
        # Fetch the user by email
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

        if user and verify_password(password, user["password_hash"]):
            # Update the last login timestamp
            cur.execute("UPDATE users SET last_login = datetime('now') WHERE email = ?", (email,))
            conn.commit()
            conn.close()

            # Create the session
            session["user_email"] = user["email"]
            log_event("LOGIN_SUCCESS", email, request.remote_addr)
            return redirect(url_for("dashboard"))
        else:
            if conn:
                conn.close()
            log_event("LOGIN_FAILED", email, request.remote_addr)
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not current_user_email():
        return redirect(url_for("login"))
    
    # Define email immediately so both GET and POST can use it
    email = current_user_email()

    if request.method == "POST":
        new_password = request.form.get("new_password")
        if is_strong_password(new_password):
            pw_hash = hash_password(new_password)
            conn = get_conn()
            cur = conn.cursor()
            # Now 'email' is correctly defined for this query
            cur.execute("UPDATE users SET password_hash = ? WHERE email = ?", (pw_hash, email))
            conn.commit()
            conn.close()
            flash("Password updated successfully!")
        else:
            flash("Password too weak!")
        return redirect(url_for("dashboard"))
    if not current_user_email():
        return redirect(url_for("login"))
    
    email = current_user_email()
    conn = get_conn()
    cur = conn.cursor()
    
    # Fetch user info
    cur.execute("SELECT full_name, last_login, created_at FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    # Fetch last 5 audit logs for this user
    cur.execute("SELECT event, ip, created_at FROM audit_logs WHERE email = ? ORDER BY created_at DESC LIMIT 5", (email,))
    logs = cur.fetchall()
    
    conn.close()

    return render_template("dashboard.html", 
                           name=user["full_name"], 
                           last_login=user["last_login"],
                           member_since=user["created_at"],
                           logs=logs) # Pass the logs to the HTML

@app.route("/logout")
def logout():
    if current_user_email():
        log_event("LOGOUT", current_user_email(), request.remote_addr)
    session.clear()
    return redirect(url_for("login"))

@app.errorhandler(403)
def forbidden(e):
    return "403 Forbidden", 403

@app.route("/profile")
def profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    email = session['user_email']
    
    conn = get_conn()
    cur = conn.cursor()
    # Corrected column names: full_name and created_at
    cur.execute("SELECT full_name, email, created_at FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if user:
        return render_template("profile.html", user=user)
    
    return "User not found", 404

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        
        # 1. Connect to the database
        conn = get_conn()
        cur = conn.cursor()
        
        # 2. ACTUALLY find the user (This creates the 'user' variable)
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
 
        # 3. Now this check will work because 'user' exists!
        if user:
            # FOR TESTING ONLY: We go straight to the reset page
            return redirect(url_for("reset_password", email=email))
 
        # Best practice: Don't tell hackers if the email was wrong
        flash("If an account exists, a reset link has been sent.")
        return redirect(url_for("login"))

    return render_template("forgot_password.html")

@app.route("/delete-account", methods=["POST"])
def delete_account():
    if not current_user_email():
        return redirect(url_for("login"))
    
    email = current_user_email()
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # 1. Log the deletion event before the user is gone
        log_event("ACCOUNT_DELETED_BY_USER", email, request.remote_addr)
        
        # 2. Delete the user
        cur.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
    except Exception as e:
        print(f"Delete error: {e}")
        flash("An error occurred during account deletion.")
        return redirect(url_for("dashboard"))
    finally:
        conn.close()
    
    # 3. Clear session and send them back to login
    session.clear()
    flash("Your account and data have been permanently deleted.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
