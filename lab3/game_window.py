from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class GameWindow(QWidget):
    def __init__(self, switch_to_menu):
        super().__init__()
        self.setWindowTitle("сапер")
        self.resize(900, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("тут тип сама игра"))

        btn = QPushButton(" ← ")
        btn.clicked.connect(switch_to_menu)
        layout.addWidget(btn)

        self.setLayout(layout)