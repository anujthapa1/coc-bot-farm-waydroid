````markdown
# Coc-Auto-Farm (Linux Waydroid Edition)

A thread-safe Python automation framework for **Clash of Clans** running inside **Waydroid on Linux**. The project combines computer vision, OCR, ADB-based Android control, and Linux input-event monitoring to automate repetitive in-game tasks.

> **Disclaimer:** This project is intended for educational, research, and personal automation experiments. Automated gameplay may violate the terms of service of the game or related services. Use it at your own risk.

---

## Features

- 🤖 **YOLOv8 object detection** for identifying game elements.
- 👁️ **EasyOCR** for reading resource counts and UI text.
- 🖼️ **OpenCV** for screenshot processing and computer vision.
- 📱 **Waydroid** for running the Android version of Clash of Clans on Linux.
- 🔌 **ADB Pipe automation** using:
  - `exec-out screencap` for screenshots.
  - `input tap` for touch interaction.
- 🧵 **Thread-safe automation architecture** for coordinating vision, GUI, and automation tasks.
- ⌨️ **F12 emergency stop** using Linux `evdev`.
- 🖥️ GUI-based configuration for resource thresholds and automation settings.
- 🐧 Designed for **Linux Mint + Weston/Wayland** environments.

---

# Architecture & Technology Stack

The application is divided into several independent modules responsible for GUI management, computer vision, Android interaction, window management, and emergency controls.

```text
┌───────────────────────────────────────────────┐
│                  Linux Mint                   │
│              Weston / Wayland                 │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │                 Waydroid                │  │
│  │                                         │  │
│  │          Clash of Clans                │  │
│  │                                         │  │
│  └──────────────────┬──────────────────────┘  │
│                     │                         │
│                  ADB Pipe                     │
│                     │                         │
│          ┌──────────▼──────────┐              │
│          │      automation.py  │              │
│          │  screencap / taps   │              │
│          └──────────┬──────────┘              │
│                     │                         │
│          ┌──────────▼──────────┐              │
│          │       vision.py     │              │
│          │ YOLOv8 / OCR / CV   │              │
│          └──────────┬──────────┘              │
│                     │                         │
│          ┌──────────▼──────────┐              │
│          │        bot.py       │              │
│          │ Automation Logic    │              │
│          └──────────┬──────────┘              │
│                     │                         │
│       ┌─────────────┴─────────────┐           │
│       │                           │           │
│   gui.py                  hotkey_manager.py   │
│       │                           │           │
│  Configuration                 F12 Stop       │
│       │                           │           │
│       └─────────────┬─────────────┘           │
│                     │                         │
│              window_manager.py                │
│                                               │
└───────────────────────────────────────────────┘
````

## Technology Stack

| Component            | Technology                  |
| -------------------- | --------------------------- |
| Operating System     | Linux Mint                  |
| Display Server       | Weston / Wayland            |
| Android Runtime      | Waydroid                    |
| Android Control      | ADB                         |
| Screenshot Interface | `adb exec-out screencap`    |
| Touch Interface      | `adb shell input tap`       |
| Object Detection     | Ultralytics YOLOv8          |
| OCR                  | EasyOCR                     |
| Image Processing     | OpenCV                      |
| GUI                  | Python Tkinter              |
| Linux Input Listener | `evdev`                     |
| Automation Language  | Python                      |
| Configuration        | Python configuration module |

---

# Requirements

Before installation, make sure the system has:

* Linux Mint
* Wayland/Weston support
* Waydroid
* Python 3
* ADB
* Working Android/Waydroid networking
* A YOLOv8 model compatible with the project
* Sufficient CPU/RAM for computer vision processing

Recommended:

* 8 GB RAM or more
* SSD storage
* Working GPU acceleration where available
* Stable Waydroid networking

---

# Installation

## 1. Install System Dependencies

Update the package database:

```bash
sudo apt update
```

Install the required system packages:

```bash
sudo apt install python3-tk libgl1-mesa-glx adb weston wmctrl
```

Verify ADB:

```bash
adb version
```

Verify Weston:

```bash
weston --version
```

Verify Python:

```bash
python3 --version
```

---

# 2. Set Up Waydroid

Install and configure Waydroid according to your Linux distribution's Waydroid setup.

After installation, verify that the Waydroid container is running:

```bash
waydroid status
```

A working installation should report the container/session as running.

Start the Waydroid session when required:

```bash
waydroid session start
```

You can also launch the Waydroid UI:

```bash
waydroid show-full-ui
```

---

# 3. Connect ADB to Waydroid

The automation system communicates with Android through ADB.

Connect to the Waydroid ADB endpoint:

```bash
adb connect 192.168.240.112:5555
```

Check connected devices:

```bash
adb devices
```

You should see a device similar to:

```text
List of devices attached
192.168.240.112:5555    device
```

If the device appears as `device`, ADB communication is ready.

---

# 4. Test ADB Screenshot Capture

Before running the bot, verify that screenshots can be obtained through ADB:

```bash
adb -s 192.168.240.112:5555 exec-out screencap -p > screenshot.png
```

Open the resulting image:

```bash
xdg-open screenshot.png
```

If the screenshot contains the Waydroid/Clash of Clans display, the ADB screenshot pipeline is working.

---

# 5. Test ADB Touch Input

ADB can send touch events using:

```bash
adb -s 192.168.240.112:5555 shell input tap X Y
```

For example:

```bash
adb -s 192.168.240.112:5555 shell input tap 500 500
```

Replace `X` and `Y` with the desired screen coordinates.

> **Important:** Coordinates depend on the Waydroid display resolution and scaling configuration.

---

# 6. Configure `/dev/input/` Permissions

The emergency F12 listener uses Linux input devices through the `evdev` library.

Add your current user to the `input` group:

```bash
sudo usermod -aG input $USER
```

Log out and log back in, or reboot the system for the group membership to take effect.

Verify membership:

```bash
groups
```

You should see:

```text
input
```

You can also inspect available input devices:

```bash
ls -l /dev/input/
```

---

# 7. Create the Python Virtual Environment

Navigate to the project directory:

```bash
cd Coc-Auto-Farm
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, the shell should display something similar to:

