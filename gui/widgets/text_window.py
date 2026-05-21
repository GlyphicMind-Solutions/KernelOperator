# ./gui/widgets/text_window.py
# Text Window for the Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt



# ==========================================
# TEXT WINDOW CLASS
# ==========================================
class TextWindow(QPlainTextEdit):
    """
    A clean, styled QPlainTextEdit used across KernelOperator.
    - Monospace font
    - No line wrapping
    - Fast scrolling
    - Optional read-only mode
    """
    # ---------------
    # Initialize
    # ---------------
    def __init__(self, read_only=False, parent=None):
        """
            Initializes the Text Window
        """
        super().__init__(parent)

        # Monospace font for code/log readability
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        self.setFont(font)

        # Disable line wrapping for clean formatting
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Optional read-only mode
        self.setReadOnly(read_only)

        # Clean border + padding
        self.setStyleSheet("""
            QPlainTextEdit {
                border: 1px solid #888;
                padding: 6px;
                background-color: #fdfdfd;
            }
        """)

        # Faster scrolling
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    # ---------------
    # Append
    # ---------------
    def append(self, text: str):
        """
            Alias for appendPlainText
        """
        self.appendPlainText(text)

    # ---------------
    # Set Text
    # ---------------
    def set_text(self, text: str):
        """
            Replace the entire contents
        """
        self.setPlainText(text)

    # ---------------
    # Clear Text
    # ---------------
    def clear_text(self):
        """
            Clear the window
        """
        self.clear()
