from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
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
        username=session["username"]
    )

@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    flash("Ви вийшли із системи.", "info")

    return redirect(url_for("users.login"))
