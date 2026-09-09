"""
Utility functions for ADB execution and image byte parsing.
"""

import subprocess
import cv2
import numpy as np
from typing import Optional, List
import config


def run_adb_command(cmd_args: List[str], device: str = None, timeout: int = config.ADB_COMMAND_TIMEOUT) -> subprocess.CompletedProcess:
    """Executes an ADB command using subprocess and returns CompletedProcess."""
    target_device = device or config.ADB_DEVICE
    full_cmd = ["adb", "-s", target_device] + cmd_args
    return subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=True)


def parse_screencap_bytes(raw_bytes: bytes) -> Optional[np.ndarray]:
    """
    Decodes raw PNG bytes received from `adb exec-out screencap` into OpenCV BGR numpy array.
    """
    if not raw_bytes:
        return None

    # Fast decode using opencv imdecode
    image_np = np.frombuffer(raw_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return image_bgr
