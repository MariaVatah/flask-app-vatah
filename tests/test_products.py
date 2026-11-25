
import pytest
from tinydb import TinyDB

from run import app as flask_app
import app.products.views as product_views


VALID_PRODUCT = {
    "name": "Test Product",
    "content": "Test product description",
    "price": "123.45",
    "category": "electronics",
    "quantity": "3",
}


@pytest.fixture
def client(tmp_path, monkeypatch):
    db = TinyDB(str(tmp_path / "test_products.json"))
    table = db.table("products")

    monkeypatch.setattr(product_views, "products_table", table)
    monkeypatch.setitem(flask_app.config, "TESTING", True)
    monkeypatch.setitem(flask_app.config, "WTF_CSRF_ENABLED", False)
    monkeypatch.setitem(flask_app.config, "SECRET_KEY", "test-secret")

    yield flask_app.test_client(), table

    db.close()


def test_products_list_page(client):
    test_client, table = client

    response = test_client.get("/product")

    assert response.status_code == 200


def test_add_product_page(client):
    test_client, table = client

    response = test_client.get("/product/add")

    assert response.status_code == 200


def test_add_product(client):
    test_client, table = client

    response = test_client.post("/product/add", data=VALID_PRODUCT)

    assert response.status_code == 302

    products = table.all()
    assert len(products) == 1
    assert products[0]["name"] == "Test Product"
    assert products[0]["id"] == 1
    assert products[0]["created_at"]
    assert products[0]["image"] == ""


def test_add_product_invalid_data(client):
    test_client, table = client

    invalid_data = VALID_PRODUCT.copy()
    invalid_data["name"] = "AB"
    invalid_data["price"] = "-10"

    response = test_client.post("/product/add", data=invalid_data)

    assert response.status_code == 200
    assert len(table.all()) == 0


def test_product_detail(client):
    test_client, table = client

    test_client.post("/product/add", data=VALID_PRODUCT)

    response = test_client.get("/product/1")

    assert response.status_code == 200
    assert b"Test Product" in response.data


def test_product_detail_not_found(client):
    test_client, table = client

    response = test_client.get("/product/999")

    assert response.status_code == 404


def test_edit_product(client):
    test_client, table = client

    test_client.post("/product/add", data=VALID_PRODUCT)

    original_product = table.get(lambda item: item["id"] == 1)
    original_created_at = original_product["created_at"]

    updated_data = VALID_PRODUCT.copy()
    updated_data["name"] = "Updated Product"
    updated_data["price"] = "200.00"

    response = test_client.post(
        "/product/1/edit",
        data=updated_data
    )

    assert response.status_code == 302

    updated_product = table.get(lambda item: item["id"] == 1)

    assert updated_product["name"] == "Updated Product"
    assert updated_product["price"] == "200.00"
    assert updated_product["id"] == 1
    assert updated_product["created_at"] == original_created_at


def test_edit_product_page(client):
    test_client, table = client

    test_client.post("/product/add", data=VALID_PRODUCT)

    response = test_client.get("/product/1/edit")

    assert response.status_code == 200
    assert b"Test Product" in response.data


def test_delete_product(client):
    test_client, table = client

    test_client.post("/product/add", data=VALID_PRODUCT)

    response = test_client.post("/product/1/delete")

    assert response.status_code == 302
    assert len(table.all()) == 0


def test_delete_product_not_found(client):
    test_client, table = client

    response = test_client.post("/product/999/delete")

    assert response.status_code == 404