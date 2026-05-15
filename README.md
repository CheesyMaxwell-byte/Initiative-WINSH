# 🛡️ WinShield

**A Proactive, Zero-Trust Endpoint Security Framework for Windows inspired by Linux AppArmor.**

Unlike traditional anti-virus software that relies on reactive signature databases to identify malware, **WinShield** enforces strict **Mandatory Access Control (MAC)**. It doesn't care *who* a program is—if it is not explicitly permitted by your profile rules to perform an action, WinShield blocks it instantly with a hard *"Nope, you can forget about that!"*

---

## ✨ Features

*   **Zero-Trust Whitelisting:** Perfect protection against Zero-Day exploits and Ransomware. Unknown applications cannot write to or modify protected directories by default.
*   **Intelligent Complain (Learning) Mode:** Switch to Learning Mode to monitor your daily workflows. WinShield automatically logs trusted applications and builds custom JSON security profiles for you.
*   **Enforce (Protection) Mode:** Armed and dangerous. Any unauthorized process attempting an illegal file modification is terminated in real-time.
*   **Immersive TUI & CLI:** Managing your endpoints feels lightning-fast with a dedicated Terminal User Interface (powered by `Textual`) and system-wide commands.
*   **Central Intelligence Hub:** Seamless API connection to a global WinShield server to securely stream real-time threat telemetry and pull community-verified application profiles.

---

## 🚀 Quick Start & Architecture

WinShield is bundled into a single, standalone executable (`winsh.exe`) for frictionless deployment across enterprise networks.

### System-Wide Command Line Control (WTC)
Once registered via the global system bridge, you can orchestrate your defense from any PowerShell or Command Prompt with the native `manage` entry point:

```bash
# Launch the interactive Cyberpunk TUI Dashboard
manage WINSH

# Manually add a trusted application to the guest list
manage WINSH allow vlc.exe

# Instantly strip permissions from a process
manage WINSH block cmd.exe

# Fetch a community-approved profile from the Central Server
manage WINSH update office_update_2026

# Pull a security threat audit report from the last 24 hours
manage WINSH report
```

---

## 🛠️ Technology Stack

*   **Core Logic & Monitoring:** Python 3.13, `psutil`, `watchdog`
*   **Terminal Interface:** `textual` (CSS-driven Terminal User Interface)
*   **Server Backend:** `FastAPI` + `Uvicorn`
*   **Compilation:** `PyInstaller` (Monolithic standalone Windows binary packaging)

---

## 📁 Repository Structure

```text
├── winsh.py             # Master core engine & CLI router
├── winsh_tui.py         # Modular Textual UI dashboard
├── winshield_server.py  # FastAPI cloud/local API for profile updates
├── manage.bat           # System32 orchestration bridge
└── README.md            # You are here
```

---

## 🛡️ Resilience & Fail-Safe

If your central server undergoes maintenance or network loss occurs, WinShield gracefully drops back to local protection and handles communication dropouts natively with standard system tracking:

```text
======================================================================
🚨 Error 289: Connection Error.
   Central server could not be reached.
   Your current version of WinShield: [VERSION]
======================================================================
```
