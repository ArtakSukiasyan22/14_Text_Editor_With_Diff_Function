import sys
from PySide6.QtWidgets import QApplication
from diff_editor import DiffEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiffEditor()
    window.show()
    sys.exit(app.exec())
