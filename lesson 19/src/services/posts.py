from src.db import db
from src.models import Post


class PostService:

    @staticmethod
    def get_posts_list() -> list[Post]:
        posts = Post.query.all()
        return posts

    @staticmethod
    def get_post_by_id(id_: int) -> Post | None:
        post = Post.query.get(id_)
        return post

    @staticmethod
    def create_new_post(title: str, content: str) -> Post:
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def edit_post(post: Post, title: str, content: str) -> Post:
        post.title = title
        post.content = content
        db.session.commit()
        return post

    @staticmethod
    def delete_post(id_: int) -> Post | None:
        post = Post.query.get(id_)
        if post is None:
            return None
        db.session.delete(post)
        db.session.commit()
        return post


post_service = PostService()
