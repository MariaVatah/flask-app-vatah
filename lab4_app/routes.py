from lab4_app.resume_data import PROFILE

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
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
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=session["username"],
        cookies=request.cookies,
        theme=session.get("theme", "light")
    )


@app.route("/set_theme/<theme>", methods=["POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("profile"))

    session["theme"] = theme
    flash("Кольорову схему змінено.", "success")
    return redirect(url_for("profile"))


@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", "").strip()

    if not key or not max_age:
        flash("Заповніть ключ cookie та термін дії.", "danger")
        return redirect(url_for("profile"))

    try:
        max_age = int(max_age)
        if max_age < 0:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути невід'ємним цілим числом.", "danger")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.set_cookie(key, value, max_age=max_age)

    flash(f"Cookie «{key}» успішно додано.", "success")
    return response



@app.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Введіть ключ cookie для видалення.", "danger")
        return redirect(url_for("profile"))

    if key not in request.cookies:
        flash(f"Cookie «{key}» не знайдено.", "danger")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.delete_cookie(key)

    flash(f"Cookie «{key}» успішно видалено.", "success")
    return response


@app.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("login"))

    cookies_to_delete = [
        key for key in request.cookies.keys()
        if key != app.config.get("SESSION_COOKIE_NAME", "session")
    ]

    if not cookies_to_delete:
        flash("Немає користувацьких cookie для видалення.", "warning")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))

    for key in cookies_to_delete:
        response.delete_cookie(key)

    flash("Запит на видалення користувацьких cookie надіслано.", "success")
    return response

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("login"))
