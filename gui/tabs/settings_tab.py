# ./gui/tabs/settings_tab.py
# Settings Tab for the Kernal Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions



#system imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout
)



# ==========================================
# SETTINGS TAB CLASS
# ==========================================
class SettingsTab(QWidget):
    """
    Settings Tab
    - Displays model info
    - Displays KernelOperator info
    - Future settings can be added here
    """
    # -----------------------
    # Initialize
    # -----------------------
    def __init__(self, parent=None):
        """
            Initialize settings tab
        """
        super().__init__(parent)
        self.engine = None
        self.model_key = None
        self._build_ui()

    # -----------------------
    # Build UI
    # -----------------------
    def _build_ui(self):
        """
            Builds UI for the Settings Tab
                -model info box
                -app info box
                -model info etc.
        """
        layout = QVBoxLayout()

        #settings tab header
        header = QLabel("Settings")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        #--- Model Info Box ---
        self.model_box = QGroupBox("Active Model Information")
        model_layout = QFormLayout()
        self.model_name_label = QLabel("None")
        self.model_path_label = QLabel("None")
        self.model_ctx_label = QLabel("None")
        #layout
        model_layout.addRow("Model Key:", self.model_name_label)
        model_layout.addRow("Model Path:", self.model_path_label)
        model_layout.addRow("Context Window:", self.model_ctx_label)
        self.model_box.setLayout(model_layout)
        layout.addWidget(self.model_box)

        #--- App Info Box ---
        app_box = QGroupBox("KernelOperator Information")
        app_layout = QFormLayout()
        app_layout.addRow("Application:", QLabel("KernelOperator"))
        app_layout.addRow("Version:", QLabel("1.0.0"))
        app_layout.addRow("Author:", QLabel("David Kistner (Unconditional Love) at GlyphicMind Solutions"))
        app_box.setLayout(app_layout)
        #layout
        layout.addWidget(app_box)

        layout.addStretch()
        self.setLayout(layout)

    # -----------------------
    # Set LLM
    # -----------------------
    def set_llm(self, engine, model_key):
        """
            Sets LLM for a given Task
        """
        self.engine = engine
        self.model_key = model_key

        cfg = engine.models_config.get(model_key, {})

        self.model_name_label.setText(model_key)
        self.model_path_label.setText(cfg.get("path", "Unknown"))
        self.model_ctx_label.setText(str(cfg.get("n_ctx", "Unknown")))

    # -----------------------
    # Clear LLM
    # -----------------------
    def clear_llm(self):
        """
            Clears LLM from given task
        """
        self.engine = None
        self.model_key = None
        self.model_name_label.setText("None")
        self.model_path_label.setText("None")
        self.model_ctx_label.setText("None")

    # -----------------------
    # Output Callback Helper (future-proof)
    # -----------------------
    def append_text(self, text: str):
        """
            Allows future modules or autonomous systems to log into the Settings tab.
            (Useful for debugging model metadata or system intelligence state.)
        """
        # No dedicated text window yet — placeholder for future expansion.
        pass

