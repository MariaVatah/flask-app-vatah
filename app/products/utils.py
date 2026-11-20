
import os
import uuid

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def save_product_image(image_file):
    if not image_file or not image_file.filename:
        return None

    original_name = secure_filename(image_file.filename)

    if "." not in original_name:
        raise ValueError("Файл повинен мати розширення PNG, JPG або JPEG.")

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Дозволені лише формати PNG, JPG та JPEG.")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    image_file.save(file_path)

    return f"uploads/{unique_name}"