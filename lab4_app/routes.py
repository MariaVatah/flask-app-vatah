from lab4_app.resume_data import PROFILE

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from lab4_app import app


DEMO_USERNAME = "student"
DEMO_PASSWORD = "12345"


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Резюме",
        profile=PROFILE,
    )

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    submitted = request.method == "POST"

    return render_template(
        "contacts.html",
        title="Контакти",
        profile=PROFILE,
        submitted=submitted,
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("profile"))

        flash("Неправильний логін або пароль.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=session["username"],
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("login"))
