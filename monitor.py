#!/usr/bin/env python3
import json
import os
import time
import psutil
from datetime import datetime

stats = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "cpu_percent": psutil.cpu_percent(interval=1),
    "memory": {
        "used": round(psutil.virtual_memory().used / (1024**3), 2),
        "total": round(psutil.virtual_memory().total / (1024**3), 2)
    },
    "disk": {
        "used": psutil.disk_usage('/').percent,
        "mount": '/'
    },
    "uptime": round(time.time() - psutil.boot_time(), 2)
}

output_path = os.path.join("public", "stats.json")
os.makedirs("public", exist_ok=True)
with open(output_path, "w") as f:
    json.dump(stats, f, indent=2)

print(f"✅ Stats written to {output_path}")
