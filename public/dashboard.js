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
      <p><strong>Uptime:</strong> ${Math.floor(
        data.uptime_seconds / 3600
      )} hours</p>
      <p style="margin-bottom:0"><strong>Host Info:</strong>
      <ul style="list-style:none; margin:0">
      <li><strong>Hostname:</strong> ${data.host.hostname}</li>
      <li><strong>OS:</strong> ${data.host.os}</li>
      <li><strong>OS Version:</strong> ${data.host.os_version}</li>
      </ul></p>
      <Strong>Top 5 Processes: </Strong><ul style="list-style:none; margin:0">
      <li> ${data.top_processes[0].name}
      </li>
      <li> ${data.top_processes[1].name}
      </li>
      <li> ${data.top_processes[2].name}
      </li>
      <li> ${data.top_processes[3].name}
      </li>
      <li> ${data.top_processes[4].name}
      </li></ul>


      
    `;
  })
  .catch((err) => {
    console.error("Failed to load stats:", err);
  });
