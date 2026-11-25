from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SelectChoice,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    content = TextAreaField(
        "Текст поста",
        validators=[
            DataRequired()
        ]
    )

    enabled = BooleanField(
        "Активний пост",
        default=True
    )

    publish_date = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Категорія",
        choices=[
            SelectChoice("news", "Новини"),
            SelectChoice("publication", "Публікація"),
            SelectChoice("tech", "Технології"),
            SelectChoice("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Зберегти")