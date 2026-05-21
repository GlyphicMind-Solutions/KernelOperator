# ./gui/tabs/description_tab.py
# Description Tab for the Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions


# system imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox
)

# local imports
from gui.widgets.text_window import TextWindow
from prompt.plan_generator import PlanGenerator


# ==================================
# DESCRIPTION TAB CLASS
# ==================================
class DescriptionTab(QWidget):
    """
    Description Tab
    - User writes what they want done
    - Generates a STRICT JSON plan using the active LLM
    - Sends RAW output to RawOutputTab
    """

    def __init__(self, raw_output_tab, parent=None):
        """
            Initializes the Description Tab
        """
        super().__init__(parent)

        self.raw_output_tab = raw_output_tab
        self.engine = None
        self.model_key = None

        self._build_ui()
        self._connect_signals()
        self._set_enabled(False)

    # ----------------------------
    # Build UI
    # ----------------------------
    def _build_ui(self):
        """
            Builds the UI
                -task description box
                -generate plan button
        """
        layout = QVBoxLayout()

        #Tab Label
        header = QLabel("Task Description")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        # Description input box
        box = QGroupBox("Describe what you want the LLM to plan")
        box_layout = QVBoxLayout()
        self.description_window = TextWindow()
        box_layout.addWidget(self.description_window)
        #layout
        box.setLayout(box_layout)
        layout.addWidget(box)

        # Generate button
        self.generate_btn = QPushButton("Generate Plan")
        self.generate_btn.setFixedHeight(40)
        #layout
        layout.addWidget(self.generate_btn)
        layout.addStretch()
        self.setLayout(layout)

    # ----------------------------
    # Connect signals
    # ----------------------------
    def _connect_signals(self):
        """
            generate plan when button is clicked
        """
        self.generate_btn.clicked.connect(self._on_generate_plan)

    # ----------------------------
    # Enable/Disable
    # ----------------------------
    def _set_enabled(self, enabled: bool):
        """
            enables the generate button and description window
        """
        self.description_window.setEnabled(enabled)
        self.generate_btn.setEnabled(enabled)

    # ----------------------------
    # Set LLM
    # ----------------------------
    def set_llm(self, engine, model_key):
        """
            sets the llm engine, and model key
        """
        self.engine = engine
        self.model_key = model_key
        self._set_enabled(True)

    # ----------------------------
    # Clear LLM
    # ----------------------------
    def clear_llm(self):
        """
            Clears LLM from task
        """
        self.engine = None
        self.model_key = None
        self._set_enabled(False)

    # ----------------------------
    # Generate Plan
    # ----------------------------
    def _on_generate_plan(self):
        """
            Generates plan based on user input
        """
        if not self.engine or not self.model_key:
            return

        description = self.description_window.toPlainText().strip()
        if not description:
            self.raw_output_tab.append_text("[ERROR] No description provided.\n")
            return

        generator = PlanGenerator(self.engine, self.model_key)

        # Clear RAW output
        self.raw_output_tab.clear()
        self.raw_output_tab.append_text("🧠 Generating plan...\n\n")

        try:
            plan_text = generator.generate_plan(description)

            # Append raw LLM output
            self.raw_output_tab.append_text(plan_text + "\n")

        except Exception as e:
            self.raw_output_tab.append_text(f"[ERROR] {str(e)}\n")