```text
(venv) user@computer:~/Coc-Auto-Farm$
```

---

# 8. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 9. Install Python Dependencies

Install all Python dependencies from the project's requirements file:

```bash
pip install -r requirements.txt
```

The dependency list should include the packages required by the project, such as:

* Ultralytics
* OpenCV
* EasyOCR
* PyTorch
* NumPy
* Pillow
* Tkinter-compatible GUI components
* `evdev`

If `evdev` needs to be installed separately:

```bash
pip install evdev
```

---

# Project Structure

A typical project structure is:

```text
Coc-Auto-Farm/
│
├── main.py
├── config.py
├── window_manager.py
├── automation.py
├── hotkey_manager.py
├── vision.py
├── bot.py
├── gui.py
│
├── requirements.txt
├── README.md
│
├── models/
│   └── ...
│
├── screenshots/
│   └── ...
│
└── venv/
    └── ...
```

---

# Module Breakdown

## `main.py`

The primary application entry point.

Responsibilities include:

* Initializing the application.
* Loading configuration.
* Starting the GUI.
* Initializing the bot.
* Starting required worker threads.
* Coordinating shutdown.

Run the application through:

```bash
python main.py
```

---

## `config.py`

Contains project configuration and automation parameters.

Typical configuration includes:

* ADB device address.
* Screen dimensions.
* Resource thresholds.
* Detection confidence values.
* Timing parameters.
* Automation delays.
* File/model paths.
* Bot behavior settings.

Example:

```python
ADB_DEVICE = "192.168.240.112:5555"

GOLD_THRESHOLD = 100000
ELIXIR_THRESHOLD = 100000
DARK_ELIXIR_THRESHOLD = 1000

YOLO_CONFIDENCE = 0.50
```

The actual values should be adjusted according to the project implementation.

---

## `window_manager.py`

