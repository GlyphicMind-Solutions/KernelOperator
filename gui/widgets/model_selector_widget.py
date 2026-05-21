# ./gui/widgets/model_selector_widget.py
# Model Selector for the Kernel Operator
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions


#system imports
from pathlib import Path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QComboBox, QMessageBox
)

#local imports
from engine.llm_engine import LLMEngine



# =======================================
# MODEL SELECTOR WIDGET CLASS
# =======================================
class ModelSelectorWidget(QWidget):
    """
    Global model selector widget for KernelOperator.
    - Dropdown of available models
    - Load Model button
    - Unload Model button
    - Emits signals when model is loaded/unloaded
    """

    model_loaded = pyqtSignal(str)
    model_unloaded = pyqtSignal()

    # --------------
    # Initialize
    # --------------
    def __init__(self, manifest_path: Path, parent=None):
        """
            Initializes the Model Selector widget
        """
        super().__init__(parent)

        # Engine loads manifest + model registry
        self.engine = LLMEngine(manifest_path)
        self.active_model_key = None

        # Dropdown for model selection
        self.dropdown = QComboBox()

        # Load / Unload buttons
        self.load_btn = QPushButton("Load Model")
        self.unload_btn = QPushButton("Unload Model")
        self.unload_btn.setEnabled(False)

        # Populate dropdown with available models
        self._populate_dropdown()
        self._connect_signals()

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.dropdown)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.unload_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    # -------------------------
    # Populate dropdown
    # -------------------------
    def _populate_dropdown(self):
        """
            Populates dropdown with manifest list
        """
        models = self.engine.get_available_models()
        for m in models:
            key = m["key"]
            path = m["path"]
            self.dropdown.addItem(f"{key}  —  {path}", key)

    # -------------------------
    # Connect signals
    # -------------------------
    def _connect_signals(self):
        """
            Establishes load/unload for buttons
        """
        self.load_btn.clicked.connect(self._load_model)
        self.unload_btn.clicked.connect(self._unload_model)

    # -------------------------
    # Load model
    # -------------------------
    def _load_model(self):
        """
            Loads model into program from dropdown
        """
        key = self.dropdown.currentData()

        try:
            # Engine handles lazy loading + caching
            self.engine.load_model(key)

            self.active_model_key = key
            self.dropdown.setEnabled(False)
            self.load_btn.setEnabled(False)
            self.unload_btn.setEnabled(True)

            # Notify GUI
            self.model_loaded.emit(key)

        except Exception as e:
            QMessageBox.critical(self, "Model Load Error", str(e))

    # -------------------------
    # Unload model
    # -------------------------
    def _unload_model(self):
        """
            Unloads current active model
        """
        if self.active_model_key in self.engine.models:
            # Safe unload: remove from cache
            self.engine.models.pop(self.active_model_key, None)

        self.active_model_key = None

        self.dropdown.setEnabled(True)
        self.load_btn.setEnabled(True)
        self.unload_btn.setEnabled(False)

        # Notify GUI
        self.model_unloaded.emit()

    # -------------------------
    # Get Active Model
    # -------------------------
    def get_active_model(self):
        """
            returns active model
        """
        return self.active_model_key

    # -------------------------
    # Get Engine
    # -------------------------
    def get_engine(self):
        """
            returns the LLMEngine instance
        """
        return self.engine

