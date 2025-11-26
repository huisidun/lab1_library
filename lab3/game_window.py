from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame

class GameWindow(QWidget):
    def __init__(self, switch_to_menu, scale="medium"):
        super().__init__()
        self.setWindowTitle("Сапер")

        size_map = {"small": (800, 600), "medium": (900, 700), "large": (1000, 800)}
        w, h = size_map.get(scale, (900, 700))
        self.resize(w, h)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("10"))
        top_bar.addStretch()
        top_bar.addWidget(QPushButton("🙂"))
        top_bar.addStretch()
        top_bar.addWidget(QLabel("00:00"))
        layout.addLayout(top_bar)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)

        layout.addWidget(QLabel("тут тип сама игра"))
        layout.addWidget(QPushButton("← назад", clicked=switch_to_menu))

        self.setLayout(layout)