Handles interaction with the Linux desktop/window environment.

Responsibilities may include:

* Detecting the Waydroid window.
* Bringing Waydroid into focus.
* Positioning the window.
* Managing window dimensions.
* Working with `wmctrl`.
* Supporting Weston/Wayland-based environments where possible.

This module helps ensure that the Android display is in a predictable state before automation begins.

---

## `automation.py`

Provides the low-level Android control interface.

The primary communication mechanism is ADB.

### Screenshot

Screenshots are captured using:

```bash
adb exec-out screencap -p
```

### Touch Input

Touch events are sent using:

```bash
adb shell input tap X Y
```

The Python implementation should centralize ADB communication in this module rather than duplicating ADB commands throughout the project.

---

## `hotkey_manager.py`

Responsible for global emergency controls.

The module uses:

```text
evdev
```

to listen for Linux input events.

The primary emergency control is:

```text
F12 → Stop automation
```

This is particularly important because the automation process may continue operating while another application/window has focus.

---

## `vision.py`

Contains computer vision functionality.

The module combines:

### YOLOv8

Ultralytics YOLOv8 is used for object detection.

Potential detections include:

* Game UI elements.
* Buildings.
* Buttons.
* Resources.
* Other objects required by the automation logic.

### EasyOCR

EasyOCR is used to extract text and numerical values from screenshots.

For example:

```text
Gold:       1,250,000
Elixir:     980,000
Dark:       12,500
```

### OpenCV

OpenCV provides image processing functionality such as:

* Screenshot conversion.
* Cropping.
* Resizing.
* Thresholding.
* Image preprocessing.
* Region-of-interest extraction.

---

## `bot.py`

Contains the higher-level automation logic.

It combines the functionality of:

```text
automation.py
       ↓
vision.py
       ↓
bot.py
```

The bot can:

1. Capture the current screen.
2. Analyze the screenshot.
3. Detect relevant objects.
4. Read resource values.
5. Determine the next action.
6. Send ADB input.
7. Wait for the game state to change.
8. Repeat until stopped.

Thread synchronization should be used where multiple workers access shared state.

---

## `gui.py`

Provides the graphical user interface.

The GUI allows the user to configure automation settings without manually editing configuration files.

Potential settings include:

* Gold threshold.
* Elixir threshold.
* Dark Elixir threshold.
* Automation state.
* Detection settings.
* Start/stop controls.
* Current bot status.

The GUI should remain responsive while automation runs in background threads.

---

# Running the Project

## 1. Start Weston

The project is designed to operate with Waydroid under a Weston/Wayland environment.

Start Weston using your configured Weston setup.

Depending on your environment, this may be launched from a terminal or desktop session.

> The exact Weston launch command can vary depending on whether Weston is being used nested inside an existing desktop environment, through a dedicated TTY, or as the primary compositor.

---

# 2. Start Waydroid

Check the Waydroid state:

```bash
waydroid status
```

Start the session:

```bash
waydroid session start
```

Launch the full UI:

```bash
waydroid show-full-ui
```

Open **Clash of Clans** inside Waydroid.

---

# 3. Connect ADB

Connect to the configured Waydroid address:

```bash
adb connect 192.168.240.112:5555
```

Verify:

```bash
adb devices
```

---

# 4. Activate the Virtual Environment

From the project directory:

```bash
source venv/bin/activate
```

---

# 5. Start the Automation Application

Run:

```bash
python main.py
```

The GUI should appear.

Configure the desired thresholds and automation settings before starting the bot.

---

# Resource Threshold Configuration

Resource thresholds determine when the automation logic should perform or avoid specific actions.

For example:

```python
GOLD_THRESHOLD = 100000
ELIXIR_THRESHOLD = 100000
DARK_ELIXIR_THRESHOLD = 1000
```

These values are examples only.

The preferred method is to configure the thresholds through the GUI when supported.

If a particular setting is not exposed in the GUI, modify:

```text
config.py
```

After changing configuration values, restart the application:

```bash
python main.py
```

---

