import pytest

from app import create_app, db
from app.posts.models import Post, PostCategory
from datetime import datetime


@pytest.fixture
def client():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

def test_create_post_page(client):
    response = client.get("/post/create")

    assert response.status_code == 200

def test_create_post(client):
    response = client.post(
        "/post/create",
        data={
            "title": "Тестовий пост",
            "content": "Текст тестового поста",
            "enabled": "y",
            "publish_date": "2026-11-25T12:00",
            "category": "news"
        },
        follow_redirects=False
    )

    assert response.status_code == 302

    post = db.session.scalar(
        db.select(Post).where(Post.title == "Тестовий пост")
    )

    assert post is not None
    assert post.content == "Текст тестового поста"
    assert post.is_active is True
    assert post.category == PostCategory.NEWS

def test_create_post_default_author(client):
    client.post(
        "/post/create",
        data={
            "title": "Пост без автора",
            "content": "Перевірка автора за замовчуванням",
            "enabled": "y",
            "publish_date": "2026-11-25T12:00",
            "category": "other"
        }
    )

    post = db.session.scalar(
        db.select(Post).where(Post.title == "Пост без автора")
    )

    assert post is not None
    assert post.author == "Anonymous"

def test_posts_list(client):
    post1 = Post(
        title="Старіший пост",
        content="Текст першого поста",
        category=PostCategory.NEWS,
        is_active=True
    )

    post2 = Post(
        title="Новіший пост",
        content="Текст другого поста",
        category=PostCategory.TECH,
        is_active=True
    )

    post1.posted = datetime(2026, 11, 24, 10, 0)
    post2.posted = datetime(2026, 11, 25, 10, 0)

    db.session.add_all([post1, post2])
    db.session.commit()

    response = client.get("/post")

    assert response.status_code == 200
    assert response.data.index("Новіший пост".encode()) < response.data.index("Старіший пост".encode())

def test_posts_list_excludes_inactive(client):
    active_post = Post(
        title="Активний пост",
        content="Цей пост має відображатися",
        category=PostCategory.NEWS,
        is_active=True
    )

    inactive_post = Post(
        title="Неактивний пост",
        content="Цей пост не повинен відображатися",
        category=PostCategory.TECH,
        is_active=False
    )

    db.session.add_all([active_post, inactive_post])
    db.session.commit()

    response = client.get("/post")

    assert response.status_code == 200
    assert "Активний пост".encode() in response.data
    assert "Неактивний пост".encode() not in response.data

def test_post_detail(client):
    post = Post(
        title="Детальний пост",
        content="Повний текст поста для перевірки сторінки.",
        category=PostCategory.NEWS,
        is_active=True
    )

    db.session.add(post)
    db.session.commit()

    response = client.get(f"/post/{post.id}")

    assert response.status_code == 200
    assert "Детальний пост".encode() in response.data
    assert "Повний текст поста для перевірки сторінки.".encode() in response.data

def test_update_post(client):
    post = Post(
        title="Старий заголовок",
        content="Старий текст",
        category=PostCategory.NEWS,
        is_active=True
    )

    db.session.add(post)
    db.session.commit()

    response = client.post(
        f"/post/{post.id}/update",
        data={
            "title": "Новий заголовок",
            "content": "Оновлений текст поста",
            "enabled": "y",
            "publish_date": "2026-11-26T12:00",
            "category": "tech"
        },
        follow_redirects=False
    )

    assert response.status_code == 302

    updated_post = db.session.get(Post, post.id)

    assert updated_post.title == "Новий заголовок"
    assert updated_post.content == "Оновлений текст поста"
    assert updated_post.category == PostCategory.TECH

def test_update_post_page(client):
    post = Post(
        title="Пост для редагування",
        content="Початковий текст",
        category=PostCategory.NEWS,
        is_active=True
    )

    db.session.add(post)
    db.session.commit()

    response = client.get(f"/post/{post.id}/update")

    assert response.status_code == 200
    assert "Пост для редагування".encode() in response.data
    assert "Початковий текст".encode() in response.data

def test_delete_post(client):
    post = Post(
        title="Пост для видалення",
        content="Цей пост потрібно видалити",
        category=PostCategory.NEWS,
        is_active=True
    )

    db.session.add(post)
    db.session.commit()

    post_id = post.id

    response = client.post(
        f"/post/{post_id}/delete",
        follow_redirects=False
    )

    assert response.status_code == 302

    deleted_post = db.session.get(Post, post_id)
    assert deleted_post is None

def test_delete_post_page(client):
    post = Post(
        title="Пост для підтвердження",
        content="Текст поста",
        category=PostCategory.NEWS,
        is_active=True
    )

    db.session.add(post)
    db.session.commit()

    response = client.get(f"/post/{post.id}/delete")

    assert response.status_code == 200
    assert "Пост для підтвердження".encode() in response.data