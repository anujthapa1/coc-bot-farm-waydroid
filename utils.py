"""
Utility functions for ADB execution and image byte parsing.
"""

import subprocess
from typing import Optional, List
import config

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


def run_adb_command(cmd_args: List[str], device: str = None, timeout: int = config.ADB_COMMAND_TIMEOUT) -> subprocess.CompletedProcess:
    """Executes an ADB command using subprocess and returns CompletedProcess."""
    target_device = device or config.ADB_DEVICE
    full_cmd = ["adb", "-s", target_device] + cmd_args
    return subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=True)


def check_adb_device_status(device: str = None) -> str:
    """
    Checks status of target device from `adb devices`.
    Returns: 'device' (authorized/ready), 'unauthorized', 'offline', or 'not_found'.
    """
    target = device or config.ADB_DEVICE
    try:
        res = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=config.ADB_COMMAND_TIMEOUT)
        for line in res.stdout.splitlines():
            line_str = line.strip()
            if target in line_str:
                parts = line_str.split()
                if len(parts) >= 2:
                    return parts[1]  # e.g. 'device', 'unauthorized', 'offline'
        return "not_found"
    except Exception:
        return "unknown"


def parse_screencap_bytes(raw_bytes: bytes) -> Optional["np.ndarray"]:
    """
    Decodes raw PNG bytes received from `adb exec-out screencap -p` into OpenCV BGR numpy array.
    """
    if not raw_bytes or cv2 is None or np is None:
        return None

    # Fast decode using opencv imdecode
    image_np = np.frombuffer(raw_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return image_bgr
