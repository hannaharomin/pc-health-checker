# 🖥️ PC Health Checker

A Python-based IT diagnostic tool that checks your PC's health and displays results in plain English through a terminal report or web dashboard.

## What It Checks
- 💾 Disk space (how full your hard drive is)
- ⚙️ CPU usage (how hard your processor is working)
- 🧠 Memory / RAM usage
- 🌐 Internet connection
- ⏱️ System uptime (how long since last restart)
- 🌡️ CPU temperature (Linux/some systems)

---

## Setup

### Step 1 — Install the required library
```bash
pip install psutil
```

### Step 2 — Run from the command line (simple mode)
```bash
# Mac/Linux
python3 health_checker.py

# Windows
python health_checker.py
```
This prints a plain-text report right in your terminal.

### Step 3 — Run with the web dashboard
```bash
# Mac/Linux
python3 server.py

# Windows
python server.py
```
Then open your browser and go to:
```
http://localhost:8000/index.html
```
Click **Run Health Scan** to see your results!

---

## Files
| File | What it does |
|------|-------------|
| `health_checker.py` | All the health check logic |
| `server.py` | Tiny web server (connects Python to the HTML page) |
| `index.html` | The visual dashboard in your browser |

---

## Skills Demonstrated (for your portfolio)
- Python scripting with `psutil` and standard library modules
- Building a REST API with Python's built-in HTTP server
- Connecting a frontend (HTML/JS) to a backend (Python)
- Parsing and serving JSON data
- Real IT diagnostic tasks: disk, CPU, memory, network checks

---

## Ideas to Extend This Project
- Add email alerts when something hits "critical"
- Log results to a JSON file to track trends over time
- Package it as a desktop app with `tkinter`
- Add more checks: battery level, running processes, open ports
