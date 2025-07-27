import psutil
import platform
import json
import os
from datetime import datetime, timezone
# Format bytes to MB or GB as needed
def bytes_to_gb(b):
    return round(b / (1024 ** 3), 2)

def get_top_processes(limit=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Sort by CPU usage descending
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]

stats = {
    
    "timestamp": datetime.now(timezone.utc).strftime("%B %d, %Y %H:%M:%S"),

    # CPU
    "cpu_percent": psutil.cpu_percent(interval=1),
    "cpu_per_core": psutil.cpu_percent(percpu=True),
    "cpu_freq": psutil.cpu_freq()._asdict(),
    "cpu_count": psutil.cpu_count(logical=False),
    "cpu_threads": psutil.cpu_count(logical=True),

    # Memory
    "memory": {
        "used": bytes_to_gb(psutil.virtual_memory().used),
        "total": bytes_to_gb(psutil.virtual_memory().total)
    },

    # Disk
    "disk": {
        "used": bytes_to_gb(psutil.disk_usage('/').used),
        "total": bytes_to_gb(psutil.disk_usage('/').total),
        "mount": '/'
    },

    # Network
    "network": {
        "bytes_sent": psutil.net_io_counters().bytes_sent,
        "bytes_recv": psutil.net_io_counters().bytes_recv
    },

    # Uptime
    "uptime_seconds": round((datetime.now(timezone.utc)
                             - datetime.fromtimestamp(psutil.boot_time(), timezone.utc)
                            ).total_seconds()),
    "boot_time": datetime.fromtimestamp(psutil.boot_time(), timezone.utc).isoformat(),

    # Host Info
    "host": {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "hostname": platform.node()
    },

    # Top processes
    "top_processes": get_top_processes()
}

# Save to JSON
output_path = os.path.join("public", "stats.json")
with open(output_path, "w") as f:
    json.dump(stats, f, indent=2)
