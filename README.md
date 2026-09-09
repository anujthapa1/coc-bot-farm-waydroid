# Coc-Auto-Farm — Linux Waydroid Edition

> **High-performance, Linux-native Clash of Clans automation system running inside Weston/Wayland environments controlling Waydroid via pure ADB.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20Mint%20%7C%20Wayland%20%7C%20Waydroid-orange.svg)](https://waydro.id/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

**Coc-Auto-Farm — Linux Waydroid Edition** is a completely refactored, native Linux automation engine for Clash of Clans. Built specifically for Linux Mint, Weston/Wayland compositors, and Waydroid LXC containers, it eliminates all legacy Windows dependencies (`pywinauto`, `pyautogui`, `keyboard`) in favor of direct Android Debug Bridge (ADB) pipe streams, `evdev` event listening, and machine-learning vision pipelines.

By executing low-level ADB commands (`adb exec-out screencap -p` and `adb shell input`), the system achieves low latency frame capturing and pixel-precise touch execution directly within the Waydroid container.

---

## Key Features

- **Pure ADB Communication Protocol**: Zero-latency frame streaming via direct stdout bytes parsing and direct input touch/swipe execution.
- **Linux Native Input Capture**: Asynchronous global emergency stop (F12) using `evdev` listening directly on `/dev/input/` event nodes.
- **AI-Powered Vision Pipeline**: Object detection powered by **Ultralytics YOLOv8** and text extraction powered by **EasyOCR** working on relative coordinate origins `(0, 0)`.
- **Thread-Safe Architecture**: Tkinter GUI running on the main thread, polling a thread-safe `queue.Queue` every 150ms to display state updates and log output.
- **State Machine Bot Engine**: Decoupled automation state machine running in a background thread for non-blocking UI and reliable state transitions.

---

## Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                 LINUX HOST OS                                     |
|                                                                                   |
|  +--------------------+        +---------------------+        +-----------------+ |
|  |   Tkinter GUI      | <====> |  Thread-Safe Queue  | <====> |   Bot Engine    | |
|  |   (Main Thread)    | 150ms  |   (queue.Queue)     |        | (Worker Thread) | |
|  +--------------------+        +---------------------+        +--------+--------+ |
|                                                                        |          |
|  +--------------------+                                                |          |
|  |  Hotkey Manager    | ------------ Global F12 Trigger --------------->|          |
|  |  (evdev /dev/input)|                                                |          |
|  +--------------------+                                                v          |
|                                                            +--------------------+ |
|                                                            |  Vision Engine     | |
|                                                            | (YOLOv8 + EasyOCR) | |
|                                                            +--------------------+ |
|                                                                        |          |
+------------------------------------------------------------------------|----------+
                                                                         |
                                ADB Bridge Protocol                      |
+------------------------------------------------------------------------|----------+
|                                                                        v          |
|  +------------------------------------------------------------------------------+ |
|  |                       WAYDROID CONTAINER (Android LXC)                       | |
|  |                                                                              | |
|  |   `adb exec-out screencap -p` ------------> OpenCV NumPy BGR Array           | |
|  |   `adb shell input tap/swipe` <------------ Touch/Swipe Automation           | |
|  |                                                                              | |
|  |   +----------------------------------------------------------------------+   | |
|  |   |                Clash of Clans (com.supercell.clashofclans)            |   | |
|  |   +----------------------------------------------------------------------+   | |
|  +------------------------------------------------------------------------------+ |
|                                                                                   |
|                             WESTON / WAYLAND COMPOSITOR                           |
+-----------------------------------------------------------------------------------+
```

---

## Technology Stack

- **Operating System / Container**: Linux Mint, Weston / Wayland Compositor, Waydroid (Android LXC)
- **Language**: Python 3.8+
- **Protocol**: Android Debug Bridge (ADB)
- **Computer Vision & ML**: OpenCV, Ultralytics YOLOv8, EasyOCR
- **Input & Event Handling**: `evdev` (Linux input event interface)
- **GUI & Threading**: Tkinter, `threading`, `queue.Queue`

---

## Project Structure

| File | Module Description |
| :--- | :--- |
| `main.py` | Main application entry point; initializes queues, logger, hotkey listener, Tkinter GUI, and clean shutdown hooks. |
| `config.py` | Central configuration file containing ADB host/port settings, paths, timeouts, GUI parameters, and vision thresholds. |
| `window_manager.py` | Manages connection to Waydroid over ADB and streams low-latency screenshots using `adb exec-out screencap -p`. |
| `automation.py` | Executes touch, swipe, text, and key events directly on the Waydroid container via `adb shell input`. |
| `vision.py` | Runs YOLOv8 object detection and EasyOCR text extraction using relative image coordinates `(0, 0)`. |
| `hotkey_manager.py` | Asynchronously scans `/dev/input/event*` devices using `evdev` to handle global F12 emergency stop. |
| `bot.py` | Runs the main automation state machine loop inside a dedicated background thread. |
| `gui.py` | Renders the Tkinter interface on the main thread and polls the event queue every 150ms for UI/log updates. |
| `logger.py` | Provides thread-safe logging supporting stdout, log files, and GUI queue streams. |
| `utils.py` | Helper module for subprocess execution and decoding raw screencap bytes into OpenCV BGR NumPy arrays. |
| `requirements.txt` | Defines all required Python package dependencies. |

---

## Installation & Setup

### Prerequisites

Ensure system dependencies and Python 3 are installed on your Linux Mint host:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk adb
```

### Repository Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/coc-auto-farm-waydroid.git
   cd coc-auto-farm-waydroid
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Ensure your user belongs to the `input` group to allow `evdev` access to `/dev/input/`:
   ```bash
   sudo usermod -aG input $USER
   ```
   *(Re-login or restart session for group changes to take effect)*

---

## Waydroid + ADB Configuration

1. Launch Waydroid container and verify IP address:
   ```bash
   waydroid status
   ```

2. Connect ADB to Waydroid (default IP is typically `192.168.240.112` or available local device):
   ```bash
   adb connect 192.168.240.112:5555
   adb devices
   ```

3. Configure custom IP in `config.py` or export environment variables:
   ```bash
   export ADB_HOST="192.168.240.112"
   export ADB_PORT=5555
   ```

---

## How to Run

Launch the application using Python 3:

```bash
python3 main.py
```

Click **Start Bot** in the GUI to initiate the automation loop. Click **Stop Bot (F12)** or press **F12** globally at any time to execute an emergency stop.

---

## GUI & Threading Architecture

The application enforces strict thread separation:
- **Main Thread**: Runs the Tkinter GUI event loop. It schedules a periodic polling function (`root.after(150, self._poll_queue)`) to process queued messages without blocking the user interface.
- **Worker Thread**: The `BotEngine` runs inside a background `threading.Thread`. It communicates status changes and object detection counts back to the GUI using thread-safe `queue.Queue` objects.
- **Hotkey Listener Thread**: `HotkeyManager` monitors `/dev/input/` events in a separate daemon thread to catch F12 keypress events instantly.

---

## YOLOv8 + EasyOCR Vision Pipeline

1. **Frame Capture**: `WindowManager` streams PNG bytes directly from stdout via `adb exec-out screencap -p`.
2. **Numpy Decoding**: `utils.parse_screencap_bytes()` decodes bytes into OpenCV BGR numpy arrays in-memory without disk I/O.
3. **Object Detection**: `Vision.detect_objects()` feeds the image matrix to the YOLOv8 model, extracting bounding boxes, labels, and center coordinates.
4. **OCR Extraction**: `Vision.extract_text()` crops region-of-interest (ROI) bounding boxes and extracts resource numbers using EasyOCR.
5. **Relative Origin**: All detected coordinates operate on a `(0, 0)` origin matching the screen width and height of the Waydroid Android display.

---

## F12 Emergency Stop

Emergency stop is handled globally across Linux desktop environments via `evdev`:
- `hotkey_manager.py` inspects `/dev/input/event*` devices for keyboard capabilities.
- When `KEY_F12` press event (`value == 1`) is detected, it instantly triggers `bot.stop()`.
- No active desktop window focus is required for the emergency stop hotkey to function.

---

## Troubleshooting

- **Permission Denied on `/dev/input/event*`**:
  Add your user to the `input` group (`sudo usermod -aG input $USER`) or run with appropriate device permissions.
- **ADB Connection Failed**:
  Ensure Waydroid is running (`waydroid status`) and verify connectivity using `adb connect <IP>:5555`.
- **YOLO Model Not Found**:
  Specify the YOLO model file path via environment variable `YOLO_MODEL_PATH="path/to/model.pt"` or update `config.py`.

---

## Development & Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Verify syntax and changes:
   ```bash
   python3 -m py_compile *.py
   ```
4. Commit your changes and submit a Pull Request.

---

## Disclaimer

This software is for educational, research, and technical demonstration purposes only. Use of automated bots in Clash of Clans may violate Supercell's Terms of Service. Use at your own risk.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
