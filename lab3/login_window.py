from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class LoginWindow(QWidget):
    def __init__(self, switch_to_menu):
        super().__init__()
        self.setWindowTitle("авторизация")
        self.resize(900, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("тут типо регистрация/авторизация"))
        btn = QPushButton("Войти")
        btn.clicked.connect(switch_to_menu)
        layout.addWidget(btn)

        self.setLayout(layout)