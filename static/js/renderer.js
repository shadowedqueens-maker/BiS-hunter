/* renderer.js - DOM builders for BiSHunter UI */

const SLOT_LABELS = {
    head: "Head", neck: "Neck", shoulder: "Shoulder", back: "Back",
    chest: "Chest", wrists: "Wrists", hands: "Hands", waist: "Waist",
    legs: "Legs", feet: "Feet", finger1: "Ring 1", finger2: "Ring 2",
    trinket1: "Trinket 1", trinket2: "Trinket 2",
    main_hand: "Main Hand", off_hand: "Off Hand", ranged_relic: "Relic",
};

const SLOT_ORDER = [
    "head", "neck", "shoulder", "back", "chest", "wrists",
    "hands", "waist", "legs", "feet", "finger1", "finger2",
    "trinket1", "trinket2", "main_hand", "off_hand", "ranged_relic",
];

function wowheadLink(itemId, name, quality) {
    // TBC Classic wowhead link - triggers their tooltip system
    const a = document.createElement("a");
    a.href = `https://tbc.wowhead.com/item=${itemId}`;
    a.dataset.wowhead = `item=${itemId}&domain=tbc`;
    a.textContent = name;
    a.className = `q${quality}`;
    a.target = "_blank";
    a.rel = "noopener";
    return a;
}

function goldDisplay(price) {
    let html = "";
    if (price.gold) html += `<span class="gold">${price.gold}g</span> `;
    if (price.silver) html += `<span class="silver">${price.silver}s</span> `;
    if (price.copper) html += `<span class="copper">${price.copper}c</span>`;
    return html || "0c";
}

// ── Character Banner ────────────────────────────────────────────────

function renderCharBanner(data) {
    const el = document.getElementById("char-banner");
    const char = data.character;
    el.innerHTML = `
        <div class="char-info">
            <h2>${char.name || "Unknown"}</h2>
            <div class="char-meta">
                Level ${char.level || "?"} ${char.class || "?"}
                &mdash; ${char.region || ""}-${char.server || ""} (${char.faction || ""})
            </div>
            <div class="char-specs">
                <span class="spec-badge main">Main: ${data.main_spec.toUpperCase()}</span>
                <span class="spec-badge off">Off: ${data.off_spec.toUpperCase()}</span>
            </div>
        </div>
    `;
}

// ── Paper Doll (Character Sheet) ────────────────────────────────────

function renderPaperDoll(data) {
    const container = document.getElementById("paper-doll");
    container.innerHTML = "";

    // Calculate average ilvl
    let ilvlSum = 0, ilvlCount = 0;
    for (const slot of SLOT_ORDER) {
        const item = data.equipped[slot];
        if (item && item.ilvl) {
            ilvlSum += item.ilvl;
            ilvlCount++;
        }
    }
    const avgIlvl = ilvlCount > 0 ? Math.round(ilvlSum / ilvlCount) : 0;

    // Center panel
    const center = document.createElement("div");
    center.className = "paper-doll-center";
    center.innerHTML = `
        <div class="class-icon">🛡️</div>
        <div class="avg-ilvl">${avgIlvl}</div>
        <div class="avg-ilvl-label">Average Item Level</div>
    `;
    container.appendChild(center);

    // Slot cards
    for (const slot of SLOT_ORDER) {
        const item = data.equipped[slot];
        const card = document.createElement("div");
        card.className = `slot-card slot-${slot}${!item ? " empty" : ""}`;

        if (item && !item.missing) {
            const nameLink = wowheadLink(item.item_id, item.name, item.quality);

            card.innerHTML = `
                <span class="slot-label">${SLOT_LABELS[slot]}</span>
                <span class="slot-item-name"></span>
                <span class="slot-ilvl">${item.ilvl}</span>
                <span class="slot-scores">
                    <span class="score-badge main">${data.main_spec[0].toUpperCase()}: ${Math.round(item.score_main)}</span>
                    <span class="score-badge off">${data.off_spec[0].toUpperCase()}: ${Math.round(item.score_off)}</span>
                </span>
            `;
            card.querySelector(".slot-item-name").appendChild(nameLink);
        } else {
            card.innerHTML = `
                <span class="slot-label">${SLOT_LABELS[slot]}</span>
                <span class="slot-item-name q0">(empty)</span>
            `;
        }

        container.appendChild(card);
    }

    // Refresh wowhead tooltips after DOM update
    refreshWowheadTooltips();
}

// ── Inventory Tab ───────────────────────────────────────────────────

