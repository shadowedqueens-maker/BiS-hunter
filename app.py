#!/usr/bin/env python3
"""BiSHunter Web Application - TBC Classic Gear Advisor"""

from flask import Flask, render_template, jsonify, request
import config
from db_loader import load_db, get_item, get_item_source
from amr_parser import parse_amr_export
from scoring import score_item, get_item_stats, STAT_WEIGHTS
from recommender import categorize_inventory, find_upgrades
from bis_lists import find_item_in_bis, BIS
from constants import (
    QUALITY_NAMES, GEAR_SLOTS, PHASES, STAT_TYPES, INVENTORY_TYPES, AMR_SLOTS,
)

app = Flask(__name__)

# Load DB once at startup
print("Starting BiSHunter Web - Loading item database...")
db = load_db(config.DB_PATH)
print("Database loaded. Starting web server...\n")


def row_to_dict(row):
    """Convert sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def format_copper(copper):
    """Convert copper to {gold, silver, copper} dict."""
    if not copper or copper <= 0:
        return {"gold": 0, "silver": 0, "copper": 0}
    return {
        "gold": copper // 10000,
        "silver": (copper % 10000) // 100,
        "copper": copper % 100,
    }


def enrich_item(item_id, spec_main="prot", spec_off="ret"):
    """Build a rich item dict for the frontend."""
    item = get_item(db, item_id)
    if not item:
        return {"item_id": item_id, "name": "Unknown Item", "missing": True}

    stats = get_item_stats(item)
    sources = get_item_source(db, item_id)
    bis = find_item_in_bis(item_id)

    source_list = []
    for src in sources:
        source_list.append({
            "boss": src["source_name"],
            "instance": src["instance_name"] or "",
            "short_name": src["short_name"] or "",
        })

    return {
        "item_id": item_id,
        "name": item["name"],
        "ilvl": item["ItemLevel"],
        "quality": item["Quality"],
        "quality_name": QUALITY_NAMES.get(item["Quality"], "Unknown"),
        "inventory_type": item["InventoryType"],
        "slot_name": INVENTORY_TYPES.get(item["InventoryType"], "unknown"),
        "armor": item["armor"] or 0,
        "stats": stats,
        "score_main": score_item(item, spec_main),
        "score_off": score_item(item, spec_off),
        "sell_price": format_copper(item["SellPrice"]),
        "sources": source_list,
        "bis_appearances": [
            {"spec": s, "phase": p, "slot": sl, "rank": r}
            for s, p, sl, r in bis
        ],
    }


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/specs")
def api_specs():
    """Return available specs, classes, phases."""
    return jsonify({
        "classes": ["PALADIN"],
        "specs": {
            "PALADIN": ["prot", "ret", "holy"],
        },
        "phases": {k: v["name"] for k, v in PHASES.items()},
        "stat_weights": STAT_WEIGHTS,
    })


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """Main analysis endpoint. Parses AMR export and returns full gear report."""
    data = request.get_json()
    if not data or "amr_export" not in data:
        return jsonify({"error": "Missing amr_export field"}), 400

    amr_string = data["amr_export"]
    main_spec = data.get("main_spec", "prot")
    off_spec = data.get("off_spec", "ret")

    # Parse AMR export
    try:
        parsed = parse_amr_export(amr_string)
    except Exception as e:
        return jsonify({"error": f"Failed to parse AMR export: {str(e)}"}), 400

    char = parsed["character"]
    equipped = parsed["equipped"]
    inventory = parsed["inventory"]

    # Enrich equipped items
    equipped_enriched = {}
    for slot in GEAR_SLOTS:
        item_id = equipped.get(slot)
        if item_id:
            equipped_enriched[slot] = enrich_item(item_id, main_spec, off_spec)
        else:
            equipped_enriched[slot] = None

    # Categorize inventory
    cats = categorize_inventory(db, equipped, inventory, main_spec, off_spec)

    inventory_result = {
        "keep_main": [],
        "keep_off": [],
        "vendor": [],
    }

    for item_id, item_row, reason in cats["keep_main"]:
        enriched = enrich_item(item_id, main_spec, off_spec)
        enriched["reason"] = reason
        inventory_result["keep_main"].append(enriched)

    for item_id, item_row, reason in cats["keep_off"]:
        enriched = enrich_item(item_id, main_spec, off_spec)
        enriched["reason"] = reason
        inventory_result["keep_off"].append(enriched)

    for item_id, item_row, sell_price in cats["vendor"]:
        enriched = enrich_item(item_id, main_spec, off_spec)
        enriched["action"] = "DE" if item_row["Quality"] >= 2 else "Vendor"
        inventory_result["vendor"].append(enriched)

    # Find upgrades per phase per spec
    upgrades = {}
    for spec in [main_spec, off_spec]:
        upgrades[spec] = {}
        for phase_key in PHASES:
            phase_upgrades = find_upgrades(db, equipped, spec, phase_key)
            upgrades[spec][phase_key] = []
            for u in phase_upgrades:
                bis_enriched = enrich_item(u["bis_id"], main_spec, off_spec)
                upgrades[spec][phase_key].append({
                    "slot": u["slot"],
                    "current_id": u["current_id"],
                    "current_name": u["current_name"],
                    "current_score": u["current_score"],
                    "bis": bis_enriched,
                    "bis_score": u["bis_score"],
                    "score_delta": u["score_delta"],
                    "source": u["source"],
                    "rank": u["rank"],
                })

    return jsonify({
        "character": char,
        "main_spec": main_spec,
        "off_spec": off_spec,
        "equipped": equipped_enriched,
        "inventory": inventory_result,
        "upgrades": upgrades,
        "phases": {k: v["name"] for k, v in PHASES.items()},
    })


@app.route("/api/item/<int:item_id>")
def api_item(item_id):
    """Return detailed item data for tooltip enrichment."""
    main_spec = request.args.get("main", "prot")
    off_spec = request.args.get("off", "ret")
    enriched = enrich_item(item_id, main_spec, off_spec)
    if enriched.get("missing"):
        return jsonify({"error": "Item not found"}), 404
    return jsonify(enriched)


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=False)
