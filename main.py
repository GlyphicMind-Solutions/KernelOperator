# ./main.py
# KernelOperator Main Application Entry Point
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions


# system imports
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# local imports
from gui.main_window import MainWindow


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================
# ---------
# Main
# ---------
def main():
    """
    Launches the KernelOperator GUI application.
    """
    app = QApplication(sys.argv)

    # Path to manifest.yaml inside ./models/
    manifest_path = Path(__file__).parent / "models" / "manifest.yaml"

    # Create main window
    window = MainWindow(manifest_path)

    # Wire PlanningTab → LauncherOutputTab
    window.planning_tab.set_launcher_output_tab(window.launcher_output_tab)

    # Show window
    window.show()

    # Start Qt event loop
    sys.exit(app.exec_())


# ------------------------------------------
# Run (for window)
# ------------------------------------------
if __name__ == "__main__":
    main()

