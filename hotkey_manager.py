"""
Global Linux hotkey manager using evdev asynchronously scanning /dev/input/ devices.
Handles global F12 emergency stop without Windows dependencies.
"""

import threading
import glob
from typing import Callable, Optional
import evdev
from evdev import ecodes
import config


class HotkeyManager:
    """Listens for global Linux input events using evdev to trigger emergency stop."""

    def __init__(self, callback: Callable[[], None], target_key: str = config.EMERGENCY_STOP_KEY):
        self.callback = callback
        self.target_key = target_key
        self.target_keycode = getattr(ecodes, target_key, ecodes.KEY_F12)
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def start(self):
        """Starts asynchronous hotkey listener thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stops hotkey listener thread."""
        self.running = False

    def _find_keyboard_devices(self):
        devices = []
        for path in glob.glob('/dev/input/event*'):
            try:
                dev = evdev.InputDevice(path)
                capabilities = dev.capabilities()
                if ecodes.EV_KEY in capabilities:
                    keys = capabilities[ecodes.EV_KEY]
                    if self.target_keycode in keys:
                        devices.append(dev)
            except (OSError, PermissionError):
                continue
        return devices

    def _listen_loop(self):
        devices = self._find_keyboard_devices()
        if not devices:
            return

        import select
        dev_map = {dev.fd: dev for dev in devices}

        while self.running:
            try:
                r, _, _ = select.select(list(dev_map.keys()), [], [], 0.5)
                for fd in r:
                    dev = dev_map[fd]
                    for event in dev.read():
                        if event.type == ecodes.EV_KEY and event.value == 1:  # Key press event
                            if event.code == self.target_keycode:
                                self.callback()
            except Exception:
                continue
