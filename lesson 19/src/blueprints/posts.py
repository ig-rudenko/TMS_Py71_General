from flask import Blueprint, render_template, request

from src.services.posts import post_service

blueprint = Blueprint('posts', __name__)


@blueprint.route("/posts")
def list_posts_view():
    posts = post_service.get_posts_list()
    return render_template("posts/list.html", posts=posts)


@blueprint.route('/posts/create', methods=["GET", "POST"])
def create_new_post_view():
    print("Функция create_new_post_view, метод:", request.method)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        print("title:", title)
        print("content:", content)

        if not title or not content:
            return render_template("posts/create.html", error="Заголовок и содержимое должны быть переданы!")

        # --------------------
        post_service.create_new_post(title, content)

        return render_template("posts/post_created_successfuly.html")

    return render_template("posts/create.html")
