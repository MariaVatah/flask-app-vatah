from datetime import datetime
from decimal import Decimal

from flask import (
    render_template,
    abort,
    flash,
    redirect,
    url_for
)

from app.products import products_bp
from app.products.database import products_table
from app.products.forms import ProductForm
from app.products.utils import save_product_image

@products_bp.route("/product")
@products_bp.route("/products/")
def list_products():
    products = products_table.all()

    return render_template(
        "products/products.html",
        products=products
    )

@products_bp.route("/product/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = save_product_image(form.image.data)

            existing_products = products_table.all()
            next_id = max(
                (product["id"] for product in existing_products),
                default=0
            ) + 1

            product = {
                "id": next_id,
                "name": form.name.data,
                "content": form.content.data,
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path or "",
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            products_table.insert(product)

            flash(
                "Товар успішно додано!",
                "success"
            )

            return redirect(url_for("products.list_products"))

        except ValueError as error:
            flash(str(error), "error")

    elif form.is_submitted():
        flash(
            "Перевірте правильність заповнення форми.",
            "error"
        )

    return render_template(
        "products/add_product.html",
        form=form
    )

@products_bp.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = products_table.get(
        lambda item: item["id"] == product_id
    )

    if product is None:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        try:
            new_image = save_product_image(form.image.data)

            updated_product = {
                "name": form.name.data,
                "content": form.content.data,
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": new_image or product["image"]
            }

            products_table.update(
                updated_product,
                lambda item: item["id"] == product_id
            )

            flash("Товар успішно оновлено!", "success")
            return redirect(
                url_for("products.detail_product", product_id=product_id)
            )

        except ValueError as error:
            flash(str(error), "error")

    elif form.is_submitted():
        flash("Перевірте правильність заповнення форми.", "error")

    else:
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(product["price"])
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    return render_template(
        "products/edit_product.html",
        form=form,
        product=product
    )

@products_bp.route("/product/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    product = products_table.get(
        lambda item: item["id"] == product_id
    )

    if product is None:
        abort(404)

    products_table.remove(
        lambda item: item["id"] == product_id
    )

    flash("Товар успішно видалено!", "success")

    return redirect(url_for("products.list_products"))

@products_bp.route("/product/<int:product_id>")
@products_bp.route("/products/<int:product_id>")
def detail_product(product_id):
    product = products_table.get(
        lambda item: item["id"] == product_id
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        product=product
    )