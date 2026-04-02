# amr_parser.py - Parse AskMrRobot export strings for TBC Classic

import re
from constants import AMR_SLOTS


def parse_amr_export(export_str):
    """Parse an AskMrRobot export string into structured character data.

    AMR export format (TBC):
        $version;region;server;name;guild;faction;race;level;extra;spec_count;
        .s1;CLASS;talents;
        .q1;itemDelta_s_slot;...;
        .inv;delta;delta;...;$

    Item IDs are delta-encoded (cumulative) within each section.
    Items may have suffixes like 'f' (random suffix), 'e' (enchant), etc.

    Returns dict with keys:
        character: {name, server, region, faction, level, class, talents}
        equipped: {slot_name: item_id, ...}
        inventory: [item_id, ...]
    """
    # Strip outer $ delimiters
    export_str = export_str.strip()
    if export_str.startswith('$'):
        export_str = export_str[1:]
    if export_str.endswith('$'):
        export_str = export_str[:-1]

    # Split into sections by the dot-prefixed markers
    # First part is character header, then .s1, .q1, .inv sections
    sections = {}
    current_key = "header"
    current_parts = []

    for part in export_str.split(';'):
        if part.startswith('.'):
            # Save previous section
            sections[current_key] = current_parts
            current_key = part[1:]  # Remove the dot
            current_parts = []
        else:
            current_parts.append(part)

    sections[current_key] = current_parts

    # Parse header
    header = sections.get("header", [])
    character = {}
    if len(header) >= 9:
        character = {
            "version": header[0],
            "region": header[1],
            "server": header[2],
            "name": header[3],
            "guild": header[4],
            "faction": "Alliance" if header[5] == "1" else "Horde",
            "race_id": int(header[6]) if header[6] else 0,
            "level": int(header[7]) if header[7] else 0,
        }

    # Parse spec section (s1)
    spec_data = sections.get("s1", [])
    if len(spec_data) >= 2:
        character["class"] = spec_data[0]
        character["talents"] = spec_data[1]

    # Parse equipped items (q1) - delta encoded with slot markers
    equipped = {}
    equip_data = sections.get("q1", [])
    current_item_id = 0

    for entry in equip_data:
        if not entry:
            continue
        # Format: <delta>s<slot> with optional suffixes
        # e.g., "25589s1", "13s6", "26s13"
        match = re.match(r'^(\d+)s(\d+)', entry)
        if match:
            delta = int(match.group(1))
            slot_id = int(match.group(2))
            current_item_id += delta
            slot_name = AMR_SLOTS.get(slot_id, f"slot_{slot_id}")
            equipped[slot_name] = current_item_id

    # Parse inventory (inv) - delta encoded item IDs
    inventory = []
    inv_data = sections.get("inv", [])
    current_item_id = 0

    for entry in inv_data:
        if not entry:
            continue

        # Strip suffixes: 'f' = random suffix, 'e' = enchant, etc.
        # e.g., "490f41", "7f36", "131e1883"
        # The number before the letter is the item ID delta
        num_match = re.match(r'^(\d+)', entry)
        if num_match:
            delta = int(num_match.group(1))
            current_item_id += delta
            if current_item_id > 0:
                inventory.append(current_item_id)

    return {
        "character": character,
        "equipped": equipped,
        "inventory": inventory,
    }


def format_equipped(equipped, db_conn=None):
    """Pretty-print equipped items. If db_conn provided, look up names."""
    from constants import GEAR_SLOTS
    if db_conn:
        from db_loader import get_item

    lines = []
    for slot in GEAR_SLOTS:
        item_id = equipped.get(slot)
        if item_id:
            if db_conn:
                item = get_item(db_conn, item_id)
                name = item['name'] if item else "???"
                ilvl = item['ItemLevel'] if item else "?"
                lines.append(f"  {slot:15s} [{item_id}] {name} (iLvl {ilvl})")
            else:
                lines.append(f"  {slot:15s} [{item_id}]")
        else:
            lines.append(f"  {slot:15s} (empty)")
    return "\n".join(lines)


if __name__ == "__main__":
    import config
    from db_loader import load_db

    result = parse_amr_export(config.AMR_EXPORT)
    char = result["character"]
    print(f"Character: {char['name']} - Level {char['level']} {char['class']}")
    print(f"Server: {char['region']}-{char['server']} ({char['faction']})")
    print(f"\nEquipped Gear:")

    conn = load_db(config.DB_PATH)
    print(format_equipped(result["equipped"], conn))

    print(f"\nInventory: {len(result['inventory'])} items")
    # Show first 10 inventory items
    for item_id in result["inventory"][:10]:
        from db_loader import get_item
        item = get_item(conn, item_id)
        if item:
            print(f"  [{item_id}] {item['name']} (iLvl {item['ItemLevel']}, Q{item['Quality']})")
        else:
            print(f"  [{item_id}] (not in DB)")

    conn.close()