function renderInventory(data) {
    const container = document.getElementById("inventory-content");
    container.innerHTML = "";

    const sections = [
        {
            key: "keep_main", label: `Keep for ${data.main_spec.toUpperCase()} (Main)`,
            cssClass: "keep-main", items: data.inventory.keep_main,
        },
        {
            key: "keep_off", label: `Keep for ${data.off_spec.toUpperCase()} (Off)`,
            cssClass: "keep-off", items: data.inventory.keep_off,
        },
        {
            key: "vendor", label: "Vendor / Disenchant",
            cssClass: "vendor", items: data.inventory.vendor,
        },
    ];

    for (const sec of sections) {
        if (!sec.items || sec.items.length === 0) continue;

        const section = document.createElement("div");
        section.className = `inv-section ${sec.cssClass}`;

        section.innerHTML = `
            <div class="inv-section-header">
                <h3>${sec.label}</h3>
                <span class="count">${sec.items.length}</span>
            </div>
        `;

        const grid = document.createElement("div");
        grid.className = "inv-grid";

        for (const item of sec.items) {
            const card = document.createElement("div");
            card.className = "inv-item";

            const nameLink = wowheadLink(item.item_id, item.name, item.quality);

            if (sec.key === "vendor") {
                const actionClass = item.action === "DE" ? "action-de" : "action-vendor";
                card.innerHTML = `
                    <div class="item-info">
                        <div class="item-name"></div>
                        <div class="item-reason">iLvl ${item.ilvl} &mdash; ${goldDisplay(item.sell_price)}</div>
                    </div>
                    <span class="item-action ${actionClass}">${item.action}</span>
                `;
            } else {
                card.innerHTML = `
                    <div class="item-info">
                        <div class="item-name"></div>
                        <div class="item-reason">${item.reason || ""}</div>
                    </div>
                    <span class="slot-scores">
                        <span class="score-badge main">${Math.round(item.score_main)}</span>
                        <span class="score-badge off">${Math.round(item.score_off)}</span>
                    </span>
                `;
            }

            card.querySelector(".item-name").appendChild(nameLink);
            grid.appendChild(card);
        }

        section.appendChild(grid);

        // Vendor total
        if (sec.key === "vendor") {
            let totalCopper = 0;
            for (const item of sec.items) {
                totalCopper += item.sell_price.gold * 10000 + item.sell_price.silver * 100 + item.sell_price.copper;
            }
            const totalPrice = {
                gold: Math.floor(totalCopper / 10000),
                silver: Math.floor((totalCopper % 10000) / 100),
                copper: totalCopper % 100,
            };
            const totalDiv = document.createElement("div");
            totalDiv.className = "vendor-total gold-display";
            totalDiv.innerHTML = `Total vendor value: ${goldDisplay(totalPrice)}`;
            section.appendChild(totalDiv);
        }

        container.appendChild(section);
    }

    if (container.children.length === 0) {
        container.innerHTML = '<div class="upgrade-empty">No inventory items to categorize.</div>';
    }

    refreshWowheadTooltips();
}

// ── Upgrades Tab ────────────────────────────────────────────────────

let currentUpgradeSpec = null;
let currentUpgradePhase = null;
let analysisData = null;

function renderUpgradeControls(data) {
    analysisData = data;
    currentUpgradeSpec = data.main_spec;
    currentUpgradePhase = "pre_raid";

    // Spec toggle
    const specToggle = document.getElementById("upgrade-spec-toggle");
    specToggle.innerHTML = "";
    for (const spec of [data.main_spec, data.off_spec]) {
        const btn = document.createElement("button");
        btn.className = `spec-toggle-btn${spec === currentUpgradeSpec ? " active" : ""}`;
        btn.textContent = spec.toUpperCase();
        btn.addEventListener("click", () => {
            currentUpgradeSpec = spec;
            specToggle.querySelectorAll(".spec-toggle-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderUpgradeTable();
        });
        specToggle.appendChild(btn);
    }

    // Phase tabs
    const phaseTabs = document.getElementById("phase-tabs");
    phaseTabs.innerHTML = "";
    for (const [key, name] of Object.entries(data.phases)) {
        const tab = document.createElement("button");
        tab.className = `phase-tab${key === currentUpgradePhase ? " active" : ""}`;
        tab.textContent = name;
        tab.addEventListener("click", () => {
            currentUpgradePhase = key;
            phaseTabs.querySelectorAll(".phase-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            renderUpgradeTable();
        });
        phaseTabs.appendChild(tab);
    }

    renderUpgradeTable();
}

function renderUpgradeTable() {
    const container = document.getElementById("upgrades-content");
    const upgrades = analysisData.upgrades[currentUpgradeSpec]?.[currentUpgradePhase] || [];

    if (upgrades.length === 0) {
        container.innerHTML = '<div class="upgrade-empty">No upgrades found for this phase.</div>';
        return;
    }

    // Filter to only show actual upgrades (positive delta) first, then others
    const sorted = [...upgrades].sort((a, b) => b.score_delta - a.score_delta);

    let html = `
        <table class="upgrade-table">
            <thead>
                <tr>
                    <th>Slot</th>
                    <th>Current</th>
                    <th></th>
                    <th>Upgrade</th>
                    <th>Delta</th>
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const u of sorted) {
        const bis = u.bis;
        const deltaClass = u.score_delta > 0 ? "delta-positive" : u.score_delta < 0 ? "delta-negative" : "delta-neutral";
        const deltaStr = u.score_delta > 0 ? `+${u.score_delta.toFixed(0)}` : u.score_delta.toFixed(0);

        html += `
            <tr>
                <td class="upgrade-slot">${SLOT_LABELS[u.slot] || u.slot}</td>
                <td class="upgrade-current">${u.current_name}</td>
                <td class="upgrade-arrow">→</td>
                <td>
                    <a href="https://tbc.wowhead.com/item=${bis.item_id}"
                       data-wowhead="item=${bis.item_id}&domain=tbc"
                       class="q${bis.quality}" target="_blank" rel="noopener">
                        ${bis.name}
                    </a>
                    <span class="slot-ilvl">(${bis.ilvl})</span>
                </td>
                <td class="upgrade-delta ${deltaClass}">${deltaStr}</td>
                <td class="upgrade-source">${u.source}</td>
            </tr>
        `;
    }

    html += "</tbody></table>";
    container.innerHTML = html;
    refreshWowheadTooltips();
}

// ── Wowhead Tooltip Refresh ─────────────────────────────────────────

function refreshWowheadTooltips() {
    // Wowhead's power.js exposes $WowheadPower for re-scanning
    if (typeof $WowheadPower !== "undefined" && $WowheadPower.refreshLinks) {
        setTimeout(() => $WowheadPower.refreshLinks(), 100);
    }
}

// Export for app.js
window.BiSRenderer = {
    renderCharBanner,
    renderPaperDoll,
    renderInventory,
    renderUpgradeControls,
};
