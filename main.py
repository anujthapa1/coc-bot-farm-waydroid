"""
Main entry point for Coc-Auto-Farm Linux/Waydroid/Weston edition.
"""

import sys
import queue
import tkinter as tk
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
