# ./gui/tabs/logs_tab.py
# Logs Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox
)

#local imports
from gui.widgets.text_window import TextWindow



# ==========================================
# LOGS TAB CLASS
# ==========================================
class LogsTab(QWidget):
    """
    Logs Tab
    - Stores persistent logs from KernelOperator
    - Does NOT auto-clear unless user manually clears it (future button)
    - Can be appended to by any module
    """
    # -----------------------
    # Initialize
    # -----------------------
    def __init__(self, parent=None):
        """
            Initializes the Log Tab
        """
        super().__init__(parent)
        self._build_ui()

    # -----------------------
    # UI Layout
    # -----------------------
    def _build_ui(self):
        """
            Builds the UI for the Log Tab
                -box, window, text (its basic)
        """
        layout = QVBoxLayout()
        #tab lable
        header = QLabel("Logs")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #box
        box = QGroupBox("Historical Logs")
        box_layout = QVBoxLayout()

        #window
        self.log_window = TextWindow()
        box_layout.addWidget(self.log_window)

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
            Append text to the logs
        """
        self.log_window.appendPlainText(text)

    # -----------------------
    # Output Callback Helper
    # -----------------------
    def get_output_callback(self):
        """
            Returns append_text so any module can stream logs directly.
            This matches the LauncherOutputTab pattern.
        """
        return self.append_text

    # -----------------------
    # Clear
    # -----------------------
    def clear(self):
        """
            Clear the logs
        """
        self.log_window.clear()

