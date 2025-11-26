import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from menu_window import MenuWindow
from game_window import GameWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self._current_scale = "medium"

        self.login_window = None
        self.menu_window = None
        self.game_window = None
        self.current_user = None

        self.show_login()

    @property
    def current_scale(self):
        return self._current_scale

    def set_scale(self, scale: str):
        if scale not in ("small", "medium", "large"):
            raise ValueError("Invalid scale")
        self._current_scale = scale
        if self.login_window:
            self.login_window.apply_scale(scale)
        if self.menu_window:
            self.menu_window.apply_scale(scale)
        if self.game_window:
            self.game_window.apply_scale(scale)

    def show_login(self):
        if self.login_window is None:
            self.login_window = LoginWindow(
                switch_to_menu=self._on_authenticated,
                initial_scale=self.current_scale,
                set_scale_callback=self.set_scale
            )
        else:
            self.login_window.apply_scale(self._current_scale)
        self.login_window.show()
        self._hide_except("login")

    def _on_authenticated(self, user):
        self.current_user = user
        self.show_menu()  

    def show_menu(self):
        if self.menu_window is None:
            self.menu_window = MenuWindow(
                switch_to_login=self.show_login,
                switch_to_game=self.show_game,
                initial_scale=self.current_scale,
                set_scale_callback=self.set_scale,
                user=self.current_user 
            )
        else:
            self.menu_window.update_greeting(self.current_user)
        self.menu_window.show()
        self._hide_except("menu")

    def show_game(self):
        if self.game_window:
            self.game_window.close()
        self.game_window = GameWindow(self.show_menu, self._current_scale)
        self.game_window.show()
        self._hide_except("game")

    def _hide_except(self, window_name: str):
        if window_name != "login" and self.login_window:
            self.login_window.hide()
        if window_name != "menu" and self.menu_window:
            self.menu_window.hide()
        if window_name != "game" and self.game_window:
            self.game_window.hide()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()