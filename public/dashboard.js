let historyChart;
const statsDiv = document.getElementById("stats");
const ctx = document.getElementById("historyChart").getContext("2d");

async function fetchAndRender() {
  try {
    const statsRes = await fetch("stats.json");
    const data = await statsRes.json();

    // render stats
    statsDiv.innerHTML = `
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
        <ul style="list-style:none; margin:0; padding:0">
          <li><strong>hostname:</strong> ${data.host.hostname}</li>
          <li><strong>os:</strong> ${data.host.os}</li>
          <li><strong>os version:</strong> ${data.host.os_version}</li>
        </ul>
      </p>
      <p style="margin-bottom:0"><strong>top 5 processes:</strong></p>
      <ul style="list-style:none; margin:0; padding:0">
        ${data.top_processes
          .slice(0, 5)
          .map(
            (p) =>
              `<li>${p.name} (${p.cpu_percent.toFixed(
                1
              )}% cpu, ${p.memory_percent.toFixed(1)}% mem)</li>`
          )
          .join("")}
      </ul>
    `;

    // fetch history
    const histRes = await fetch("history.json");
    const history = await histRes.json();
    const labels = history.map((e) => e.timestamp);
    const cpuData = history.map((e) => e.cpu_percent);

    // draw or update chart
    if (!historyChart) {
      historyChart = new Chart(ctx, {
        type: "line",
        data: {
          labels,
          datasets: [
            { label: "cpu %", data: cpuData, fill: false, tension: 0.3 },
          ],
        },
        options: {
          scales: {
            x: { title: { display: true, text: "timestamp" } },
            y: {
              beginAtZero: true,
              max: 100,
              title: { display: true, text: "cpu %" },
            },
          },
        },
      });
    } else {
      historyChart.data.labels = labels;
      historyChart.data.datasets[0].data = cpuData;
      historyChart.update();
    }
  } catch (err) {
    console.error("dashboard error:", err);
    statsDiv.textContent = "failed to load data.";
  }
}

// initial load
fetchAndRender();

// auto-refresh every 60 seconds
setInterval(fetchAndRender, 60_000);

// wire the manual refresh button
refreshBtn.addEventListener("click", () => {
  console.log("refresh-btn clicked");
  refreshBtn.disabled = true;
  fetchAndRender().finally(() => {
    refreshBtn.disabled = false;
  });
});
