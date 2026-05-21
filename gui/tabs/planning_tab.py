# ./gui/tabs/planning_tab.py
# Planning Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
)

#local imports
from gui.widgets.text_window import TextWindow
from runtime.validator import PlanValidator
from runtime.security import SecurityContext
from runtime.launcher import PlanLauncher



# =========================================
# PLANNING TAB CLASS
# =========================================
class PlanningTab(QWidget):
    """
    Planning Tab
    - User pastes the final verified plan
    - Validates the plan
    - Executes the plan using the KernelOperator runtime
    - Streams output to Launcher Output tab
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
        self.launcher_output_tab = None
        self._build_ui()
        self._connect_signals()
        self._set_enabled(False)

    # ----------------------
    # Build UI
    # ----------------------
    def _build_ui(self):
        """
            Builds the UI for the Planning Tab
        """
        layout = QVBoxLayout()

        header = QLabel("Planning")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #--- Plan Input Window
        plan_box = QGroupBox("Final Plan (paste here)")
        plan_layout = QVBoxLayout()
        #window
        self.plan_window = TextWindow()
        plan_layout.addWidget(self.plan_window)
        #layout
        plan_box.setLayout(plan_layout)
        layout.addWidget(plan_box)

        #--- Run Button
        self.run_btn = QPushButton("Run Plan")
        self.run_btn.setFixedHeight(40)
        layout.addWidget(self.run_btn)
        #layout
        layout.addStretch()
        self.setLayout(layout)

    # ----------------------
    # Connect Signals
    # ----------------------
    def _connect_signals(self):
        """
            Runs plan when "Run Plan" button is clicked
        """
        self.run_btn.clicked.connect(self._on_run_plan)

    # ----------------------
    # Set Enabled
    # ----------------------
    def _set_enabled(self, enabled: bool):
        """
            Sets plan window and run button to enabled
        """
        self.plan_window.setEnabled(enabled)
        self.run_btn.setEnabled(enabled)

    # ----------------------
    # LLM Injection
    # ----------------------
    def set_llm(self, engine, model_key):
        """
            Sets LLM for a given Task
        """
        self.engine = engine
        self.model_key = model_key
        self._set_enabled(True)

    # ----------------------
    # LLM Injection
    # ----------------------
    def clear_llm(self):
        """
            Clears current LLM from task
        """
        self.engine = None
        self.model_key = None
        self._set_enabled(False)

    # -------------------------
    # Set Launcher Output Tab
    # -------------------------
    def set_launcher_output_tab(self, tab):
        """
            Called by MainWindow to wire the launcher output tab
        """
        self.launcher_output_tab = tab

    # ----------------------
    # On Run Plan
    # ----------------------
    def _on_run_plan(self):
        """
            Run Plan Logic:
              -validates plan
              -executes plan
        """
        if not self.engine or not self.model_key:
            return

        if not self.launcher_output_tab:
            return

        plan_text = self.plan_window.toPlainText().strip()
        if not plan_text:
            self.launcher_output_tab.append_text("[ERROR] No plan provided.\n")
            return

        # Clear launcher output
        self.launcher_output_tab.clear()
        self.launcher_output_tab.append_text("🧠 Validating plan...\n\n")

        # Validate Plan
        validator = PlanValidator()
        security = SecurityContext()

        try:
            # Strict JSON validation
            validator.validate(plan_text)

            # Creation-only safety checks
            security.check_plan(plan_text)

        except Exception as e:
            self.launcher_output_tab.append_text(f"[VALIDATION ERROR] {str(e)}\n")
            return

        self.launcher_output_tab.append_text("✔ Plan validated successfully.\n\n")
        self.launcher_output_tab.append_text("🚀 Executing plan...\n\n")

        # Launch Plan
        launcher = PlanLauncher(
            output_callback=self.launcher_output_tab.append_text
        )

        try:
            launcher.execute(plan_text)
            self.launcher_output_tab.append_text("\n✔ Plan execution complete.\n")

        except Exception as e:
            self.launcher_output_tab.append_text(f"[EXECUTION ERROR] {str(e)}\n")

