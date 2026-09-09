"""
Main entry point for Coc-Auto-Farm Linux/Waydroid/Weston edition.
"""

import sys
import queue
import tkinter as tk


def check_missing_dependencies():
    """Checks for required Python dependencies and prints user-friendly error if missing."""
    missing = []
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")

    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    try:
        import ultralytics
    except ImportError:
        missing.append("ultralytics")

    try:
        import easyocr
    except ImportError:
        missing.append("easyocr")

    try:
        import evdev
    except ImportError:
        missing.append("evdev")

    try:
        import PIL
    except ImportError:
        missing.append("Pillow")

    if missing:
        print("\n" + "=" * 60)
        print("MISSING PYTHON DEPENDENCIES DETECTED!")
        print("=" * 60)
        print(f"The following required packages are missing: {', '.join(missing)}")
        print("\nPlease run the following command in your terminal to install them:\n")
        print("    pip3 install -r requirements.txt\n")
        print("Or install individually:")
        print(f"    pip3 install {' '.join(missing)}")
        print("=" * 60 + "\n")
        sys.exit(1)


check_missing_dependencies()

import config
from logger import setup_logger
from bot import BotEngine
from hotkey_manager import HotkeyManager
from gui import AppGUI


def main():
    # Thread-safe queue for logs & UI state updates
    ui_queue = queue.Queue()

    # Logger setup
    logger = setup_logger(ui_queue)
    logger.info("Initializing Coc-Auto-Farm Linux/Waydroid Edition...")

    # Bot engine
    bot = BotEngine(ui_queue, logger)

    # Emergency stop hotkey callback
    def on_emergency_stop():
        logger.warning("Emergency Stop (F12) triggered!")
        bot.stop()

    hotkey_mgr = HotkeyManager(callback=on_emergency_stop)
    hotkey_mgr.start()

    # Tkinter root window
    root = tk.Tk()

    def handle_start():
        logger.info("Starting bot engine from GUI...")
        bot.start()

    def handle_stop():
        logger.info("Stopping bot engine from GUI...")
        bot.stop()

    def handle_close():
        logger.info("Shutting down application...")
        bot.stop()
        hotkey_mgr.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", handle_close)

    gui = AppGUI(root, ui_queue, on_start=handle_start, on_stop=handle_stop)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received.")
        handle_close()


if __name__ == "__main__":
    main()
