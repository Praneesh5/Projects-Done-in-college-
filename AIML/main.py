"""
main.py — Application Entry Point
==================================
Launches the Healthcare AI desktop application.

This is the file to run:
    python main.py

Or to build as an executable:
    pyinstaller --onefile --windowed --icon=assets/icon.ico main.py

Prerequisites:
    1. Install dependencies: pip install -r requirements.txt
    2. Train the model:      python train_model.py
    3. Then run:             python main.py
"""

import sys
import os
import logging


def main() -> None:
    """
    Application entry point.

    Steps:
        1. Set up logging
        2. Verify model artifacts exist
        3. Launch the GUI
    """
    # ── Setup Logging ─────────────────────────────────────────────────
    from core.utils import setup_logging, MODELS_DIR
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("Healthcare AI Application Starting...")
    logger.info("=" * 50)

    # ── Verify Model Artifacts ────────────────────────────────────────
    required_files = ["model.joblib", "scaler.joblib"]
    missing = [f for f in required_files if not os.path.isfile(os.path.join(MODELS_DIR, f))]

    if missing:
        logger.error("Missing model files: %s", missing)
        logger.error("Please run 'python train_model.py' first.")

        # Show error dialog if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Model Not Found",
                "The trained model was not found.\n\n"
                "Please run the following command first:\n"
                "    python train_model.py\n\n"
                f"Expected location: {MODELS_DIR}\n"
                f"Missing files: {', '.join(missing)}"
            )
            root.destroy()
        except Exception:
            pass
        sys.exit(1)

    # ── Launch Application ────────────────────────────────────────────
    try:
        from gui.app import HealthcareApp

        logger.info("Initializing GUI...")
        app = HealthcareApp()

        logger.info("Application ready. Entering main loop.")
        app.mainloop()

        logger.info("Application closed normally.")

    except Exception as e:
        logger.exception("Fatal error: %s", e)

        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Application Error",
                f"A fatal error occurred:\n\n{str(e)}\n\n"
                "Please check the app.log file for details."
            )
            root.destroy()
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()