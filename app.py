from helpers import login_required
import sqlite3
from flask import flash,Flask,session , render_template, request, redirect, url_for
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
    user_id = session.get("user_id")
    conn = get_db_connection()
    problems = conn.execute('SELECT id, title, topic, difficulty, theory_url, practice_url, status, notes FROM problems WHERE user_id = ? order by id desc', (user_id,)).fetchall()
    conn.close()
    return render_template('index.html', problems=problems)


@app.route("/login", methods=["GET", "POST"])
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

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db = get_db()
    db.execute("DELETE FROM problems WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    db.commit()
    flash("Problem deleted!", "warning")
    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST", "GET"])
@login_required
def edit(id):

    if request.method == "GET":
        conn = get_db_connection()
        problem = conn.execute("SELECT * FROM problems WHERE id = ? AND user_id = ?", (id, session["user_id"])).fetchone()
        if not problem: 
            conn.close()   
            return redirect("/")
        conn.close()
        return render_template("edit.html", problem=problem)
       

    else:
        conn = get_db_connection()
        title = request.form.get("title")
        topic = request.form.get("topic")
        difficulty = request.form.get("difficulty")
        status = request.form.get("status")
        theory_url = request.form.get("theory_url", "")
        practice_url = request.form.get("practice_url", "")
        notes = request.form.get("notes", "")

        if not title or not topic or not difficulty or not status:
            conn.close()
            return "All fields except URLs and notes are required.", 400

        conn.execute(
            "UPDATE problems SET title = ?, topic = ?, difficulty = ?, status = ?, theory_url = ?, practice_url = ?, notes = ? WHERE id = ? AND user_id = ?",
            (title, topic, difficulty, status, theory_url, practice_url, notes, id, session["user_id"])
        )
        conn.commit()
        conn.close()
        flash("Problem updated!", "info")
        return redirect("/")
        
    

@app.route("/register", methods=["GET", "POST"])
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



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        
        title = request.form.get("title")
        if not title:
            return ("Provide Title")

        topic = request.form.get("topic")
        if not topic:
            return ("Provide Topic")

        difficulty = request.form.get("difficulty")
        if not difficulty:
            return ("Provide Difficulty")

        status = request.form.get("status")
        if not status:  
            return ("Provide Status")   

        theory_url = request.form.get("theory_url", "")
        practice_url = request.form.get("practice_url", "")
        notes = request.form.get("notes", "")

        user_id = session.get("user_id")

        conn = get_db_connection()
        conn.execute("INSERT INTO problems(title, topic, difficulty, status, theory_url, practice_url, notes, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, topic, difficulty, status, theory_url, practice_url, notes, user_id))
        flash("Problem added successfully!", "success")
        conn.commit()
        conn.close()
        flash("Problem added!", "success")
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)