import logging
import os

from flask import render_template, flash, redirect, url_for
from . import app
from .forms import ContactForm

CONTACT_LOG = os.path.join(app.root_path, "contacts.log")

contact_logger = logging.getLogger("contact_form")
contact_logger.setLevel(logging.INFO)

if not contact_logger.handlers:
    file_handler = logging.FileHandler(
        CONTACT_LOG,
        encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(message)s")
    )
    contact_logger.addHandler(file_handler)

PROFILE = {
    "name": "Марія Ватах",
    "role": "Junior Developer",
    "location": "Івано-Франківськ, Україна",
    "email": "mariia.vatakh.24@pnu.edu.ua",
    "about": "Студентка-програмістка, яка вивчає Python та веброзробку. Люблю перетворювати ідеї на зрозумілі й корисні цифрові рішення.",
    "education": [
        {
            "period": "2024 — дотепер",
            "title": "Інженерія програмного забезпечення (ІПЗ)",
            "place": "Карпатський національний університет імені Василя Стефаника",
            "detail": "Вивчення алгоритмів, структур даних, вебтехнологій та основ розробки програмного забезпечення."
        }
    ],
    "skills": [
        "Розв’язання задач",
        "Командна робота",
        "Увага до деталей",
        "Самостійне навчання"
    ],
    "technologies": [
        "Python", "Flask", "HTML5", "CSS3",
        "Bootstrap", "Git", "SQL — базово"
    ],
    "projects": [
        {
            "name": "Flask Portfolio",
            "kind": "Навчальний проєкт",
            "detail": "Невеликий адаптивний сайт із шаблонами Jinja2, маршрутизацією та контактною формою."
        },
        {
            "name": "Python Utilities",
            "kind": "Практика",
            "detail": "Набір невеликих скриптів для автоматизації повторюваних задач і роботи з даними."
        }
    ]
}



@app.route("/")
def homepage():
    return render_template(
        "homepage.html",
        title="Головна",
        profile=PROFILE
    )


@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Резюме",
        profile=PROFILE
    )



@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        contact_logger.info(
            "Нове повідомлення | Ім'я: %s | Email: %s | "
            "Телефон: %s | Тема: %s | Повідомлення: %s",
            form.name.data,
            form.email.data,
            form.phone.data,
            form.subject.data,
            form.message.data
        )

        flash(
            "Повідомлення успішно оброблено!",
            "success"
        )

        return redirect(url_for("contacts"))

    if form.is_submitted():
        flash(
            "Не вдалося обробити форму. Перевірте правильність заповнення полів.",
            "error"
        )

    return render_template(
        "contacts.html",
        title="Контакти",
        profile=PROFILE,
        form=form
    )