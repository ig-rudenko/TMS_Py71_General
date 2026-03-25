
from src.views import Menu, MenuCommand
from src.services import logout_service, add_post_service, view_post_service


def main():
    menu = Menu()
    menu.register_service(MenuCommand.post_add, add_post_service)
    menu.register_service(MenuCommand.post_view, view_post_service)
    menu.register_service(MenuCommand.logout, logout_service)

    menu.welcome()
    menu.run()


if __name__ == '__main__':
    main()
