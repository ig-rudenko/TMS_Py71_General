from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .db_connector import session
from .models import User, Post
from .exceptions import LogoutException


def login_service(username: str, password: str) -> User | None:
    user = session.query(User).filter(User.username == username).first()
    if not user:
        print("Нет такого пользователя")
        return None

    if user.password != password:
        print("Неверный пароль")

    return user


def reg_service(username: str, password: str) -> User | None:
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return user


def logout_service(*args, **kwargs) -> None:
    print("Выход")
    raise LogoutException


def add_post_service(user: User | None, *args, **kwargs) -> None:
    if user is None:
        print("Войдите, чтобы создать заметку!")
        return

    while True:
        title = input("Введите заголовок: ")
        if len(title) > 64:
            print("Слишком длинный заголовок")
            continue
        break

    content = input("Введите содержимое: ")

    commit = input("Создать? [Y/n] ") or "y"
    if commit.lower() == "n":
        return

    post = Post(title=title, content=content, user_id=user.id)
    session.add(post)
    session.commit()


def get_post_verbose(post: Post, with_content: bool) -> str:
    text = f"""
# {post.id}
# {post.created_at.strftime("%d/%m/%Y %H:%M")}
-----------------------------
 {post.title}
-----------------------------"""

    if with_content:
        text += f"""
 {post.content}
==========================================
"""
    return text


def view_post_service(user: User, post_value: str = "", *args, **kwargs) -> None:
    if user is None:
        print("Войдите, чтобы смотреть заметки!")
        return

    # Проверяем что передан ID заметки и он НЕ числовой!
    if post_value and not post_value.isdigit():
        print("Неверный идентификатор заметки! Должно быть число.")
        return

    # select posts.*
    #   from posts
    #   join users on (posts.user_id=users.id)
    #   where users.username = 'igor';
    query = (
        select(Post)
        .join(User, User.id == Post.user_id)
        .where(User.username == user.username)
        .limit(10)
    )

    # Если у нас передан идентификатор заметки и он числовой.
    if post_value:
        query = query.where(Post.id == int(post_value))

        try:
            post = session.execute(query).scalar_one()
        except NoResultFound:
            print("Нет такой заметки!")
            return

        print(get_post_verbose(post, with_content=True))
        return

    # Если ID заметки пустой, тогда возвращаем все заметки без содержимого
    posts = session.execute(query).scalars()
    text = ""
    for post in posts:
        text += get_post_verbose(post, with_content=False)

    print(text)
