from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .user import User
from .use_data import UserManager

class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.setModal(True)
        self.resize(350, 300)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(QLabel("Имя:"))
        self.first_name = QLineEdit()
        layout.addWidget(self.first_name)

        layout.addWidget(QLabel("Фамилия:"))
        self.last_name = QLineEdit()
        layout.addWidget(self.last_name)

        layout.addWidget(QLabel("Телефон (+7XXXXXXXXXX):"))
        self.phone = QLineEdit()
        layout.addWidget(self.phone)

        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)

        layout.addWidget(QLabel("Пароль (не менее 4 симв.):"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self._register)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def _register(self):
        try:
            # генерация id
            user_manager = UserManager()
            new_id = f"{len(user_manager.users) + 1:05d}"  

            user = User(
                user_id=new_id,
                first_name=self.first_name.text().strip(),
                last_name=self.last_name.text().strip(),
                phone=self.phone.text().strip(),
                email=self.email.text().strip(),
                password=self.password.text()
            )

            if user_manager.add_user(user):
                QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
                self.accept()  # ззакрыть мсгбокс
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким телефоном уже существует.")

        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректные данные:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зарегистрироваться:\n{e}")