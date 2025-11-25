import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from menu_window import MenuWindow
from game_window import GameWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # создание окон
        self.login_window = LoginWindow(self.show_menu)
        self.menu_window = MenuWindow(self.show_login, self.show_game)
        self.game_window = GameWindow(self.show_menu)

        # начало с авторизайии
        self.show_login()

    def show_login(self):
        self.login_window.show()
        self.menu_window.hide()
        self.game_window.hide()

    def show_menu(self):
        self.login_window.hide()
        self.menu_window.show()
        self.game_window.hide()

    def show_game(self):
        self.login_window.hide()
        self.menu_window.hide()
        self.game_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()