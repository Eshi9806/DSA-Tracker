from helpers import login_required
import sqlite3
from flask import Flask,session , render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('tracker.db')
    # Row factory allows accessing columns by name (e.g., row['title'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    problems = conn.execute('SELECT * FROM problems').fetchall()
    conn.close()
    return f"Total problems tracked: {len(problems)}"



@app.route("/login", methods=["GET", "POST"])
@login_required
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password", 403)

        # Query database for username
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        ).fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return ("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "GET":
        conn = get_db_connection()
        return render_template('registration.html')

    else:
        
        username = request.form.get("username")
        if not username:
            return ("Provide Username")

        password = request.form.get("password")
        if not password:
            return ("Provide a password")

        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return ("Confirm Password")

        if password != confirm_password:
            return ("Password not matched")
            conn = get_db_connection()

        if len(conn.execute("Select * from users where username = ?", (username,)).fetchall()) > 0:
            conn.close()
            return ("Username already taken")
        password1 = generate_password_hash(password)
        conn.execute("INSERT INTO users(username,hash) VALUES (?,?)", (username, password1))
        conn.commit()
        conn.close()

        return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)