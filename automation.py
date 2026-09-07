"""
Automation module executing tap, swipe, text, and keyevent directly via ADB shell input.
"""

from utils import run_adb_command
import config


class Automation:
    """Handles inputs directly on the Waydroid Android subsystem using ADB input events."""

    def __init__(self, device: str = None):
        self.device = device or config.ADB_DEVICE

    def tap(self, x: int, y: int) -> bool:
        """Executes ADB shell input tap at relative coordinates (x, y)."""
        try:
            run_adb_command(["shell", "input", "tap", str(int(x)), str(int(y))], device=self.device)
            return True
        except Exception:
            return False

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """Executes ADB shell input swipe from (x1, y1) to (x2, y2)."""
        try:
            run_adb_command(
                ["shell", "input", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2)), str(int(duration_ms))],
                device=self.device
            )
            return True
        except Exception:
            return False

    def text(self, text_content: str) -> bool:
        """Sends text input via ADB shell input text."""
        try:
            run_adb_command(["shell", "input", "text", text_content], device=self.device)
            return True
        except Exception:
            return False

    def keyevent(self, key_code: int) -> bool:
        """Sends an Android key event via ADB (e.g. 3 = HOME, 4 = BACK)."""
        try:
            run_adb_command(["shell", "input", "keyevent", str(key_code)], device=self.device)
            return True
        except Exception:
            return False
