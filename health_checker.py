import psutil
import platform
import datetime
import socket
import json


def check_disk_space():
    """Check how full your hard drive is."""
    disk = psutil.disk_usage('/')
    percent_used = disk.percent
    free_gb = round(disk.free / (1024 ** 3), 1)
    total_gb = round(disk.total / (1024 ** 3), 1)

    if percent_used < 70:
        status = "good"
        message = f"Plenty of space left. {free_gb} GB free out of {total_gb} GB."
    elif percent_used < 90:
        status = "warning"
        message = f"Getting full. Only {free_gb} GB free out of {total_gb} GB. Consider cleaning up files."
    else:
        status = "critical"
        message = f"Almost full! Only {free_gb} GB free. Please delete files soon."

    return {
        "name": "Disk Space",
        "icon": "💾",
        "status": status,
        "value": f"{percent_used}% used",
        "message": message
    }


def check_cpu():
    """Check how hard your CPU is working."""
    # Wait 1 second to get an accurate reading
    cpu_percent = psutil.cpu_percent(interval=1)

    if cpu_percent < 60:
        status = "good"
        message = f"CPU is relaxed at {cpu_percent}% usage. All good!"
    elif cpu_percent < 85:
        status = "warning"
        message = f"CPU is working hard at {cpu_percent}%. You may have too many programs open."
    else:
        status = "critical"
        message = f"CPU is maxed out at {cpu_percent}%! Close some programs right away."

    return {
        "name": "CPU Usage",
        "icon": "⚙️",
        "status": status,
        "value": f"{cpu_percent}%",
        "message": message
    }


def check_memory():
    """Check how much RAM is being used."""
    mem = psutil.virtual_memory()
    percent_used = mem.percent
    available_gb = round(mem.available / (1024 ** 3), 1)

    if percent_used < 70:
        status = "good"
        message = f"Memory is fine. {available_gb} GB available."
    elif percent_used < 90:
        status = "warning"
        message = f"Memory is getting low ({percent_used}% used). Try closing unused apps."
    else:
        status = "critical"
        message = f"Almost out of memory ({percent_used}% used)! Close programs immediately."

    return {
        "name": "Memory (RAM)",
        "icon": "🧠",
        "status": status,
        "value": f"{percent_used}% used",
        "message": message
    }


def check_internet():
    """Check if the computer can reach the internet using a socket connection."""
    # We try connecting to multiple well-known servers on port 80 (HTTP)
    # This is just a "knock on the door" — no full web request needed
    test_hosts = [
        ("8.8.8.8", 53),       # Google DNS
        ("1.1.1.1", 53),       # Cloudflare DNS
        ("208.67.222.222", 53) # OpenDNS
    ]

    for host, port in test_hosts:
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            return {
                "name": "Internet",
                "icon": "🌐",
                "status": "good",
                "value": "Connected",
                "message": "Internet connection is working normally."
            }
        except Exception:
            continue  # Try the next host

    # All hosts failed
    return {
        "name": "Internet",
        "icon": "🌐",
        "status": "critical",
        "value": "No connection",
        "message": "Cannot reach the internet. Check your Wi-Fi or cable connection."
    }


def check_uptime():
    """Check how long the computer has been running."""
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.datetime.now().timestamp() - boot_time
    uptime_hours = uptime_seconds / 3600

    days = int(uptime_hours // 24)
    hours = int(uptime_hours % 24)

    if days > 0:
        value = f"{days}d {hours}h"
    else:
        value = f"{hours} hours"

    if uptime_hours < 72:
        status = "good"
        message = f"Computer has been on for {value}. Looking healthy!"
    elif uptime_hours < 168:  # 7 days
        status = "warning"
        message = f"Running for {value}. Consider restarting to apply updates and free memory."
    else:
        status = "critical"
        message = f"Running for {value}! Please restart your computer — it really needs it."

    return {
        "name": "System Uptime",
        "icon": "⏱️",
        "status": status,
        "value": value,
        "message": message
    }


def check_temperature():
    """Try to read CPU temperature (works best on Linux)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            raise Exception("No sensors found")

        # Look for CPU temp under common sensor names
        for name in ['coretemp', 'cpu_thermal', 'k10temp', 'acpitz']:
            if name in temps:
                temp = temps[name][0].current
                if temp < 70:
                    status = "good"
                    message = f"CPU temperature is normal at {temp}°C."
                elif temp < 90:
                    status = "warning"
                    message = f"CPU is warm at {temp}°C. Check that fans are working."
                else:
                    status = "critical"
                    message = f"CPU is very hot at {temp}°C! Check cooling immediately."
                return {
                    "name": "CPU Temp",
                    "icon": "🌡️",
                    "status": status,
                    "value": f"{temp}°C",
                    "message": message
                }
        raise Exception("CPU sensor not found")
    except Exception:
        return {
            "name": "CPU Temp",
            "icon": "🌡️",
            "status": "good",
            "value": "N/A",
            "message": "Temperature sensors not available on this system."
        }


def get_system_info():
    """Get basic info about the computer."""
    return {
        "os": platform.system() + " " + platform.release(),
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "checked_at": datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    }


def run_all_checks():
    """Run every check and return the full report."""
    checks = [
        check_disk_space(),
        check_cpu(),
        check_memory(),
        check_internet(),
        check_uptime(),
        check_temperature(),
    ]

    # Count how many checks are in each status
    statuses = [c["status"] for c in checks]
    if "critical" in statuses:
        overall = "critical"
        summary = "⚠️ Some issues need your attention!"
    elif "warning" in statuses:
        overall = "warning"
        summary = "🔶 Your PC is mostly healthy, but a few things to watch."
    else:
        overall = "good"
        summary = "✅ Your PC looks great! Everything is running well."

    return {
        "system": get_system_info(),
        "overall": overall,
        "summary": summary,
        "checks": checks
    }


# --- Run from command line (no web server needed) ---
if __name__ == "__main__":
    print("\n🖥️  PC Health Checker — Running checks...\n")
    report = run_all_checks()
    print(f"System: {report['system']['os']}  |  {report['system']['hostname']}")
    print(f"Checked: {report['system']['checked_at']}\n")
    print(f"Overall: {report['summary']}\n")
    print("-" * 50)
    for check in report["checks"]:
        icon = "✅" if check["status"] == "good" else ("⚠️" if check["status"] == "warning" else "🚨")
        print(f"{icon}  {check['name']}: {check['value']}")
        print(f"    {check['message']}\n")
