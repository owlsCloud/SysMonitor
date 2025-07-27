fetch("stats.json")
  .then((res) => res.json())
  .then((data) => {
    const div = document.getElementById("stats");
    div.innerHTML = `
      <p><strong>Time:</strong> ${data.timestamp}</p>
      <p><strong>CPU Usage:</strong> ${data.cpu_percent}%</p>
      <p><strong>Memory:</strong> ${data.memory.used} GB / ${
      data.memory.total
    } GB</p>
      <p><strong>Disk Usage:</strong> ${data.disk.used}% on ${
      data.disk.mount
    }</p>
      <p><strong>Uptime:</strong> ${Math.floor(data.uptime / 3600)} hours</p>
    `;
  })
  .catch((err) => {
    console.error("Failed to load stats:", err);
  });
