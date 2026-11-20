from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    Regexp
)


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім’я",
        validators=[
            DataRequired(message="Вкажіть ваше ім’я."),
            Length(
                min=4,
                max=10,
                message="Ім’я повинно містити від 4 до 10 символів."
            )
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Вкажіть електронну пошту."),
            Email(message="Введіть коректну адресу електронної пошти.")
        ]
    )

    phone = StringField(
        "Номер телефону",
        validators=[
            Optional(),
            Regexp(
                r"^\+380\d{9}$",
                message="Введіть номер у форматі +380XXXXXXXXX."
            )
        ]
    )

    subject = SelectField(
        "Тема повідомлення",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("suggestion", "Пропозиція"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть тему повідомлення.")
        ]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть текст повідомлення."),
            Length(
                max=500,
                message="Повідомлення не повинно перевищувати 500 символів."
            )
        ]
    )

    submit = SubmitField("Надіслати повідомлення")