from enum import StrEnum
from typing import Callable

from .models import User
from .services import login_service, reg_service
from .exceptions import LogoutException


class MenuCommand(StrEnum):
    login = "вход"
    register = "регистрация"
    logout = "выход"
    post_add = "создать"
    post_view = "посмотреть"
    post_edit = "изменить"
    post_delete = "удалить"


MENU_CONTENT_TEMPLATE = """
==========================================
  Для работы используй следующие команды:
{commands}
===========================================
  """


def get_menu_commands_verbose():
    text = ""
    for cmd in MenuCommand:
        text += f"   {cmd}\n"
    return text


class Menu:

    def __init__(self):
        self._user: User | None = None
        self._services_map: dict[MenuCommand, Callable] = {
            MenuCommand.login: self.login_service,
            MenuCommand.register: self.user_reg_service
        }

    def login_service(self, *args, **kwargs) -> None:
        username = input("Введите username: ")
        password = input("Введите password: ")
        res = login_service(username, password)
        self._user = res

    def user_reg_service(self, *args, **kwargs) -> None:
        username = input("Введите username: ")
        password = input("Введите password: ")
        res = reg_service(username, password)
        self._user = res

    def register_service(self, cmd: MenuCommand, service: Callable) -> None:
        self._services_map[cmd] = service

    def process_cmd(self, user_input: str) -> None:
        # ['вход']
        # ['посмотреть', '1']
        # ['']
        cmd = user_input.strip().split()
        # Проверяем что пользователь ввёл хоть что-то.
        if not cmd:
            print("Неверная команда!")
            return

        cmd_value: MenuCommand = cmd.pop(0)
        # Проверяем, что пользователь ввёл верную команду.
        if cmd_value not in MenuCommand:
            print("Неверная команда!")
            return

        # Проверяем, что для команды есть сервис.
        if cmd_value not in self._services_map:
            print("Нет сервиса для команды :(")
            return

        service = self._services_map[cmd_value]
        service(self._user, *cmd)

    def welcome(self) -> None:
        cmd_verbose = get_menu_commands_verbose()
        print(MENU_CONTENT_TEMPLATE.format(commands=cmd_verbose))

    def run(self):
        while True:
            print("")
            username = f"[{self._user.username}]" if self._user else ""
            cmd = input(f" {username}> ")
            try:
                self.process_cmd(cmd)
            except LogoutException:
                self._user = None
