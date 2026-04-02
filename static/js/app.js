/* app.js - BiSHunter main controller */

(function () {
    const amrInput = document.getElementById("amr-input");
    const mainSpecSelect = document.getElementById("main-spec");
    const offSpecSelect = document.getElementById("off-spec");
    const analyzeBtn = document.getElementById("analyze-btn");
    const loadingOverlay = document.getElementById("loading-overlay");
    const resultsSection = document.getElementById("results-section");

    // ── Tab Switching ───────────────────────────────────────────────

    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const tabId = btn.dataset.tab;

            // Update button active state
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // Show/hide tab panes
            document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.add("hidden"));
            const target = document.getElementById(`tab-${tabId}`);
            if (target) {
                target.classList.remove("hidden");
            }
        });
    });

    // ── Analyze Button ──────────────────────────────────────────────

    analyzeBtn.addEventListener("click", async () => {
        const amrExport = amrInput.value.trim();
        if (!amrExport) {
            alert("Please paste your AskMrRobot export string.");
            return;
        }

        const mainSpec = mainSpecSelect.value;
        const offSpec = offSpecSelect.value;

        if (mainSpec === offSpec) {
            alert("Main spec and off spec must be different.");
            return;
        }

        // Show loading
        loadingOverlay.classList.remove("hidden");
        resultsSection.classList.add("hidden");

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    amr_export: amrExport,
                    main_spec: mainSpec,
                    off_spec: offSpec,
                }),
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || "Server error");
            }

            const data = await response.json();

            // Render all sections
            BiSRenderer.renderCharBanner(data);
            BiSRenderer.renderPaperDoll(data);
            BiSRenderer.renderInventory(data);
            BiSRenderer.renderUpgradeControls(data);

            // Show results
            resultsSection.classList.remove("hidden");

            // Reset to Character tab
            document.querySelector('.tab-btn[data-tab="character"]').click();

        } catch (err) {
            alert("Error: " + err.message);
            console.error(err);
        } finally {
            loadingOverlay.classList.add("hidden");
        }
    });

    // ── Pre-fill with default export if available ───────────────────

    // Allow pre-filling via URL hash
    if (window.location.hash) {
        try {
            const params = JSON.parse(decodeURIComponent(window.location.hash.slice(1)));
            if (params.amr) amrInput.value = params.amr;
            if (params.main) mainSpecSelect.value = params.main;
            if (params.off) offSpecSelect.value = params.off;
        } catch (e) {
            // Ignore invalid hash
        }
    }
})();
