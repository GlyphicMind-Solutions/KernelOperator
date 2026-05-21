# ./gui/tabs/raw_output_tab.py
# Raw LLM Output Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox
)

#local imports
from gui.widgets.text_window import TextWindow



# ====================================
# RAW OUTPUT TAB CLASS
# ====================================
class RawOutputTab(QWidget):
    """
    RAW LLM Output Tab
    - Displays raw text from LLM generation
    - This is the ONLY tab that auto-refreshes
    - Other tabs never overwrite themselves
    """
    # -----------------------
    # Initialize
    # -----------------------
    def __init__(self, parent=None):
        """
            Initializes the RAW LLM output tab
        """
        super().__init__(parent)
        self._build_ui()

    # -----------------------
    # UI Layout
    # -----------------------
    def _build_ui(self):
        """
            Builds the UI for the LLM Raw Output Tab
        """
        layout = QVBoxLayout()

        #header
        header = QLabel("RAW LLM Output")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #box
        box = QGroupBox("Model Output (auto-refreshes)")
        box_layout = QVBoxLayout()

        #window
        self.output_window = TextWindow()
        box_layout.addWidget(self.output_window)

        #layout
        box.setLayout(box_layout)
        layout.addWidget(box)
        layout.addStretch()
        self.setLayout(layout)

    # -----------------------
    # Append Text
    # -----------------------
    def append_text(self, text: str):
        """
            Append text to the output window
        """
        self.output_window.appendPlainText(text)

    # -----------------------
    # Set Text
    # -----------------------
    def set_text(self, text: str):
        """
            Replace the entire output
        """
        self.output_window.setPlainText(text)

    # -----------------------
    # Clear
    # -----------------------
    def clear(self):
        """
            Clear the output window
        """
        self.output_window.clear()

