from PySide6.QtWidgets import (
    QMainWindow, 
    QPlainTextEdit, 
    QVBoxLayout, 
    QWidget,
    QLabel
)
from PySide6.QtGui import QFont

class DiffEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diff Editor")
        self.resize(1200, 800)

        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout(central_widget)

        # Labels for text areas
        old_label = QLabel("Old Version:")
        new_label = QLabel("New Version:")

        # Text editors and configure font for editors
        self.old_text = QPlainTextEdit()
        self.new_text = QPlainTextEdit()
        editor_font = QFont("Courier", 11)
        self.old_text.setFont(editor_font)
        self.new_text.setFont(editor_font)

        # Diff output
        diff_label = QLabel("Diff Output:")
        self.diff_output = QPlainTextEdit()
        self.diff_output.setFont(editor_font)
        self.diff_output.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(old_label)
        layout.addWidget(self.old_text)
        layout.addWidget(new_label)
        layout.addWidget(self.new_text)
        layout.addWidget(diff_label)
        layout.addWidget(self.diff_output)