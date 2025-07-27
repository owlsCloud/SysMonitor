#!/usr/bin/env python3
import psutil
import platform
import json
import os
import logging
from datetime import datetime, timezone

# Base directory & log config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "monitor.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def bytes_to_gb(b):
    return round(b / (1024**3), 2)

def get_top_processes(limit=5):
    procs = []
    for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return procs[:limit]

try:
    # Gather stats
    now = datetime.now(timezone.utc)
    stats = {
        "timestamp": now.strftime("%B %d, %Y %H:%M:%S UTC"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_per_core": psutil.cpu_percent(percpu=True),
        "cpu_freq": psutil.cpu_freq()._asdict(),
        "cpu_count": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "memory": {
            "used": bytes_to_gb(psutil.virtual_memory().used),
            "total": bytes_to_gb(psutil.virtual_memory().total)
        },
        "disk": {
            "used": bytes_to_gb(psutil.disk_usage('/').used),
            "total": bytes_to_gb(psutil.disk_usage('/').total),
            "mount": '/'
        },
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_recv": psutil.net_io_counters().bytes_recv
        },
        "uptime_seconds": round((now - datetime.fromtimestamp(psutil.boot_time(), timezone.utc)).total_seconds()),
        "boot_time": datetime.fromtimestamp(psutil.boot_time(), timezone.utc)
                              .strftime("%B %d, %Y %H:%M:%S UTC"),
        "host": {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "hostname": platform.node()
        },
        "top_processes": get_top_processes()
    }

    # Paths
    stats_path   = os.path.join(BASE_DIR, "public", "stats.json")
    history_path = os.path.join(BASE_DIR, "public", "history.json")

    # Write stats.json
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    # Update rolling history (keep last 12)
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = json.load(f)
    else:
        history = []

    history.append({"timestamp": stats["timestamp"], "cpu_percent": stats["cpu_percent"]})
    history = history[-12:]
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    logging.info(f"Wrote stats and history ({len(history)} entries)")

except Exception:
    logging.exception("Failed to collect or write stats")
