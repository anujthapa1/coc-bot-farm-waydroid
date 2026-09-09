"""
Tkinter GUI running on the main thread, polling the queue every 150ms.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import queue
from typing import Callable
import config


class AppGUI:
    """Tkinter Application Interface."""

    def __init__(self, root: tk.Tk, msg_queue: queue.Queue, on_start: Callable, on_stop: Callable):
        self.root = root
        self.msg_queue = msg_queue
        self.on_start = on_start
        self.on_stop = on_stop

        self.root.title(config.GUI_TITLE)
        self.root.geometry(config.GUI_GEOMETRY)

        self._build_ui()
        self._schedule_queue_poll()

    def _build_ui(self):
        # Controls Frame
        ctrl_frame = ttk.Frame(self.root, padding=10)
        ctrl_frame.pack(fill=tk.X)

        self.start_btn = ttk.Button(ctrl_frame, text="Start Bot", command=self.on_start)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(ctrl_frame, text="Stop Bot (F12)", command=self.on_stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(ctrl_frame, text="Status: STOPPED", font=("Helvetica", 11, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Log Text Box
        log_frame = ttk.LabelFrame(self.root, text="Logs", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(log_frame, state="disabled", wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def _schedule_queue_poll(self):
        self.root.after(config.GUI_POLL_INTERVAL_MS, self._poll_queue)

    def _poll_queue(self):
        while not self.msg_queue.empty():
            try:
                item = self.msg_queue.get_nowait()
                if isinstance(item, str):
                    self._append_log(item)
                elif isinstance(item, dict) and item.get("type") == "STATUS_UPDATE":
                    state = item.get("state", "UNKNOWN")
                    dets = item.get("detections_count", 0)
                    self.status_label.config(text=f"Status: {state} | Objects: {dets}")
            except queue.Empty:
                break
            except Exception:
                pass

        self._schedule_queue_poll()

    def _append_log(self, text: str):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
