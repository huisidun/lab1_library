def get_global_style() -> str:
    return """
    QWidget {
        font-family: "Segoe UI", "Arial", sans-serif;
        font-size: 16px;
        font-weight: bold;
        background-color: #EBE7E7;
    }
    QLabel {
        color: #333;
    }
    QPushButton {
        background-color: #C7C6C6;
        color: black;
        padding: 10px 20px;
        border-radius: 6px;
        min-width: 120px;
    }
    QPushButton:hover {
        background-color: #D9D9D9;
    }
    QGroupBox {
        font-weight: bold;
        color: #2c3e50;
        border: 1px solid #bdc3c7;
        border-radius: 6px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    QLineEdit {
        padding: 8px;
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        background: white;
    }
    """