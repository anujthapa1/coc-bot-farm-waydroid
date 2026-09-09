"""
Configuration settings for Coc-Auto-Farm Linux/Waydroid/ADB edition.
"""

import os

# ADB Settings
ADB_HOST = os.environ.get("ADB_HOST", "192.168.240.112")
ADB_PORT = int(os.environ.get("ADB_PORT", 5555))
ADB_DEVICE = os.environ.get("ADB_DEVICE", f"{ADB_HOST}:{ADB_PORT}")

# Connection Retries & Timeouts
ADB_CONNECT_TIMEOUT = 10
ADB_COMMAND_TIMEOUT = 5

# GUI Settings
GUI_POLL_INTERVAL_MS = 150
GUI_TITLE = "Coc-Auto-Farm (Linux / Waydroid / Weston)"
GUI_GEOMETRY = "800x600"

# Hotkey Settings
EMERGENCY_STOP_KEY = "KEY_F12"

# Vision / ML Settings
YOLO_MODEL_PATH = os.environ.get("YOLO_MODEL_PATH", "models/coc_yolo.pt")
CONFIDENCE_THRESHOLD = 0.5
EASYOCR_LANGUAGES = ["en"]
EASYOCR_GPU = False  # Set to True if CUDA is available on Linux host

# Target Game Settings
PACKAGE_NAME = "com.supercell.clashofclans"
MAIN_ACTIVITY = "com.supercell.clashofclans.GameApp"

# File Paths
LOG_FILE = "coc_auto_farm.log"
