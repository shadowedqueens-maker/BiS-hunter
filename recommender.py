# recommender.py - Gear categorization and upgrade recommendation engine

from constants import (
    GEAR_SLOTS, INVENTORY_TYPE_TO_SLOTS, QUALITY_NAMES,
    PALADIN_CLASS_MASK, PHASES, ITEM_CLASS_ARMOR, ITEM_CLASS_WEAPON,
)
from bis_lists import get_all_bis_ids, get_bis_for_slot, find_item_in_bis, BIS
from scoring import score_item, get_item_stats, format_item_score
from db_loader import get_item, get_item_source


def _is_equippable_by_paladin(item_row):
    """Check if a paladin can equip this item."""
    ac = item_row["AllowableClass"]
    if ac == -1:
        return True
    return (ac & PALADIN_CLASS_MASK) != 0


def _get_item_slots(item_row):
    """Determine which gear slots an item can fill."""
    inv_type = item_row["InventoryType"]
    return INVENTORY_TYPE_TO_SLOTS.get(inv_type, [])


def _format_source(conn, item_id):
    """Get a human-readable source string for an item."""
    sources = get_item_source(conn, item_id)
    if sources:
        parts = []
        for src in sources:
            if src["instance_name"]:
                parts.append(f"{src['source_name']} ({src['short_name']})")
            else:
                parts.append(src["source_name"])
        return ", ".join(parts)
    return "Unknown source"


def _format_copper(copper):
    """Format copper amount as gold/silver/copper."""
    if not copper or copper <= 0:
        return "0c"
    gold = copper // 10000
    silver = (copper % 10000) // 100
    cop = copper % 100
    parts = []
    if gold:
        parts.append(f"{gold}g")
    if silver:
        parts.append(f"{silver}s")
    if cop:
        parts.append(f"{cop}c")
    return " ".join(parts)


def categorize_inventory(conn, equipped, inventory, main_spec, off_spec):
    """Categorize all character items into keep/vendor/disenchant.

    Args:
        conn: SQLite database connection
        equipped: dict of {slot_name: item_id} from AMR parser
        inventory: list of item_ids from bags/bank
        main_spec: "prot" or "ret"
        off_spec: "prot" or "ret"

    Returns:
        dict with keys:
            keep_main: [(item_id, item_row, reason), ...]
            keep_off: [(item_id, item_row, reason), ...]
            keep_equipped: [(slot, item_id, item_row), ...]
            vendor: [(item_id, item_row, sell_price), ...]
            unknown: [(item_id, reason), ...]
    """
    main_bis = get_all_bis_ids(main_spec)
    off_bis = get_all_bis_ids(off_spec)

    result = {
        "keep_main": [],
        "keep_off": [],
        "keep_equipped": [],
        "vendor": [],
        "unknown": [],
    }

    # Equipped items are always "keep"
    for slot, item_id in equipped.items():
        item = get_item(conn, item_id)
        if item:
            result["keep_equipped"].append((slot, item_id, item))
        else:
            result["unknown"].append((item_id, "Not in DB (equipped)"))

    # Categorize inventory items
    for item_id in inventory:
        item = get_item(conn, item_id)
        if not item:
            result["unknown"].append((item_id, "Not in DB"))
            continue

        quality = item["Quality"]
        item_class = item["class"]

        # Skip non-equipment items (consumables, trade goods, quest items, etc.)
        if item_class not in (ITEM_CLASS_ARMOR, ITEM_CLASS_WEAPON):
            continue

        # Skip items a paladin can't equip
        if not _is_equippable_by_paladin(item):
            result["vendor"].append((item_id, item, item["SellPrice"] or 0))
            continue

        # Check if it's on any BiS list
        bis_matches = find_item_in_bis(item_id)
        if bis_matches:
            for spec, phase, slot, rank in bis_matches:
                if spec == main_spec:
                    phase_name = PHASES.get(phase, {}).get("name", phase)
                    result["keep_main"].append((
                        item_id, item,
                        f"BiS #{rank} for {main_spec} {slot} in {phase_name}"
                    ))
                    break
                elif spec == off_spec:
                    phase_name = PHASES.get(phase, {}).get("name", phase)
                    result["keep_off"].append((
                        item_id, item,
                        f"BiS #{rank} for {off_spec} {slot} in {phase_name}"
                    ))
                    break
            else:
                # In some BiS list but not main or off spec (shouldn't happen with 2 specs)
                pass
            continue

        # Not on any BiS list - score it for both specs
        slots = _get_item_slots(item)
        if not slots:
            result["vendor"].append((item_id, item, item["SellPrice"] or 0))
            continue

        main_score = score_item(item, main_spec)
        off_score = score_item(item, off_spec)

        # Compare against currently equipped items in those slots
        dominated = True  # Is this item worse than equipped in ALL applicable slots?
        for slot in slots:
            equipped_id = equipped.get(slot)
            if equipped_id:
                eq_item = get_item(conn, equipped_id)
                if eq_item:
                    eq_main = score_item(eq_item, main_spec)
                    eq_off = score_item(eq_item, off_spec)
                    # Keep if it's better than equipped for either spec
                    if main_score > eq_main or off_score > eq_off:
                        dominated = False
                        break
                else:
                    dominated = False
                    break
            else:
                # Empty slot - definitely keep it
                dominated = False
                break

        if dominated:
            # Worse than equipped for both specs in all possible slots
            result["vendor"].append((item_id, item, item["SellPrice"] or 0))
        else:
            # Better than equipped for at least one spec/slot
            if main_score >= off_score:
                result["keep_main"].append((
                    item_id, item,
                    f"Scored {main_score:.0f} for {main_spec} (upgrade for {', '.join(slots)})"
                ))
            else:
                result["keep_off"].append((
                    item_id, item,
                    f"Scored {off_score:.0f} for {off_spec} (upgrade for {', '.join(slots)})"
                ))

    return result


