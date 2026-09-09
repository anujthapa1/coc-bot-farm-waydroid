"""
Window manager using pure ADB for Linux Mint / Waydroid / Weston environment.
Captures frames using high-speed ADB pipe stdout directly into OpenCV NumPy arrays.
"""

import subprocess
from typing import Optional, Tuple
import config

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

from utils import parse_screencap_bytes, check_adb_device_status


class WindowManager:
    """Manages Waydroid screen frame acquisition over ADB without Windows dependencies."""

    def __init__(self, device: str = None):
        self.device = device or config.ADB_DEVICE

    def connect(self) -> Tuple[bool, str]:
        """
        Connects to the Waydroid ADB target and checks authorization.
        Returns (success: bool, status_message: str).
        """
        try:
            cmd = ["adb", "connect", self.device]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=config.ADB_CONNECT_TIMEOUT, text=True)
            output = res.stdout.lower() + res.stderr.lower()

            status = check_adb_device_status(self.device)
            if status == "unauthorized":
                msg = (
                    f"ADB Device {self.device} is UNAUTHORIZED! "
                    "Please allow USB Debugging prompt inside Waydroid, or run: "
                    "'adb kill-server && adb connect " + self.device + "'"
                )
                return False, msg
            elif status == "offline":
                return False, f"ADB Device {self.device} is offline."
            elif status == "device" or "connected" in output or "already connected" in output:
                return True, f"Connected to ADB device {self.device}."
            else:
                return False, f"Could not connect to {self.device}: {res.stdout.strip()}"
        except Exception as e:
            return False, f"ADB connection error: {e}"

    def get_frame(self) -> Optional["np.ndarray"]:
        """
        Captures low-latency frame from Waydroid via `adb exec-out screencap -p`.
        Returns BGR numpy image array (origin 0,0).
        """
        if cv2 is None or np is None:
            return None

        try:
            cmd = ["adb", "-s", self.device, "exec-out", "screencap", "-p"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_png, stderr = process.communicate(timeout=config.ADB_COMMAND_TIMEOUT)

            if process.returncode != 0 or not raw_png:
                return None

            return parse_screencap_bytes(raw_png)
        except Exception:
            return None
