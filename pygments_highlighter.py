from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer
from PySide6.QtCore import Qt

from pygments import lex
from pygments.token import Token


class PygmentsHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        # self.formatter = HtmlFormatter()
        self.lexer = PythonLexer()

    def highlightBlock(self, text):

        # Get styled token
        tokens = highlight(text, self.lexer, self.formatter).splitlines()
        for token in tokens:
            if not token.strip():
                continue
            # Parse token and style based on type
            token_type, token_value = token.split(":", 1)
            fmt = QTextCharFormat()

            # Example styles (can be expanded)
            if "Keyword" in token_type:
                fmt.setForeground(QColor(Qt.blue))
                fmt.setFontWeight(QFont.Bold)
            elif "String" in token_type:
                fmt.setForeground(QColor(Qt.darkGreen))
            elif "Comment" in token_type:
                fmt.setForeground(QColor(Qt.gray))
                fmt.setFontItalic(True)

            # Apply format
            start = text.find(token_value)
            length = len(token_value)
            if start >= 0:
                self.setFormat(start, length, fmt)

    # def highlightBlock(self, text):
    #     for token_type, token_value in lex(text, self.lexer):
    #         fmt = QTextCharFormat()
    #         if token_type in Token.Keyword:
    #             fmt.setForeground(QColor(Qt.blue))
    #             fmt.setFontWeight(QFont.Bold)
    #         elif token_type in Token.String:
    #             fmt.setForeground(QColor(Qt.darkGreen))
    #         elif token_type in Token.Comment:
    #             fmt.setForeground(QColor(Qt.gray))
    #             fmt.setFontItalic(True)

    #         start = text.find(token_value)
    #         if start >= 0:
    #             self.setFormat(start, len(token_value), fmt)