def find_upgrades(conn, equipped, spec, phase):
    """Find BiS upgrades the character still needs for a given spec and phase.

    Returns list of dicts:
        {slot, current_id, current_name, current_score,
         bis_id, bis_name, bis_score, score_delta, source, rank}
    """
    upgrades = []
    bis_data = BIS.get(spec, {}).get(phase, {})

    for slot in GEAR_SLOTS:
        bis_items = bis_data.get(slot, [])
        if not bis_items:
            continue

        current_id = equipped.get(slot)
        current_item = get_item(conn, current_id) if current_id else None
        current_score = score_item(current_item, spec) if current_item else 0.0
        current_name = current_item["name"] if current_item else "(empty)"

        for rank, bis_id in enumerate(bis_items, 1):
            if bis_id == current_id:
                # Already have this BiS item equipped
                break

            bis_item = get_item(conn, bis_id)
            if not bis_item:
                continue

            bis_score = score_item(bis_item, spec)
            delta = bis_score - current_score
            source = _format_source(conn, bis_id)

            upgrades.append({
                "slot": slot,
                "current_id": current_id,
                "current_name": current_name,
                "current_score": current_score,
                "bis_id": bis_id,
                "bis_name": bis_item["name"],
                "bis_ilvl": bis_item["ItemLevel"],
                "bis_quality": bis_item["Quality"],
                "bis_score": bis_score,
                "score_delta": round(delta, 1),
                "source": source,
                "rank": rank,
            })
            break  # Only show the highest-priority BiS item they don't have

    # Sort by score delta (biggest upgrades first)
    upgrades.sort(key=lambda x: -x["score_delta"])
    return upgrades


def format_report(conn, equipped, inventory, main_spec, off_spec):
    """Generate the full recommendation report as a string."""
    lines = []

    # Categorize inventory
    cats = categorize_inventory(conn, equipped, inventory, main_spec, off_spec)

    # === Currently Equipped ===
    lines.append("=" * 70)
    lines.append("  CURRENTLY EQUIPPED")
    lines.append("=" * 70)
    for slot, item_id, item in cats["keep_equipped"]:
        prot_score = score_item(item, "prot")
        ret_score = score_item(item, "ret")
        q = QUALITY_NAMES.get(item["Quality"], "?")
        lines.append(f"  {slot:15s} [{q}] {item['name']} (iLvl {item['ItemLevel']}) "
                     f"  Prot: {prot_score:.0f}  Ret: {ret_score:.0f}")

    # === Keep for Main Spec ===
    if cats["keep_main"]:
        lines.append("")
        lines.append("=" * 70)
        lines.append(f"  KEEP FOR {main_spec.upper()} (Main Spec)")
        lines.append("=" * 70)
        for item_id, item, reason in cats["keep_main"]:
            q = QUALITY_NAMES.get(item["Quality"], "?")
            lines.append(f"  [{q}] {item['name']} (iLvl {item['ItemLevel']}) - {reason}")

    # === Keep for Off Spec ===
    if cats["keep_off"]:
        lines.append("")
        lines.append("=" * 70)
        lines.append(f"  KEEP FOR {off_spec.upper()} (Off Spec)")
        lines.append("=" * 70)
        for item_id, item, reason in cats["keep_off"]:
            q = QUALITY_NAMES.get(item["Quality"], "?")
            lines.append(f"  [{q}] {item['name']} (iLvl {item['ItemLevel']}) - {reason}")

    # === Vendor / Disenchant ===
    if cats["vendor"]:
        lines.append("")
        lines.append("=" * 70)
        lines.append("  VENDOR / DISENCHANT (not useful for either spec)")
        lines.append("=" * 70)
        total_vendor = 0
        for item_id, item, sell_price in sorted(cats["vendor"], key=lambda x: -x[2]):
            q = QUALITY_NAMES.get(item["Quality"], "?")
            price_str = _format_copper(sell_price)
            action = "DE" if item["Quality"] >= 2 else "Vendor"
            lines.append(f"  [{q}] {item['name']} (iLvl {item['ItemLevel']}) "
                         f"- {action} ({price_str})")
            total_vendor += sell_price
        lines.append(f"  --- Total vendor value: {_format_copper(total_vendor)} ---")

    # === Upgrades to Farm ===
    for spec, label in [(main_spec, "MAIN SPEC"), (off_spec, "OFF SPEC")]:
        for phase_key in ["pre_raid", "t4", "t5", "t6", "sunwell"]:
            phase_name = PHASES.get(phase_key, {}).get("name", phase_key)
            upgrades = find_upgrades(conn, equipped, spec, phase_key)

            if upgrades:
                lines.append("")
                lines.append("=" * 70)
                lines.append(f"  UPGRADES TO FARM: {spec.upper()} ({label}) - {phase_name}")
                lines.append("=" * 70)
                for u in upgrades:
                    q = QUALITY_NAMES.get(u["bis_quality"], "?")
                    delta_str = f"+{u['score_delta']}" if u['score_delta'] > 0 else str(u['score_delta'])
                    lines.append(
                        f"  {u['slot']:15s} [{q}] {u['bis_name']} (iLvl {u['bis_ilvl']}) "
                        f"  Score: {u['bis_score']:.0f} ({delta_str} vs {u['current_name']})"
                    )
                    lines.append(f"  {'':15s} Source: {u['source']}")

    return "\n".join(lines)
