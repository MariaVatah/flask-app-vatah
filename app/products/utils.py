
import os
import uuid

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def is_valid_image(file_path, extension):
    with open(file_path, "rb") as file:
        header = file.read(8)

    if extension == "png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")

    if extension in {"jpg", "jpeg"}:
        return header.startswith(b"\xff\xd8\xff")

    return False


def save_product_image(image_file):
    if not image_file or not image_file.filename:
        return None

    original_name = secure_filename(image_file.filename)

    if "." not in original_name:
        raise ValueError(
            "Файл повинен мати розширення PNG, JPG або JPEG."
        )

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Дозволені лише формати PNG, JPG та JPEG."
        )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    image_file.save(file_path)

    if not is_valid_image(file_path, extension):
        os.remove(file_path)
        raise ValueError(
            "Файл не є справжнім зображенням PNG, JPG або JPEG."
        )

    return f"uploads/{unique_name}"