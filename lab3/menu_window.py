from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from classes.use_data import UserManager


class MenuWindow(QWidget):
    def __init__(self, switch_to_login, switch_to_game, initial_scale, set_scale_callback, user=None):
        super().__init__()
        self.setWindowTitle("Меню")
        self._switch_to_login = switch_to_login
        self._switch_to_game = switch_to_game
        self._set_scale = set_scale_callback
        self._user = user

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self.setLayout(self._layout)

        self.apply_scale(initial_scale)
        self._init_ui()

    def _init_ui(self):
        self._layout.setSpacing(20)
        
        if self._user:
            title = QLabel("САПЁР")
            title.setStyleSheet("font-size: 20px; font-weight: bold;")
            title.setAlignment(Qt.AlignLeft)
            self._layout.addWidget(title)
            
            greeting_text = f"Здравствуй, {self._user.full_name}!"
            greeting = QLabel(greeting_text)
            greeting.setStyleSheet("font-size: 18px; font-weight: bold; color: #510202;")
            greeting.setAlignment(Qt.AlignLeft)
            self._layout.addWidget(greeting)
        else:
            title = QLabel("САПЁР")
            title.setStyleSheet("font-size: 20px; font-weight: bold;")
            title.setAlignment(Qt.AlignLeft)
            self._layout.addWidget(title)

        settings_label = QLabel("Настройки игры")
        settings_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        settings_label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(settings_label)

        levels_group = QGroupBox("Уровень сложности")
        levels_layout = QVBoxLayout()
        
        levels = [
            ("Новичок", 9, 9, 10),
            ("Любитель", 16, 16, 40),
            ("Профессионал", 16, 30, 99)  # rows=16, cols=30
        ]
        
        for name, rows, cols, mines in levels:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, r=rows, c=cols, m=mines: self._switch_to_game((r, c, m)))
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
        
        if self._user:
            records_btn = QPushButton("Мои рекорды")
            records_btn.clicked.connect(self._show_records)
            self._layout.addWidget(records_btn)

        back_btn = QPushButton("← назад")
        back_btn.clicked.connect(self._switch_to_login)
        self._layout.addWidget(back_btn)

    def _show_records(self):
        user_manager = UserManager()
        record = user_manager.get_record_by_user_id(self._user.id)

        lines = []
        for i, name in [(1, "Новичок"), (2, "Любитель"), (3, "Профессионал")]:
            best = getattr(record, f"best_time_{i}")
            if best is not None:
                m = int(best) // 60
                s = int(best) % 60
                lines.append(f"{name}: {m:02}:{s:02}")
            else:
                lines.append(f"{name}: —")

        QMessageBox.information(self, "Мои рекорды", "\n".join(lines))

    def update_greeting(self, user):
        while self._layout.count():
            child = self._layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._user = user
        self._init_ui()

    def apply_scale(self, scale: str):
        size_map = {"small": (800, 600), "medium": (900, 700), "large": (1000, 800)}
        margin_map = {"small": 20, "medium": 30, "large": 40}
        w, h = size_map[scale]
        margin = margin_map[scale]
        self.resize(w, h)
        self._layout.setContentsMargins(margin, margin, margin, margin)