# Emergency Stop

The project provides a global emergency stop using:

```text
F12
```

Pressing **F12** should signal the automation system to stop its active operations.

This is implemented through Linux input events using `evdev`.

The emergency stop is designed to provide a quick way to terminate automation if:

* The bot behaves unexpectedly.
* ADB input becomes incorrect.
* Vision detection produces an incorrect result.
* The game enters an unexpected state.
* The user needs to regain manual control.

Always keep the F12 emergency stop available while testing new automation behavior.

---

# Thread Safety

The project is designed around thread-safe automation.

A typical execution model can be represented as:

```text
                    Main Thread
                        │
                  ┌─────┴─────┐
                  │    GUI    │
                  └─────┬─────┘
                        │
                 Shared Bot State
                        │
          ┌─────────────┴─────────────┐
          │                           │
     Bot Worker                  Hotkey Worker
          │                           │
    Vision + ADB                    evdev
          │                           │
          └─────────────┬─────────────┘
                        │
                   Stop Event
```

Shared state should be protected using appropriate synchronization mechanisms such as:

```python
threading.Lock
```

and/or:

```python
threading.Event
```

An emergency stop event is especially useful because it allows worker threads to terminate cleanly without relying on unsafe thread termination.

---

# Troubleshooting

## ADB Connection Drops

### Check the connection

Run:

```bash
adb devices
```

If the device is missing, reconnect:

```bash
adb connect 192.168.240.112:5555
```

If ADB reports an existing/stale connection, restart the ADB server:

```bash
adb kill-server
adb start-server
adb connect 192.168.240.112:5555
```

Then verify:

```bash
adb devices
```

### Check Waydroid

```bash
waydroid status
```

If the session/container is not running, start it:

```bash
waydroid session start
```

Then reconnect ADB.

---

# `/dev/input/` Permission Denied

If the application reports an error similar to:

```text
Permission denied: '/dev/input/eventX'
```

add your user to the `input` group:

```bash
sudo usermod -aG input $USER
```

Then log out and log back in.

Verify:

```bash
groups
```

You should see:

```text
input
```

Check the device permissions:

```bash
ls -l /dev/input/event*
```

Avoid running the entire automation application as root unless absolutely necessary. The preferred approach is to configure appropriate group permissions for the input devices.

---

# F12 Does Not Work

If F12 is not detected:

1. Verify that your user belongs to the `input` group.
2. Log out and log back in after changing group membership.
3. Check that `/dev/input/event*` devices are accessible.
4. Make sure another process is not exclusively consuming the keyboard event.
5. Confirm that the correct keyboard event device is being monitored.

You can inspect available devices using:

```bash
ls /dev/input/
```

---

# Waydroid Resolution / Scaling Problems

Vision-based automation depends heavily on consistent screen coordinates.

If Waydroid is running at an unexpected resolution, YOLO detection regions and ADB tap coordinates may no longer match the expected positions.

Symptoms include:

* Incorrect tap locations.
* Objects not detected.
* OCR returning incorrect values.
* Buttons appearing outside expected regions.
* GUI scaling not matching the model's expected input.

Check the current Android display configuration:

```bash
adb shell wm size
```

You can also inspect density:

```bash
adb shell wm density
```

If the display has been manually overridden, restore the appropriate configuration or configure the expected resolution.

For example:

```bash
adb shell wm size reset
```

and:

```bash
adb shell wm density reset
```

Restart Waydroid after making major display configuration changes if necessary.

> **Important:** YOLO detection and coordinate-based ADB input should be tested again whenever the Waydroid resolution or display scaling changes.

---

# Computer Vision Troubleshooting

## YOLOv8 Detection Problems

If objects are not detected:

* Verify the correct model file is loaded.
* Check the model's confidence threshold.
* Confirm the screenshot resolution.
* Ensure the screenshot contains the expected game interface.
* Verify that the training data matches the current game UI.

A confidence threshold that is too high may cause valid objects to be ignored.

---

## EasyOCR Problems

If OCR values are incorrect:

