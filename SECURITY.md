# Security Policy

## Reporting

If you discover a vulnerability or privacy issue, please open a **GitHub issue** with **SECURITY** in the title or email the maintainers if you prefer not to disclose publicly. Avoid publishing exploit details; a maintainer will coordinate next steps and timelines.

## Data & privacy

- The app stores presets and last state locally in `crosshair_presets.json` and `crosshair_last_state.json` next to the script. No telemetry is collected.
- No network access or elevated privileges are used by default.

## Permissions & risks

- The overlay is an always‑on‑top window. Some apps (especially games) may render above it; behavior varies across OS/WM/GPU.
- Transparency relies on Tk/window manager features; test on your system before streaming/competitive use.

## Responsible use & Terms

- This project is **not intended for hacking, cheating, or bypassing anti‑cheat** in games or other software.
- Using overlays may violate a product’s **Terms of Service**/**EULA**. **You are solely responsible** for compliance with any third‑party terms and **accept all risk** (including bans/account actions). The authors/maintainers **assume no liability** for misuse.

## Supported versions

Target: **Python 3.8+** with **Tk 8.6+** on Windows/macOS/Linux.
