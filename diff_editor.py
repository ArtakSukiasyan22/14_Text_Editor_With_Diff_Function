from PySide6.QtWidgets import (
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QSplitter,
)
from PySide6.QtGui import Qt, QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from pygments_highlighter import PygmentsHighlighter
from difflib import unified_diff


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.added_format = QTextCharFormat()
        self.added_format.setBackground(QColor("lightgreen"))

        self.removed_format = QTextCharFormat()
        self.removed_format.setBackground(QColor("lightcoral"))

    def highlightBlock(self, text):
        if text.startswith("+") and not text.startswith("+++"):
            self.setFormat(0, len(text), self.added_format)
        elif text.startswith("-") and not text.startswith("---"):
            self.setFormat(0, len(text), self.removed_format)


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
        editor_font = QFont("Courier", 9)
        self.old_text.setFont(editor_font)
        self.new_text.setFont(editor_font)

        # Apply syntax highlighting
        self.old_highlighter = PygmentsHighlighter(self.old_text.document())
        self.new_highlighter = PygmentsHighlighter(self.new_text.document())

        # Diff output
        diff_label = QLabel("Diff Output:")
        self.diff_output = QPlainTextEdit()
        self.diff_output.setFont(editor_font)
        self.diff_output.setReadOnly(True)

        # Apply diff highlighter
        self.diff_highlighter = DiffHighlighter(self.diff_output.document())

        # Connect signals to update diff
        self.old_text.textChanged.connect(self.update_diff)
        self.new_text.textChanged.connect(self.update_diff)

        # Create a splitter for vertical layout
        splitter = QSplitter(Qt.Vertical)

        # Add widgets to the splitter
        splitter.addWidget(self.old_text)
        splitter.addWidget(self.new_text)

        # Add splitter to the layout
        layout.addWidget(old_label)
        layout.addWidget(splitter)
        layout.addWidget(diff_label)
        layout.addWidget(self.diff_output)

    def update_diff(self):
        # Get text from editors
        old_text = self.old_text.toPlainText().splitlines()
        new_text = self.new_text.toPlainText().splitlines()

        # Generate diff
        diff = list(unified_diff(old_text, new_text, lineterm=""))

        # Display diff
        self.diff_output.setPlainText("\n".join(diff))
