from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
    current_app
)

from app.users import users_bp


USERNAME = "student"
PASSWORD = "12345"


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)

    return render_template(
        "users/hi.html",
        name=name,
        age=age
    )


@users_bp.route("/admin")
def admin():
    return redirect(
        url_for(
            "users.greetings",
            name="administrator",
            age=45
        )
    )


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=request.cookies,
        theme=request.cookies.get("theme", "dark")
    )


@users_bp.route("/theme", methods=["POST"])
def change_theme():
    theme = request.form.get("theme", "dark")

    if theme not in ("dark", "light"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(request.referrer or url_for("resume"))

    response = make_response(
        redirect(request.referrer or url_for("resume"))
    )

    response.set_cookie(
        "theme",
        theme,
        max_age=365 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    flash("Кольорову схему успішно змінено!", "success")

    return response

@users_bp.route("/cookies/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    days = request.form.get("days", type=int)

    if not key or days is None or days <= 0:
        flash("Вкажіть ключ і коректний термін дії cookie.", "danger")
        return redirect(url_for("users.profile"))

    session_cookie_name = current_app.config.get(
        "SESSION_COOKIE_NAME",
        "session"
)

    if key == session_cookie_name:
        flash("Це зарезервований ключ сесії. Виберіть інший.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        key,
        value,
        max_age=days * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    flash(f"Cookie «{key}» успішно додано!", "success")
    return response


@users_bp.route("/cookies/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Вкажіть ключ cookie для видалення.", "danger")
        return redirect(url_for("users.profile"))

    session_cookie_name = current_app.config.get(
        "SESSION_COOKIE_NAME",
        "session"
    )

    if key == session_cookie_name:
        flash("Не можна видалити Cookie авторизації.", "danger")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash(f"Cookie «{key}» не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)

    flash(f"Cookie «{key}» успішно видалено!", "success")
    return response


@users_bp.route("/cookies/delete-all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    session_cookie_name = current_app.config.get(
        "SESSION_COOKIE_NAME",
        "session"
    )

    deleted_count = 0

    for key in request.cookies:
        if key != session_cookie_name:
            response.delete_cookie(key)
            deleted_count += 1

    flash(
        f"Видалено cookies: {deleted_count}. Сесію авторизації збережено.",
        "success"
    )

    return response


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    flash("Ви вийшли із системи.", "info")

    return redirect(url_for("users.login"))
