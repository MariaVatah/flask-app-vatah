
import pytest

from run import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def login(client):
    """Допоміжна функція для авторизації."""
    return client.post(
        "/users/login",
        data={
            "username": "student",
            "password": "12345"
        },
        follow_redirects=True
    )

def test_login_success(client):
    response = login(client)

    assert response.status_code == 200
    assert "Ви успішно увійшли в систему!".encode() in response.data


def test_login_wrong_password(client):
    response = client.post(
        "/users/login",
        data={
            "username": "student",
            "password": "wrong"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Неправильний логін або пароль!".encode() in response.data


def test_profile_requires_login(client):
    response = client.get("	/users/profile")

    assert response.status_code == 302
    assert response.location.endswith("/users/login")


def test_profile_available_after_login(client):
    login(client)

    response = client.get("	/users/profile")

    assert response.status_code == 200


def test_logout(client):
    login(client)

    response = client.post("/users/logout")

    assert response.status_code == 302
    assert response.location.endswith("/users/login")

    response = client.get("	/users/profile")

    assert response.status_code == 302
    assert response.location.endswith("/users/login")

def test_add_cookie(client):
    login(client)

    response = client.post(
        "/users/cookies/add",
        data={
            "key": "test_cookie",
            "value": "hello",
            "days": "7"
        }
    )

    assert response.status_code == 302
    assert client.get_cookie("test_cookie") is not None
    assert client.get_cookie("test_cookie").value == "hello"


def test_add_cookie_rejects_invalid_expiration(client):
    login(client)

    response = client.post(
        "/users/cookies/add",
        data={
            "key": "test_cookie",
            "value": "hello",
            "days": "0"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Вкажіть ключ і коректний термін дії cookie.".encode() in response.data
    assert client.get_cookie("test_cookie") is None


def test_add_cookie_rejects_session_cookie(client):
    login(client)

    response = client.post(
        "/users/cookies/add",
        data={
            "key": "session",
            "value": "fake",
            "days": "7"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Це зарезервований ключ сесії.".encode() in response.data


def test_add_cookie_requires_login(client):
    response = client.post(
        "/users/cookies/add",
        data={
            "key": "test_cookie",
            "value": "hello",
            "days": "7"
        }
    )

    assert response.status_code == 302
    assert response.location.endswith("/users/login")


def test_delete_cookie(client):
    login(client)
    client.set_cookie("test_cookie", "hello")

    response = client.post(
        "/users/cookies/delete",
        data={"key": "test_cookie"}
    )

    assert response.status_code == 302

    delete_headers = response.headers.getlist("Set-Cookie")
    assert any(
        header.startswith("test_cookie=") and "Max-Age=0" in header
        for header in delete_headers
    )


def test_delete_cookie_protects_session(client):
    login(client)

    response = client.post(
        "/users/cookies/delete",
        data={"key": "session"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Не можна видалити Cookie авторизації.".encode() in response.data

    response = client.get("	/users/profile")
    assert response.status_code == 200


def test_delete_all_cookies_preserves_session(client):
    login(client)
    client.set_cookie("test_cookie", "hello")

    response = client.post("/users/cookies/delete-all")

    assert response.status_code == 302
    assert client.get_cookie("test_cookie") is None

    response = client.get("	/users/profile")
    assert response.status_code == 200

@pytest.mark.parametrize("theme", ["light", "dark"])
def test_change_theme(client, theme):
    response = client.post(
        "/users/theme",
        data={"theme": theme}
    )

    assert response.status_code == 302
    assert client.get_cookie("theme") is not None
    assert client.get_cookie("theme").value == theme


def test_change_theme_rejects_invalid_value(client):
    response = client.post(
        "/users/theme",
        data={"theme": "red"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Невідома кольорова схема.".encode() in response.data
    assert client.get_cookie("theme") is None
