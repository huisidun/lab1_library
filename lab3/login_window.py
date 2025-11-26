from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt
from use_data import authenticate_user
from exceptions import InvalidCredentialsError


class LoginWindow(QWidget):
    def __init__(self, switch_to_menu, initial_scale, set_scale_callback):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self._switch_to_menu = switch_to_menu
        self._set_scale = set_scale_callback

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self.setLayout(self._layout)

        self.apply_scale(initial_scale)
        self._init_ui()

    def _init_ui(self):
        self._layout.setSpacing(15)

        title = QLabel("САПЁР")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignLeft)
        self._layout.addWidget(title)

        title = QLabel(" ")
        self._layout.addWidget(title)
        title = QLabel(" ")
        self._layout.addWidget(title)

        title = QLabel("Авторизация")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7XXXXXXXXXX")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("••••••••")

        form.addRow("Телефон:", self.phone_input)
        form.addRow("Пароль:", self.password_input)
        self._layout.addLayout(form)

        self._layout.addStretch()

        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self._on_login)  # ← НОВЫЙ МЕТОД!
        self._layout.addWidget(login_btn)

        register_btn = QPushButton("Регистрация")
        self._layout.addWidget(register_btn)

    def _on_login(self):
        phone = self.phone_input.text().strip()
        password = self.password_input.text()

        try:
            user = authenticate_user(phone, password)
            self._switch_to_menu(user)  
        except InvalidCredentialsError:
            QMessageBox.warning(self, "Ошибка", "Неверный телефон или пароль.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось войти: {str(e)}")

    def apply_scale(self, scale: str):
        size_map = {"small": (800, 600), "medium": (900, 700), "large": (1000, 800)}
        margin_map = {"small": 20, "medium": 30, "large": 40}
        w, h = size_map[scale]
        margin = margin_map[scale]
        self.resize(w, h)
        self._layout.setContentsMargins(margin, margin, margin, margin)