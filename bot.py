"""
Bot automation state machine running in background thread and sending updates via queue.
"""

import threading
import queue
import time
import logging
from window_manager import WindowManager
from automation import Automation
from vision import Vision
import config


class BotEngine:
    """Main CoC auto farm state machine engine."""

    def __init__(self, update_queue: queue.Queue, logger: logging.Logger):
        self.queue = update_queue
        self.logger = logger
        self.window_mgr = WindowManager()
        self.automation = Automation()
        self.vision = Vision()
        self.running = False
        self.thread = None
        self.state = "IDLE"

    def start(self):
        """Starts the bot automation loop thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.logger.info("Bot engine started.")

    def stop(self):
        """Stops the bot automation loop."""
        self.running = False
        self.logger.info("Emergency Stop / Pause requested.")

    def _run_loop(self):
        connected, msg = self.window_mgr.connect()
        if not connected:
            self.logger.warning(f"ADB Connection Issue: {msg}")

        while self.running:
            try:
                # Re-verify connection if needed
                frame = self.window_mgr.get_frame()
                if frame is None:
                    connected, msg = self.window_mgr.connect()
                    if not connected:
                        self.logger.warning(f"Failed frame capture / ADB status: {msg}")
                    time.sleep(1.0)
                    continue

                # Run object detection
                detections = self.vision.detect_objects(frame)

                # Update GUI queue with frame summary/status
                self.queue.put({
                    "type": "STATUS_UPDATE",
                    "state": self.state,
                    "detections_count": len(detections),
                    "timestamp": time.time()
                })

                # State Machine Logic
                if self.state == "IDLE":
                    self.state = "SEARCHING_TARGET"
                    self.logger.info("State changed to SEARCHING_TARGET")
                elif self.state == "SEARCHING_TARGET":
                    # Sample logic: check for attack button or targets
                    attack_btn = [d for d in detections if d["label"] == "attack_button"]
                    if attack_btn:
                        cx, cy = attack_btn[0]["center"]
                        self.logger.info(f"Tapping attack button at ({cx}, {cy})")
                        self.automation.tap(cx, cy)
                        self.state = "ATTACKING"
                    else:
                        time.sleep(0.5)

                elif self.state == "ATTACKING":
                    self.logger.info("In attack phase...")
                    time.sleep(2.0)
                    self.state = "IDLE"

                time.sleep(0.2)

            except Exception as e:
                self.logger.error(f"Error in bot loop: {e}")
                time.sleep(1.0)

        self.logger.info("Bot engine stopped.")
