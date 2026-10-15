
from flask import render_template, request
from . import app


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
@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Резюме",
        profile=PROFILE
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    submitted = False

    if request.method == "POST":
        submitted = True

    return render_template(
        "contacts.html",
        title="Контакти",
        profile=PROFILE,
        submitted=submitted
    )

@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template(
        "homepage.html",
        title="Головна сторінка",
        agent=agent
    )