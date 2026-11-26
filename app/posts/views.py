from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
)

from app import db
from app.posts import posts_bp
from app.posts.forms import PostForm
from app.posts.models import Post, PostCategory, Tag
from app.users.models import User


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    form.user_id.choices = [
        (user.id, user.username)
        for user in db.session.scalars(
            db.select(User).order_by(User.username)
        ).all()
    ]

    form.tags.choices = [
        (tag.id, tag.name)
        for tag in db.session.scalars(
            db.select(Tag).order_by(Tag.name)
        ).all()
    ]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data,
            category=PostCategory(form.category.data),
            user_id=form.user_id.data
        )

        post.tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()

        db.session.add(post)
        db.session.commit()

        flash("Post added successfully", "success")

        return redirect(url_for("posts.create_post"))

    return render_template(
        "posts/add_post.html",
        form=form
    )


@posts_bp.route("", methods=["GET"])
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()

    return render_template("posts/posts.html", posts=posts)


@posts_bp.route("/<int:id>", methods=["GET"])
def post_detail(id):
    post = db.get_or_404(Post, id)
    return render_template("posts/detail_post.html", post=post)


@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    form.user_id.choices = [
        (user.id, user.username)
        for user in db.session.scalars(
            db.select(User).order_by(User.username)
        ).all()
    ]

    form.tags.choices = [
        (tag.id, tag.name)
        for tag in db.session.scalars(
            db.select(Tag).order_by(Tag.name)
        ).all()
    ]

    if not form.is_submitted():
        form.user_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.category.data = post.category.value

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = PostCategory(form.category.data)
        post.user_id = form.user_id.data

        post.tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()

        db.session.commit()

        flash("Post updated successfully", "success")
        return redirect(url_for("posts.post_detail", id=post.id))

    return render_template("posts/add_post.html", form=form)


@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash("Post deleted successfully", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template("posts/delete_confirm.html", post=post)