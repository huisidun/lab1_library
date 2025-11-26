from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, switch_to_login, switch_to_game, initial_scale, set_scale_callback):
        super().__init__()
        self.setWindowTitle("Меню")
        self._switch_to_login = switch_to_login
        self._switch_to_game = switch_to_game
        self._set_scale = set_scale_callback

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self.setLayout(self._layout)

        self.apply_scale(initial_scale)
        self._init_ui()

    def _init_ui(self):
        self._layout.setSpacing(20)

        title = QLabel("САПЁР")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignLeft)
        self._layout.addWidget(title)

        title = QLabel("Настройки игры")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(title)

        levels_group = QGroupBox("Уровень сложности")
        levels_layout = QVBoxLayout()
        for text in ["Новичок", "Любитель", "Профессионал"]:
            btn = QPushButton(text)
            btn.clicked.connect(self._switch_to_game)
            levels_layout.addWidget(btn)
        levels_group.setLayout(levels_layout)
        self._layout.addWidget(levels_group)

        scale_group = QGroupBox("Масштаб интерфейса")
        scale_layout = QHBoxLayout()
        for name, scale in [("Маленький", "small"), ("Средний", "medium"), ("Большой", "large")]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, s=scale: self._set_scale(s))
            scale_layout.addWidget(btn)
        scale_group.setLayout(scale_layout)
        self._layout.addWidget(scale_group)

        self._layout.addStretch() 

        back_btn = QPushButton("← назад")
        back_btn.clicked.connect(self._switch_to_login)
        self._layout.addWidget(back_btn)

    def apply_scale(self, scale: str):
        size_map = {"small": (800, 600), "medium": (900, 700), "large": (1000, 800)}
        margin_map = {"small": 20, "medium": 30, "large": 40}
        w, h = size_map[scale]
        margin = margin_map[scale]
        self.resize(w, h)
        self._layout.setContentsMargins(margin, margin, margin, margin)