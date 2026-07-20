from flask import Flask, render_template, request, redirect
import sqlite3
import os
from flask import session
import uuid

app = Flask(__name__)

USERNAME = os.environ.get("ADMIN_USERNAME")
PASSWORD_LOGIN = os.environ.get("ADMIN_PASSWORD")

app.secret_key = os.environ.get("SECRET_KEY")


UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# DB HELPER
def get_db():

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row

    return conn


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
@app.route("/contact")
def contact():
    return render_template("contact.html")

# SUCCESS PAGE
@app.route("/success")
def success():
    return render_template("success.html")

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


#UPLOAD (IMAGE + VIDEO + YOUTUBE)

@app.route("/admin/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]

        file_type = request.form["file_type"]
        youtube_url = request.form.get("youtube_url", "").strip()
        print(request.form)

        conn = get_db()
        cursor = conn.cursor()

        # ===========================
        # YOUTUBE
        # ===========================

        if file_type == "youtube":

            if youtube_url == "":
                conn.close()
                return "Please enter a YouTube URL."

            cursor.execute("""
                INSERT INTO portfolio
                (title, category, file_name, file_type, youtube_url, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                title,
                category,
                None,
                "youtube",
                youtube_url,
                description
            ))

            conn.commit()
            conn.close()

            return redirect("/admin")

        # ===========================
        # IMAGE / VIDEO
        # ===========================

        file = request.files.get("file")

        if not file or file.filename == "":
            conn.close()
            return "No file selected."

        filename = file.filename

        ext = filename.rsplit(".", 1)[1].lower()

        if ext in ["jpg", "jpeg", "png", "webp"]:
            detected_type = "image"

        elif ext in ["mp4", "webm", "mov"]:
            detected_type = "video"

        else:
            conn.close()
            return "Unsupported file type."

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        cursor.execute("""
            INSERT INTO portfolio
            (title, category, file_name, file_type, youtube_url, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            category,
            filename,
            detected_type,
            None,
            description
        ))

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

    file_type = request.form["file_type"]
    youtube_url = request.form.get("youtube_url", "").strip()

    file = request.files.get("file")

    # ==========================
    # YOUTUBE
    # ==========================

    if file_type == "youtube":

        cursor.execute("""
            UPDATE portfolio
            SET
                title=?,
                category=?,
                file_type=?,
                youtube_url=?,
                description=?
            WHERE id=?
        """, (
            title,
            category,
            file_type,
            youtube_url,
            description,
            id
        ))

    # ==========================
    # IMAGE / VIDEO
    # ==========================

    elif file and file.filename != "":

        ext = os.path.splitext(file.filename)[1]

        filename = f"{uuid.uuid4().hex}{ext}"

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
                file_type=?,
                youtube_url=NULL,
                description=?
            WHERE id=?
        """, (
            title,
            category,
            filename,
            file_type,
            description,
            id
        ))

    # ==========================
    # NO NEW FILE
    # ==========================

    else:

        cursor.execute("""
            UPDATE portfolio
            SET
                title=?,
                category=?,
                file_type=?,
                youtube_url=?,
                description=?
            WHERE id=?
        """, (
            title,
            category,
            file_type,
            youtube_url if file_type == "youtube" else None,
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

    cursor.execute(
        "SELECT file_name, file_type FROM portfolio WHERE id=?",
        (id,)
    )

    item = cursor.fetchone()

    if item:

        # Burahin lang ang local file kung image/video
        if item["file_type"] != "youtube" and item["file_name"]:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                item["file_name"]
            )

            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except PermissionError:
                print(f"⚠ File is currently in use: {filepath}")

        cursor.execute(
            "DELETE FROM portfolio WHERE id=?",
            (id,)
        )

        conn.commit()

    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)