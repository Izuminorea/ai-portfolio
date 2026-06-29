from flask import Flask, render_template, request, redirect
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from flask import session

app = Flask(__name__)

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

USERNAME = "admin"
PASSWORD_LOGIN = "qwerty10"

app.secret_key = os.environ.get("SECRET_KEY")


UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# DB HELPER
def get_db():
    return sqlite3.connect("database.db")


# HOME
@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM portfolio
        ORDER BY id DESC
        LIMIT 8
    """)

    works = cursor.fetchall()
    conn.close()

    return render_template("index.html", works=works)


# PORTFOLIO PAGE
@app.route("/portfolio")
def portfolio():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM portfolio
        ORDER BY id DESC
    """)

    items = cursor.fetchall()
    conn.close()

    return render_template("portfolio.html", items=items)

#CONTACT PAGE

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        body = f"""
New Portfolio Message

Name: {fullname}
Email: {email}
Subject: {subject}

Message:
{message}
"""

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        try:

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            server.quit()

            return render_template("success.html")

        except Exception as e:

            return str(e)

    return render_template("contact.html")

# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")

# TOOLS PAGE
@app.route("/tools")
def tools():
    return render_template("tools.html")


# LOGIN PAGE
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD_LOGIN:

            session["admin"] = True

            return redirect("/admin")

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")

# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ADMIN DASHBOARD
@app.route("/admin")
def admin():

    if "admin" not in session:

        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM portfolio
        ORDER BY id DESC
    """)

    items = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        items=items
    )


# UPLOAD (IMAGE + VIDEO + DESCRIPTION)
@app.route("/admin/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]

        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        filename = file.filename
        ext = filename.rsplit(".", 1)[1].lower()

        # detect file type
        if ext in ["jpg", "jpeg", "png", "webp"]:
            file_type = "image"
        elif ext in ["mp4", "webm", "mov"]:
            file_type = "video"
        else:
            return "Unsupported file type"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO portfolio
            (title, category, file_name, file_type, description)
            VALUES (?, ?, ?, ?, ?)
        """, (title, category, filename, file_type, description))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("upload.html")


# EDIT ITEM
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):

    conn = get_db()
    cursor = conn.cursor()

    title = request.form["title"]
    category = request.form["category"]
    description = request.form["description"]

    file = request.files.get("file")

    if file and file.filename != "":

        # Get old file
        cursor.execute(
            "SELECT file_name FROM portfolio WHERE id=?",
            (id,)
        )

        old = cursor.fetchone()

        if old:
            old_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                old[0]
            )

            if os.path.exists(old_path):
                os.remove(old_path)

        filename = file.filename

        file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        cursor.execute("""
            UPDATE portfolio
            SET
                title=?,
                category=?,
                file_name=?,
                description=?
            WHERE id=?
        """,
        (
            title,
            category,
            filename,
            description,
            id
        ))

    else:

        cursor.execute("""
            UPDATE portfolio
            SET
                title=?,
                category=?,
                description=?
            WHERE id=?
        """,
        (
            title,
            category,
            description,
            id
        ))

    conn.commit()
    conn.close()

    return redirect("/admin")


# DELETE ITEM + FILE REMOVE
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT file_name FROM portfolio WHERE id=?", (id,))
    item = cursor.fetchone()

    if item:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], item[0])
        if os.path.exists(filepath):
            os.remove(filepath)

    cursor.execute("DELETE FROM portfolio WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)