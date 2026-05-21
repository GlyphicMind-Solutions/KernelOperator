# ./gui/tabs/analyze_plan_tab.py
# Analyze Plan Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox
)

#local imports
from gui.widgets.text_window import TextWindow
from prompt.plan_analyzer import PlanAnalyzer



# ==================================
# ANALYZE PLAN TAB CLASS
# ==================================
class AnalyzePlanTab(QWidget):
    """
    Analyze Plan Tab
    - Two windows:
        1. Plan to Analyze
        2. LLM Analysis Output
    - Uses the active LLM to analyze a plan
    - Does NOT touch RAW LLM OUTPUT
    """
    # ----------------------
    # Initialize
    # ----------------------
    def __init__(self, parent=None):
        """
            Initializes the Analyze Plan Tab
        """
        super().__init__(parent)
        self.engine = None
        self.model_key = None
        self._build_ui()
        self._connect_signals()
        self._set_enabled(False)

    # ----------------------
    # Build UI
    # ----------------------
    def _build_ui(self):
        """
            Builds the UI for the Analyze Plan Tab
        """
        layout = QVBoxLayout()

        # Header
        header = QLabel("Analyze Plan")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #--- Top Window: Plan to Analyze ---#
        plan_box = QGroupBox("Plan to Analyze")
        plan_layout = QVBoxLayout()
        #Plan input window
        self.plan_input = TextWindow()
        plan_layout.addWidget(self.plan_input)
        #plan layout box
        plan_box.setLayout(plan_layout)
        layout.addWidget(plan_box)

        # Analyze Button
        self.analyze_btn = QPushButton("Analyze Plan")
        self.analyze_btn.setFixedHeight(40)
        layout.addWidget(self.analyze_btn)

        #--- Bottom Window: LLM Analysis Output ---#
        output_box = QGroupBox("LLM Analysis Output")
        output_layout = QVBoxLayout()
        # Analysis Window
        self.analysis_output = TextWindow()
        output_layout.addWidget(self.analysis_output)
        # Layout
        output_box.setLayout(output_layout)
        layout.addWidget(output_box)

        layout.addStretch()
        self.setLayout(layout)

    # ----------------------
    # Connect Signals
    # ----------------------
    def _connect_signals(self):
        """
            Analyzes Plan when the Analyze Plan button is clicked
        """
        self.analyze_btn.clicked.connect(self._on_analyze_plan)

    # ----------------------
    # Set Enabled
    # ----------------------
    def _set_enabled(self, enabled: bool):
        """
            Sets enabled state for plan input and analyze
        """
        self.plan_input.setEnabled(enabled)
        self.analyze_btn.setEnabled(enabled)
        self.analysis_output.setEnabled(enabled)

    # ----------------------
    # Set LLM
    # ----------------------
    def set_llm(self, engine, model_key):
        """
            Sets the LLM for the task
        """
        self.engine = engine
        self.model_key = model_key
        self._set_enabled(True)

    # ----------------------
    # Clear LLM
    # ----------------------
    def clear_llm(self):
        """
            Clears current LLM from task
        """
        self.engine = None
        self.model_key = None
        self._set_enabled(False)

    # ----------------------
    # Analyze Plan
    # ----------------------
    def _on_analyze_plan(self):
        """
            Takes a plan that was generated, analyzes the plan into a description.
            NOTE: if your inputted description matches the Analyze Plan output,
            you have a solid plan and can run/execute with ease.
        """
        if not self.engine or not self.model_key:
            return

        plan_text = self.plan_input.toPlainText().strip()
        if not plan_text:
            self.analysis_output.appendPlainText("[ERROR] No plan provided.\n")
            return

        analyzer = PlanAnalyzer(self.engine, self.model_key)

        self.analysis_output.clear()
        self.analysis_output.appendPlainText("🧠 Analyzing plan...\n\n")

        try:
            # Strict JSON analysis output
            result = analyzer.analyze_plan(plan_text)
            self.analysis_output.appendPlainText(result + "\n")

        except Exception as e:
            self.analysis_output.appendPlainText(f"[ERROR] {str(e)}\n")

