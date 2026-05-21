# ./gui/tabs/launcher_output_tab.py
# Planning Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions


#system imports
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox
)

#local imports
from gui.widgets.text_window import TextWindow



# ========================================
# LAUNCHER OUTPUT TAB CLASS
# ========================================
class LauncherOutputTab(QWidget):
    """
    Launcher Output Tab
    - Displays streaming output from the KernelOperator runtime
    - Used by PlanningTab and PlanLauncher
    """
    # -----------------------
    # Initialize
    # -----------------------
    def __init__(self, parent=None):
        """
            Initializes the Launcher Output Tab
        """
        super().__init__(parent)
        self._build_ui()

    # -----------------------
    # UI Layout
    # -----------------------
    def _build_ui(self):
        """
            Builds the UI for the Launcher Output Tab
                -log box -outputwindow
        """
        layout = QVBoxLayout()

        #--- Launcher Output Tab ---
        header = QLabel("Launcher Output")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #log box
        box = QGroupBox("Execution Log")
        box_layout = QVBoxLayout()

        #output window
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
            Append text to the launcher output
        """
        self.output_window.appendPlainText(text)

    # -----------------------
    # Output Callback Helper
    # -----------------------
    def get_output_callback(self):
        """
            Returns the append_text function so the launcher
            can stream output directly into this tab.
        """
        return self.append_text

    # -----------------
    # Clear
    # -----------------
    def clear(self):
        """
            Clear the output window text
        """
        self.output_window.clear()

