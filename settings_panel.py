from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings"))
        self.setLayout(layout)
