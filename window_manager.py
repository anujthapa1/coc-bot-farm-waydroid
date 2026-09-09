"""
Window manager using pure ADB for Linux Mint / Waydroid / Weston environment.
Captures frames using high-speed ADB pipe stdout directly into OpenCV NumPy arrays.
"""

import subprocess
import cv2
import numpy as np
from typing import Optional
import config
from utils import parse_screencap_bytes


class WindowManager:
    """Manages Waydroid screen frame acquisition over ADB without Windows dependencies."""

    def __init__(self, device: str = None):
        self.device = device or config.ADB_DEVICE

    def connect(self) -> bool:
        """Connects to the Waydroid ADB target."""
        try:
            cmd = ["adb", "connect", self.device]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=config.ADB_CONNECT_TIMEOUT, text=True)
            return "connected" in res.stdout.lower() or "already connected" in res.stdout.lower()
        except Exception:
            return False

    def get_frame(self) -> Optional[np.ndarray]:
        """
        Captures low-latency frame from Waydroid via `adb exec-out screencap`.
        Returns BGR numpy image array (origin 0,0).
        """
        try:
            cmd = ["adb", "-s", self.device, "exec-out", "screencap", "-p"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_png, stderr = process.communicate(timeout=config.ADB_COMMAND_TIMEOUT)

            if process.returncode != 0 or not raw_png:
                return None

            return parse_screencap_bytes(raw_png)
        except Exception:
            return None
