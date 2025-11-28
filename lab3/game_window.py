# game_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from game.game_logic import MinesweeperGame
from classes.use_data import UserManager


class GameWindow(QWidget):
    def __init__(self, switch_to_menu, scale="medium", rows=9, cols=9, mines=10, current_user=None, difficulty="новичок"):
        super().__init__()
        self.setWindowTitle("Сапёр")

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.switch_to_menu = switch_to_menu
        self.scale = scale
        self.current_user = current_user
        self.difficulty = difficulty

        self.game = MinesweeperGame(self.rows, self.cols, self.mines)
        self.time_elapsed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)

        self._init_ui()

    def _init_ui(self):
        size_map = {"small": (800, 600), "medium": (900, 700), "large": (1000, 800)}
        w, h = size_map.get(self.scale, (900, 700))
        self.resize(w, h)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(10)

        self.mine_label = QLabel(str(self.mines))
        self.mine_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.mine_label.setFixedWidth(40)

        self.smile_btn = QPushButton("🙂")
        self.smile_btn.setFixedSize(40, 40)
        self.smile_btn.clicked.connect(self._restart_game)

        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.time_label.setFixedWidth(50)

        top_bar.addWidget(self.mine_label)
        top_bar.addStretch()
        top_bar.addWidget(self.smile_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.time_label)
        main_layout.addLayout(top_bar)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(2)
        main_layout.addWidget(line)

        available_height = h - 120
        available_width = w - 20
        button_size = min(available_height // self.rows, available_width // self.cols)
        if button_size < 20:
            button_size = 20

        field_width = self.cols * button_size
        field_height = self.rows * button_size
        self.field_container = QWidget()
        self.field_container.setFixedSize(field_width, field_height)

        self.grid_layout = QGridLayout(self.field_container)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons = []

        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                btn = QPushButton("")
                btn.setFixedSize(button_size, button_size)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                btn.setFocusPolicy(Qt.NoFocus)
                btn.clicked.connect(lambda _, r=r, c=c: self._on_left_click(r, c))
                btn.setContextMenuPolicy(Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(lambda pos, r=r, c=c: self._on_right_click(r, c))
                btn.setStyleSheet(self._get_base_style())
                self.grid_layout.addWidget(btn, r, c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.field_container)
        main_layout.addLayout(center_layout)

        back_btn = QPushButton("← назад")
        back_btn.clicked.connect(self._on_back)
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)
        self._update_ui()
        self.timer.start(1000)

    def _get_base_style(self):
        return """
            QPushButton {
                background-color: #c0c0c0;
                text-align: left;
                padding-left: 5px;
                border: 1px solid #a0a0a0;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """

    def _get_number_color(self, num: str) -> str:
        return {
            "0": "#000000",
            "1": "#1f77b4",
            "2": "#2ca02c",
            "3": "#d62728",
            "4": "#9467bd",
            "5": "#8c564b",
            "6": "#17becf",
            "7": "#e377c2",
            "8": "#7f7f7f"
        }.get(num, "#000000")

    def _on_left_click(self, row: int, col: int):
        if self.game.game_over:
            return

        alive = self.game.reveal(row, col)
        self._update_ui()

        if self.game.won:
            self._game_won()
        elif not alive:
            self._game_over()

    def _on_right_click(self, row: int, col: int):
        if self.game.game_over:
            return
        self.game.toggle_flag(row, col)
        self._update_ui()

    def _update_ui(self):
        font_size = max(14, 18 - self.rows // 3)
        for r in range(self.rows):
            for c in range(self.cols):
                state = self.game.get_cell_state(r, c)
                btn = self.buttons[r][c]

                if state == 'flag':
                    btn.setText("🚩")
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: #ffeb3b;
                            color: black;
                            text-align: left;
                            padding-left: 5px;
                            border: 1px solid #a0a0a0;
                            font-weight: bold;
                            font-size: {font_size}px;
                        }}
                        QPushButton:hover {{
                            background-color: #fff176;
                        }}
                        QPushButton:pressed {{
                            background-color: #fff59d;
                        }}
                    """)
                elif state == 'mine':
                    btn.setText("💣")
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: #f44336;
                            color: white;
                            text-align: left;
                            padding-left: 5px;
                            border: 1px solid #a0a0a0;
                            font-weight: bold;
                            font-size: {font_size}px;
                        }}
                        QPushButton:hover {{
                            background-color: #ff7961;
                        }}
                        QPushButton:pressed {{
                            background-color: #ffcccb;
                        }}
                    """)
                elif state == 'hidden':
                    btn.setText("")
                    btn.setStyleSheet(self._get_base_style())
                else:
                    btn.setText(state)
                    color = self._get_number_color(state)
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: #e8e8e8;
                            color: {color};
                            text-align: left;
                            padding-left: 5px;
                            border: 1px solid #a0a0a0;
                            font-weight: bold;
                            font-size: {font_size}px;
                        }}
                        QPushButton:hover {{
                            background-color: #f0f0f0;
                        }}
                        QPushButton:pressed {{
                            background-color: #ffffff;
                        }}
                    """)

    def _update_timer(self):
        if not self.game.game_over:
            self.time_elapsed += 1
            self.time_label.setText(f"{self.time_elapsed // 60:02}:{self.time_elapsed % 60:02}")

    def _restart_game(self):
        self.game = MinesweeperGame(self.rows, self.cols, self.mines)
        self.time_elapsed = 0
        self.timer.stop()
        self.timer.start(1000)
        self.smile_btn.setText("🙂")
        self._update_ui()

    def _game_over(self):
        self.timer.stop()
        self.smile_btn.setText("😵")
        self.game.game_over = True

    def _game_won(self):
        self.timer.stop()
        self.smile_btn.setText("😎")
        self.game.game_over = True

        if self.current_user:
            user_manager = UserManager()
            record = user_manager.get_record_by_user_id(self.current_user.id)

            level_map = {"новичок": 1, "любитель": 2, "профессионал": 3}
            level = level_map[self.difficulty]
            current_best = getattr(record, f"best_time_{level}")

            if current_best is None or self.time_elapsed < current_best:
                setattr(record, f"best_time_{level}", float(self.time_elapsed))
                user_manager.save_records()
                minutes = self.time_elapsed // 60
                seconds = self.time_elapsed % 60
                time_str = f"{minutes:02}:{seconds:02}"
                QMessageBox.information(
                    self,
                    "Новый рекорд!",
                    f"Режим: {self.difficulty}\nВаше время: {time_str}\nЭто новый рекорд!"
                )

    def _on_back(self):
        self.timer.stop()
        self.switch_to_menu()