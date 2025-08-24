# Install & Run — Crosshair Overlay (Tkinter)

This app is a **Python Tkinter GUI** that runs on **Windows, macOS, and Linux**. It uses a transparent‑color technique for the overlay; support depends on your OS/Tk build and window manager.

> **Compatibility:** Python **3.8+**, Tk **8.6+**.

## 1) Get the code

```bash
git clone https://github.com/<you>/crosshair-overlay.git
cd crosshair-overlay
```

## 2) Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

## 3) Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt 
```

### Linux: install Tkinter (if missing)

On Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

On Fedora:
```bash
sudo dnf install -y python3-tkinter
```

If you’re on Wayland and transparency doesn’t work, consider trying an X11 session or lower the in‑app **Opacity**.

### macOS notes

- Tkinter is included with the Python.org installer. If using Homebrew Python, you may need `brew install tcl-tk`
  and ensure your Python links against it (see Homebrew docs).
- Transparency support can vary by Tk build; if a white box appears, reduce **Opacity**.

### Windows notes

- No extra setup should be required. Ensure your Python includes Tk. If transparency behaves oddly under certain GPUs, lowering **Opacity** helps.

## 4) Run the app

```bash
python crosshair_overlay.py
```

## 5) Uninstall / cleanup

Just remove the cloned folder. Preset/state files live next to `crosshair_overlay.py` as:
- `crosshair_presets.json`
- `crosshair_last_state.json`
