# ./gui/main_window.py
# Main GUI window for the Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions


#system imports
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)

#local imports
from gui.widgets.model_selector_widget import ModelSelectorWidget
from gui.tabs.description_tab import DescriptionTab
from gui.tabs.raw_output_tab import RawOutputTab
from gui.tabs.analyze_plan_tab import AnalyzePlanTab
from gui.tabs.planning_tab import PlanningTab
from gui.tabs.launcher_output_tab import LauncherOutputTab
from gui.tabs.logs_tab import LogsTab
from gui.tabs.settings_tab import SettingsTab



# ======================================
# MAIN WINDOW CLASS
# ======================================
class MainWindow(QMainWindow):
    """
    KernelOperator Main Window
    - Global model selector at the top
    - Tab system below
    - Passes active model + engine to all tabs
    """
    # -------------
    # Initialize
    # -------------
    def __init__(self, manifest_path: Path):
        """
            Initializes the Main GUI
        """
        super().__init__()

        #window title/size
        self.setWindowTitle("GlyphicMind Solutions: KernelOperator — AI Planning & Launcher Runtime")
        self.resize(1200, 800)

        # Global Model Selector
        self.model_selector = ModelSelectorWidget(manifest_path)

        # Tab layout
        self.tabs = QTabWidget()
        self.raw_output_tab = RawOutputTab()
        self.description_tab = DescriptionTab(self.raw_output_tab)
        self.analyze_plan_tab = AnalyzePlanTab()
        self.planning_tab = PlanningTab()
        self.launcher_output_tab = LauncherOutputTab()
        self.logs_tab = LogsTab()
        self.settings_tab = SettingsTab()

        # Tab Names
        self.tabs.addTab(self.description_tab, "Description")
        self.tabs.addTab(self.raw_output_tab, "RAW LLM Output")
        self.tabs.addTab(self.analyze_plan_tab, "Analyze Plan")
        self.tabs.addTab(self.planning_tab, "Planning")
        self.tabs.addTab(self.launcher_output_tab, "Launcher Output")
        self.tabs.addTab(self.logs_tab, "Logs")
        self.tabs.addTab(self.settings_tab, "Settings")

        # Top Layout
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.model_selector)
        layout.addWidget(self.tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Connect model events
        self.model_selector.model_loaded.connect(self._on_model_loaded)
        self.model_selector.model_unloaded.connect(self._on_model_unloaded)

    # -------------------------
    # On Model Loaded
    # -------------------------
    def _on_model_loaded(self, key: str):
        """
            sets a model key for actions
        """

        engine = self.model_selector.get_engine()

        # Pass engine + model key to all tabs that need it
        self.description_tab.set_llm(engine, key)
        self.analyze_plan_tab.set_llm(engine, key)
        self.planning_tab.set_llm(engine, key)

    # -------------------------
    # On Model Unloaded
    # -------------------------
    def _on_model_unloaded(self):
        """
            Clears tabs when model is unloaded
        """
        # Disable LLM-dependent tabs
        self.description_tab.clear_llm()
        self.analyze_plan_tab.clear_llm()
        self.planning_tab.clear_llm()

