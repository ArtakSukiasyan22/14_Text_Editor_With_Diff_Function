from PySide6.QtWidgets import (
    QMainWindow,
    QPlainTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtGui import (
    QFont,
    QSyntaxHighlighter,
    QTextCharFormat,
    QColor,
    QTextFormat,
    QIcon,
)
from difflib import unified_diff
from code_editor import CodeEditor


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.added_format = QTextCharFormat()
        self.removed_format = QTextCharFormat()

        self.added_format.setBackground(QColor("lightgreen"))
        self.removed_format.setBackground(QColor("lightcoral"))
        self.added_format.setProperty(QTextFormat.FullWidthSelection, True)
        self.removed_format.setProperty(QTextFormat.FullWidthSelection, True)

    def highlightBlock(self, text):
        if text.startswith("+") and not text.startswith("+++"):
            self.setFormat(0, len(text), self.added_format)
        elif text.startswith("-") and not text.startswith("---"):
            self.setFormat(0, len(text), self.removed_format)


class DiffEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diff Editor")
        self.setWindowIcon(QIcon("logo.png"))
        self.resize(1200, 800)

        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        v_layout = QVBoxLayout(central_widget)

        # Labels for text areas
        old_label = QLabel("Old Version:")
        new_label = QLabel("New Version:")
        diff_label = QLabel("Diff Output:")

        # Text editors and configure font for editors
        # self.old_text = QPlainTextEdit()
        # self.new_text = QPlainTextEdit()
        self.old_text = CodeEditor()
        self.new_text = CodeEditor()
        self.diff_output = QPlainTextEdit()
        editor_font = QFont("Monaco", 10)
        self.old_text.setFont(editor_font)
        self.new_text.setFont(editor_font)
        self.diff_output.setFont(editor_font)
        self.diff_output.setReadOnly(True)

        # Add widgets to the layout
        h_layout = QHBoxLayout()
        v_old_layout = QVBoxLayout()
        v_new_layout = QVBoxLayout()

        v_old_layout.addWidget(old_label)
        v_old_layout.addWidget(self.old_text)
        v_new_layout.addWidget(new_label)
        v_new_layout.addWidget(self.new_text)

        h_layout.addLayout(v_old_layout)
        h_layout.addLayout(v_new_layout)

        v_layout.addLayout(h_layout)
        v_layout.addWidget(diff_label)
        v_layout.addWidget(self.diff_output)

        # Connect signals to update diff
        self.old_text.textChanged.connect(self.update_diff)
        self.new_text.textChanged.connect(self.update_diff)

        # Apply diff highlighter
        self.diff_highlighter = DiffHighlighter(self.diff_output.document())

    def update_diff(self):
        # Get text from editors
        old_text = self.old_text.toPlainText().splitlines()
        new_text = self.new_text.toPlainText().splitlines()

        # Generate diff
        diff = list(unified_diff(old_text, new_text, lineterm=""))

        # Display diff
        self.diff_output.setPlainText("\n".join(diff))
