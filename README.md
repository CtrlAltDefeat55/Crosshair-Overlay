# Crosshair Overlay (Tkinter)

A lightweight, always-on-top **crosshair overlay** for Windows/macOS/Linux built with **Tkinter**. Control it with a side panel: choose crosshair **type**, **color**, **size**, and **opacity**; **lock/unlock** and drag to position; **reset** to center; and **save/load presets** that persist across runs.

> **Core script:** `crosshair_overlay.py`  
> **Data files (auto-created):** `crosshair_presets.json`, `crosshair_last_state.json` (stored next to the script)

---

## ⚠️ Legal & Acceptable Use

- This tool is **not intended for hacking, cheating, or bypassing anti‑cheat systems**.  
- Using overlays in **games or other software may violate their Terms of Service or EULAs**. You are solely responsible for how you use this tool.  
- **The authors/maintainers are not responsible** for bans, account actions, or any consequences that result from misuse or ToS violations.  
- Intended uses include **accessibility**, **UI testing**, **training/demonstration**, and **non‑competitive** contexts where overlays are allowed.

---

## Table of Contents

- [Features](#features)
- [User Interface](#user-interface)
- [Installation](#installation)
- [Usage](#usage)
  - [Start/Stop & status](#startstop--status)
  - [Move, lock & reset](#move-lock--reset)
  - [Crosshair settings](#crosshair-settings)
  - [Presets](#presets)
- [Known limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Features

- **10 crosshair types:** Standard, Circle, Dot, Plus, X, Cross, Target, Square, Diamond, Arrow
- **Color, Size, Opacity** sliders/inputs with validation
- **Topmost** transparent overlay window (no borders, optional drag-to-move)
- **Lock/Unlock** to fix position vs. drag
- **Reset to center** of the current screen
- **Presets**: create, save, delete, and auto-load last state (`crosshair_presets.json`, `crosshair_last_state.json`)

## User Interface

<img width="397" height="729" alt="UI overlay" src="https://github.com/user-attachments/assets/72f96f03-2f82-45ba-99b8-57e700ecef5f" />


## Installation

Quick start is below. See **[INSTALL.md](INSTALL.md)** for step-by-step OS-specific setup and Tkinter tips.

```bash
git clone https://github.com/<you>/crosshair-overlay.git
cd crosshair-overlay

# (Optional) create a virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt  # no third-party deps; safe to skip

# Run
python crosshair_overlay.py
```

---

## Usage

### Start/Stop & status
- Click **Start Overlay** to show the crosshair window (it’s borderless, always-on-top).
- Status indicator turns **green** when running; **red** when stopped.
- Click **Stop Overlay** to hide it without closing the controller.

### Move, lock & reset
- **Unlock Position** to enable **dragging** (click & drag anywhere on the overlay).
- **Lock Position** to disable dragging.
- **Reset Position** re-centers the overlay on the main display.

### Crosshair settings
- Choose **Type**, **Color**, **Size**, **Opacity** from the controls.
- Changes apply live while the overlay is running.
- The overlay canvas scales with **Size** (`window_size = size * 4`) for visibility.

### Presets
- Create a new preset by entering a name and clicking **Create**.
- Use the dropdown to select a preset; **Save** to update it or **Delete** to remove it.
- Your last selected preset or ad‑hoc settings are saved to `crosshair_last_state.json` automatically on exit.

---

## Known limitations

- **Transparency:** The overlay uses a transparent color trick (`wm_attributes("-transparentcolor", "white")`).  
  - **Windows:** Works as intended.  
  - **macOS/Linux:** Support varies by Tk build/window manager; if unsupported, you may see a white square around the crosshair. Reduce **Opacity** as a workaround.
- **Fullscreen apps/games:** Some apps render above topmost windows; behavior differs by GPU/OS.
- **HiDPI scaling:** On unusual DPI settings, you may need to tweak **Size** to taste.

---

## Troubleshooting

- **“No module named tkinter”** – Install Tk for your Python:  
  - Ubuntu/Debian: `sudo apt-get install python3-tk`  
  - Fedora: `sudo dnf install python3-tkinter`  
  - macOS (Homebrew Python): `brew install python-tk` (or install an official Python that bundles Tk)  
- **Overlay not transparent** – Your Tk/window manager may not support `-transparentcolor`; lower **Opacity** instead.
- **Overlay not draggable** – Click **Unlock Position** first, then drag.
- **Nothing draws** – Ensure the overlay window is visible (Start Overlay) and you didn’t set **Size** to 0.

---

## Contributing

Contributions are welcome! Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** for style, testing, and PR guidelines.
