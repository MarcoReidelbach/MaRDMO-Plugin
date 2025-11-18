document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("progress-root");
  if (!root) return;

  const jobId = root.dataset.jobId;
  const progressStatusUrl = root.dataset.progressUrl;
  const coloredContainer = document.getElementById("coloredContainer");
  const status = document.getElementById("status");

  if (!progressStatusUrl || !coloredContainer || !status) {
    console.error("Progress page is missing required elements or data attributes.");
    return;
  }

  function getDotHTML() {
    return `
      <span class="dots" style="display:inline-flex;width:1.5em;justify-content:left;">
        <span class="blink" style="animation: blink 1.8s infinite ease-in-out; animation-delay:0s;">.</span>
        <span class="blink" style="animation: blink 1.8s infinite ease-in-out; animation-delay:0.3s;">.</span>
        <span class="blink" style="animation: blink 1.8s infinite ease-in-out; animation-delay:0.6s;">.</span>
      </span>
      <style>
        @keyframes blink {
          0%, 80% { opacity: 0.2; }
          40% { opacity: 1; }
        }
      </style>
    `;
  }

  async function updateProgress() {
    try {
      const res = await fetch(progressStatusUrl, { cache: "no-store" });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();

      // Error state
      if (data.phase === "error" || data.progress === -1) {
        status.innerHTML = `
          <div style="white-space:nowrap;">❌ Upload failed</div>
          <div style="font-size:22px;color:darkred;max-width:600px;margin:0.5rem auto 0;">
            ${data.error || "Unknown error"}
          </div>
        `;
        return;
      }

      // Update logo fill
      if (typeof data.progress === "number") {
        coloredContainer.style.width = `${data.progress}%`;
      }

      // Phase: items
      if (data.phase === "items") {
        status.innerHTML = `
          <div style="white-space:nowrap;">Create new Items${getDotHTML()}</div>
        `;
        setTimeout(updateProgress, 500);
        return;
      }

      // Phase: relations
      if (data.phase === "relations") {
        status.innerHTML = `
          <div style="white-space:nowrap;">Create new Items ✅</div>
          <div style="white-space:nowrap;">Create new Statements${getDotHTML()}</div>
        `;
        setTimeout(updateProgress, 500);
        return;
      }

      // Phase: done
      if (data.phase === "done" && data.done) {
        const hasRedirect = !!data.redirect;
        const finalLine = hasRedirect
          ? `✅ Upload complete! Redirecting${getDotHTML()}`
          : "✅ Upload complete!";

        status.innerHTML = `
          <div style="white-space:nowrap;">Create new Items ✅</div>
          <div style="white-space:nowrap;">Create new Statements ✅</div>
          <div style="white-space:nowrap;">${finalLine}</div>
        `;
        coloredContainer.style.width = "100%";

        if (hasRedirect) {
          setTimeout(() => {
            window.location.href = data.redirect;
          }, 1500);
        }
        return;
      }

      // Fallback: keep polling
      if (!data.done) {
        setTimeout(updateProgress, 1000);
      }
    } catch (err) {
      console.error("Error updating progress:", err);
      status.innerHTML = `
        <div style="white-space:nowrap;">❌ Upload failed</div>
        <div style="font-size:22px;color:darkred;max-width:600px;margin:0.5rem auto 0;">
          Fehler beim Abrufen des Fortschritts.
        </div>
      `;
    }
  }

  updateProgress();
});

