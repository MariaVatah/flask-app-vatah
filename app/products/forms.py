from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    IntegerField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    ValidationError
)


def validate_price_precision(form, field):
    raw_value = (field.raw_data or [""])[0].strip()

    if "." in raw_value:
        decimal_part = raw_value.rsplit(".", 1)[1]

        if len(decimal_part) > 2:
            raise ValidationError(
                "Ціна може містити не більше двох знаків після коми."
            )


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(
                min=3,
                message="Назва повинна містити щонайменше 3 символи."
            )
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис товару.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            InputRequired(message="Введіть ціну товару."),
            NumberRange(
                min=0.01,
                message="Ціна повинна бути більшою за нуль."
            ),
            validate_price_precision
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("computers", "Комп'ютерна техніка"),
            ("phones", "Смартфони"),
            ("accessories", "Аксесуари"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть категорію товару.")
        ]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Вкажіть кількість товару."),
            NumberRange(
                min=0,
                message="Кількість не може бути від'ємною."
            )
        ]
    )

    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені лише зображення PNG, JPG та JPEG."
            )
        ]
    )

    submit = SubmitField("Зберегти товар")