* Verify the crop/region of interest.
* Increase screenshot resolution where appropriate.
* Preprocess the image using OpenCV.
* Check that the selected OCR language configuration is correct.
* Avoid reading text while the game is transitioning between screens.

OCR accuracy depends heavily on image quality and the selected region.

---

# Development Workflow

A recommended development workflow is:

```text
1. Start Waydroid
        ↓
2. Connect ADB
        ↓
3. Capture screenshot
        ↓
4. Verify resolution
        ↓
5. Test YOLO detection
        ↓
6. Test OCR
        ↓
7. Test individual ADB actions
        ↓
8. Test bot logic
        ↓
9. Test emergency stop
        ↓
10. Run complete automation
```

Always test individual components before enabling the complete automation loop.

---

# Safety Recommendations

Before running the automation unattended:

* Confirm the correct ADB device is connected.
* Confirm the Waydroid resolution.
* Test screenshot capture.
* Test object detection.
* Test OCR.
* Test individual touch actions.
* Verify F12 emergency stop.
* Monitor CPU and memory usage.
* Keep logs enabled where possible.
* Test with conservative thresholds first.

Do not assume that computer vision will always produce a correct result. Changes to the game's interface, animations, popups, network conditions, or screen scaling can affect detection and automation.

---

# Example Command Sequence

A typical startup sequence is:

```bash
# Enter project directory
cd Coc-Auto-Farm

# Activate virtual environment
source venv/bin/activate

# Start Waydroid
waydroid session start

# Connect ADB
adb connect 192.168.240.112:5555

# Verify device
adb devices

# Start the application
python main.py
```

---

# Stopping the Application

The preferred emergency mechanism is:

```text
F12
```

For normal application shutdown, use the GUI's stop/exit controls if available.

If the application becomes unresponsive, terminate the Python process from a terminal:

```bash
pkill -f "python main.py"
```

Use forced termination only when normal shutdown mechanisms fail.

---

# Configuration Checklist

Before starting automation, verify:

* [ ] Waydroid is running.
* [ ] Clash of Clans is open.
* [ ] ADB is connected.
* [ ] `adb devices` shows the expected device.
* [ ] Screenshot capture works.
* [ ] Screen resolution matches the expected configuration.
* [ ] YOLOv8 model is available.
* [ ] EasyOCR is installed.
* [ ] `/dev/input/` is accessible.
* [ ] User belongs to the `input` group.
* [ ] F12 emergency stop works.
* [ ] Resource thresholds are configured.
* [ ] Python virtual environment is activated.

---

# License

This project is released under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Coc-Auto-Farm contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# Credits

This project makes use of the following technologies and open-source projects:

* **Python** — Core automation language.
* **Waydroid** — Android runtime environment for Linux.
* **ADB (Android Debug Bridge)** — Android communication and input control.
* **Ultralytics YOLOv8** — Object detection.
* **EasyOCR** — Optical character recognition.
* **OpenCV** — Computer vision and image processing.
* **evdev** — Linux input event handling.
* **Tkinter** — Graphical user interface.
* **Weston** — Wayland compositor.
* **wmctrl** — Linux window management.

---

# Disclaimer

Coc-Auto-Farm is an independent automation project and is **not affiliated with, endorsed by, or sponsored by Supercell**.

Clash of Clans and related trademarks belong to their respective owners.

Users are responsible for ensuring that their use of automation complies with the applicable game's terms of service and other applicable rules.

---

## Project Summary

**Coc-Auto-Farm (Linux Waydroid Edition)** combines:

```text
Linux Mint
    +
Weston / Wayland
    +
Waydroid
    +
ADB
    +
OpenCV
    +
YOLOv8
    +
EasyOCR
    +
Python Threading
    +
evdev
```

to provide a modular computer-vision-driven automation environment for Android applications running through Waydroid.

The architecture separates **Android control**, **computer vision**, **OCR**, **bot logic**, **GUI configuration**, **window management**, and **emergency input handling**, making the project easier to maintain, test, and extend.

```
```
