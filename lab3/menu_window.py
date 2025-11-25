from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class MenuWindow(QWidget):
    def __init__(self, switch_to_login, switch_to_game):
        super().__init__()
        self.setWindowTitle("меню")
        self.resize(900, 700) # среднее поумолчанию
        # маленькое - self.resize(800, 600)
        # большое - self.resize(1000, 800)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("тут типо меню"))

        btn1 = QPushButton(" ← вернуться к авторизации")
        btn1.clicked.connect(switch_to_login)
        btn2 = QPushButton("начать игру →")
        btn2.clicked.connect(switch_to_game)

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        self.setLayout(layout)


