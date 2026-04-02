# db_loader.py - Parse TBC item database SQL dumps into in-memory SQLite

import os
import re
import sqlite3


# Column names from unmodified.sql INSERT statement (line 180)
UNMODIFIED_COLUMNS = [
    "entry", "class", "subclass", "unk0", "name", "displayid", "Quality", "Flags",
    "BuyCount", "BuyPrice", "SellPrice", "InventoryType", "AllowableClass", "AllowableRace",
    "ItemLevel", "RequiredLevel", "RequiredSkill", "RequiredSkillRank", "requiredspell",
    "requiredhonorrank", "RequiredCityRank", "RequiredReputationFaction", "RequiredReputationRank",
    "maxcount", "stackable", "ContainerSlots",
    "stat_type1", "stat_value1", "stat_type2", "stat_value2",
    "stat_type3", "stat_value3", "stat_type4", "stat_value4",
    "stat_type5", "stat_value5", "stat_type6", "stat_value6",
    "stat_type7", "stat_value7", "stat_type8", "stat_value8",
    "stat_type9", "stat_value9", "stat_type10", "stat_value10",
    "dmg_min1", "dmg_max1", "dmg_type1", "dmg_min2", "dmg_max2", "dmg_type2",
    "dmg_min3", "dmg_max3", "dmg_type3", "dmg_min4", "dmg_max4", "dmg_type4",
    "dmg_min5", "dmg_max5", "dmg_type5",
    "armor", "holy_res", "fire_res", "nature_res", "frost_res", "shadow_res", "arcane_res",
    "delay", "ammo_type", "RangedModRange",
    "spellid_1", "spelltrigger_1", "spellcharges_1", "spellppmRate_1",
    "spellcooldown_1", "spellcategory_1", "spellcategorycooldown_1",
    "spellid_2", "spelltrigger_2", "spellcharges_2", "spellppmRate_2",
    "spellcooldown_2", "spellcategory_2", "spellcategorycooldown_2",
    "spellid_3", "spelltrigger_3", "spellcharges_3", "spellppmRate_3",
    "spellcooldown_3", "spellcategory_3", "spellcategorycooldown_3",
    "spellid_4", "spelltrigger_4", "spellcharges_4", "spellppmRate_4",
    "spellcooldown_4", "spellcategory_4", "spellcategorycooldown_4",
    "spellid_5", "spelltrigger_5", "spellcharges_5", "spellppmRate_5",
    "spellcooldown_5", "spellcategory_5", "spellcategorycooldown_5",
    "bonding", "description", "PageText", "LanguageID", "PageMaterial",
    "startquest", "lockid", "Material", "sheath", "RandomProperty", "RandomSuffix",
    "block", "itemset", "MaxDurability", "area", "Map", "BagFamily", "TotemCategory",
    "socketColor_1", "socketContent_1", "socketColor_2", "socketContent_2",
    "socketColor_3", "socketContent_3", "socketBonus", "GemProperties",
    "RequiredDisenchantSkill", "ArmorDamageModifier", "DisenchantID", "FoodType",
    "minMoneyLoot", "maxMoneyLoot", "Duration", "ExtraFlags",
]

# Columns we actually care about for item evaluation
ITEM_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS items (
    entry INTEGER PRIMARY KEY,
    class INTEGER,
    subclass INTEGER,
    name TEXT,
    displayid INTEGER,
    Quality INTEGER,
    Flags INTEGER,
    BuyPrice INTEGER,
    SellPrice INTEGER,
    InventoryType INTEGER,
    AllowableClass INTEGER,
    AllowableRace INTEGER,
    ItemLevel INTEGER,
    RequiredLevel INTEGER,
    RequiredSkill INTEGER,
    RequiredSkillRank INTEGER,
    RequiredReputationFaction INTEGER,
    RequiredReputationRank INTEGER,
    stat_type1 INTEGER, stat_value1 INTEGER,
    stat_type2 INTEGER, stat_value2 INTEGER,
    stat_type3 INTEGER, stat_value3 INTEGER,
    stat_type4 INTEGER, stat_value4 INTEGER,
    stat_type5 INTEGER, stat_value5 INTEGER,
    stat_type6 INTEGER, stat_value6 INTEGER,
    stat_type7 INTEGER, stat_value7 INTEGER,
    stat_type8 INTEGER, stat_value8 INTEGER,
    stat_type9 INTEGER, stat_value9 INTEGER,
    stat_type10 INTEGER, stat_value10 INTEGER,
    dmg_min1 REAL, dmg_max1 REAL, dmg_type1 INTEGER,
    dmg_min2 REAL, dmg_max2 REAL, dmg_type2 INTEGER,
    armor INTEGER,
    holy_res INTEGER, fire_res INTEGER, nature_res INTEGER,
    frost_res INTEGER, shadow_res INTEGER, arcane_res INTEGER,
    delay INTEGER,
    spellid_1 INTEGER, spelltrigger_1 INTEGER,
    spellid_2 INTEGER, spelltrigger_2 INTEGER,
    spellid_3 INTEGER, spelltrigger_3 INTEGER,
    spellid_4 INTEGER, spelltrigger_4 INTEGER,
    spellid_5 INTEGER, spelltrigger_5 INTEGER,
    bonding INTEGER,
    RandomProperty INTEGER,
    RandomSuffix INTEGER,
    block INTEGER,
    itemset INTEGER,
    MaxDurability INTEGER,
    socketColor_1 INTEGER, socketColor_2 INTEGER, socketColor_3 INTEGER,
    socketBonus INTEGER, GemProperties INTEGER
)
"""

# Indices for extracting relevant columns from the full row
# Maps our SQLite column name -> index in UNMODIFIED_COLUMNS
_COL_INDEX = {name: i for i, name in enumerate(UNMODIFIED_COLUMNS)}

COLUMNS_TO_EXTRACT = [
    "entry", "class", "subclass", "name", "displayid", "Quality", "Flags",
    "BuyPrice", "SellPrice", "InventoryType", "AllowableClass", "AllowableRace",
    "ItemLevel", "RequiredLevel", "RequiredSkill", "RequiredSkillRank",
    "RequiredReputationFaction", "RequiredReputationRank",
    "stat_type1", "stat_value1", "stat_type2", "stat_value2",
    "stat_type3", "stat_value3", "stat_type4", "stat_value4",
    "stat_type5", "stat_value5", "stat_type6", "stat_value6",
    "stat_type7", "stat_value7", "stat_type8", "stat_value8",
    "stat_type9", "stat_value9", "stat_type10", "stat_value10",
    "dmg_min1", "dmg_max1", "dmg_type1", "dmg_min2", "dmg_max2", "dmg_type2",
    "armor", "holy_res", "fire_res", "nature_res", "frost_res", "shadow_res", "arcane_res",
    "delay",
    "spellid_1", "spelltrigger_1", "spellid_2", "spelltrigger_2",
    "spellid_3", "spelltrigger_3", "spellid_4", "spelltrigger_4",
    "spellid_5", "spelltrigger_5",
    "bonding", "RandomProperty", "RandomSuffix",
    "block", "itemset", "MaxDurability",
    "socketColor_1", "socketColor_2", "socketColor_3",
    "socketBonus", "GemProperties",
]

EXTRACT_INDICES = [_COL_INDEX[c] for c in COLUMNS_TO_EXTRACT]


def _parse_value(val_str):
    """Parse a single SQL value string into Python type."""
    val_str = val_str.strip()
    if val_str.startswith("'") and val_str.endswith("'"):
        # String value - unescape SQL single quotes
        return val_str[1:-1].replace("\\'", "'").replace("''", "'")
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        return val_str


def _tokenize_row(row_str):
    """Parse a parenthesized SQL value tuple into a list of raw value strings.
    Handles escaped quotes inside strings."""
    values = []
    current = []
    in_string = False
    i = 0
    while i < len(row_str):
        ch = row_str[i]
        if in_string:
            if ch == '\\' and i + 1 < len(row_str):
                current.append(ch)
                current.append(row_str[i + 1])
                i += 2
                continue
            elif ch == "'":
                # Check for escaped '' (double single quote)
                if i + 1 < len(row_str) and row_str[i + 1] == "'":
                    current.append("''")
                    i += 2
                    continue
                else:
                    in_string = False
                    current.append(ch)
            else:
                current.append(ch)
        else:
            if ch == "'":
                in_string = True
                current.append(ch)
            elif ch == ',':
                values.append(''.join(current))
                current = []
            else:
                current.append(ch)
        i += 1
    if current:
        values.append(''.join(current))
    return values


def _parse_items_from_unmodified(filepath):
    """Parse all item rows from unmodified.sql, yielding extracted column tuples."""
    count = 0
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        in_values = False
        for line in f:
            stripped = line.strip()
            if stripped.startswith("INSERT INTO `items`"):
                in_values = True
                # The VALUES keyword is at the end of this line
                continue
            if not in_values:
                continue
            # Stop at lines that don't start with '('
            if not stripped.startswith('('):
                if stripped.startswith('LOCK') or stripped.startswith('/*!') or stripped == '':
                    in_values = False
                    continue
                # Could be continuation of previous INSERT
                continue

            # Strip leading '(' and trailing '),' or ');'
            row_str = stripped
            if row_str.startswith('('):
                row_str = row_str[1:]
            if row_str.endswith('),'):
                row_str = row_str[:-2]
            elif row_str.endswith(');'):
                row_str = row_str[:-2]
                in_values = False  # Last row of this INSERT block
            elif row_str.endswith(')'):
                row_str = row_str[:-1]

            tokens = _tokenize_row(row_str)
            if len(tokens) < len(UNMODIFIED_COLUMNS):
                continue  # Skip malformed rows

            # Extract only the columns we care about
            extracted = []
            for idx in EXTRACT_INDICES:
                extracted.append(_parse_value(tokens[idx]))

            count += 1
            yield tuple(extracted)

    print(f"  Parsed {count} items from unmodified.sql")


def _parse_thatsmybis_inserts(filepath):
    """Parse INSERT VALUES from a thatsmybis table dump."""
    rows = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Find INSERT INTO ... VALUES (...),(...);
    pattern = re.compile(r"INSERT INTO `\w+` VALUES\s*(.*?);", re.DOTALL)
    for match in pattern.finditer(content):
        values_str = match.group(1)
        # Split into individual row tuples
        depth = 0
        current = []
        in_str = False
        i = 0
        while i < len(values_str):
            ch = values_str[i]
            if in_str:
                if ch == '\\' and i + 1 < len(values_str):
                    current.append(ch)
                    current.append(values_str[i + 1])
                    i += 2
                    continue
                elif ch == "'":
                    in_str = False
            else:
                if ch == "'":
                    in_str = True
                elif ch == '(':
                    depth += 1
                    if depth == 1:
                        current = []
                        i += 1
                        continue
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        row_str = ''.join(current)
                        tokens = _tokenize_row(row_str)
                        rows.append(tuple(_parse_value(t) for t in tokens))
                        i += 1
                        continue
            current.append(ch)
            i += 1
    return rows


def load_db(db_path):
    """Load TBC item database from SQL dumps into in-memory SQLite.

    Args:
        db_path: Path to the burning-crusade-item-db-main directory

    Returns:
        sqlite3.Connection to the in-memory database
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Create tables
    cur.execute(ITEM_TABLE_SQL)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS instances (
            id INTEGER PRIMARY KEY,
            name TEXT,
            short_name TEXT,
            slug TEXT,
            "order" INTEGER,
            expansion_id INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_sources (
            id INTEGER PRIMARY KEY,
            name TEXT,
            slug TEXT,
            instance_id INTEGER,
            npc_id INTEGER,
            object_id INTEGER,
            "order" INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_item_sources (
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            item_source_id INTEGER
        )
    """)

    # Load items from unmodified.sql
    print("Loading items from unmodified.sql...")
    unmodified_path = os.path.join(db_path, "db", "unmodified.sql")
    placeholders = ",".join(["?"] * len(COLUMNS_TO_EXTRACT))
    col_names = ",".join(COLUMNS_TO_EXTRACT)
    insert_sql = f"INSERT OR IGNORE INTO items ({col_names}) VALUES ({placeholders})"

    batch = []
    for row in _parse_items_from_unmodified(unmodified_path):
        batch.append(row)
        if len(batch) >= 1000:
            cur.executemany(insert_sql, batch)
            batch = []
    if batch:
        cur.executemany(insert_sql, batch)

    # Load thatsmybis tables
    tmb_dir = os.path.join(db_path, "thatsmybis", "tables")

    print("Loading instances...")
    instances_path = os.path.join(tmb_dir, "instances.sql")
    if os.path.exists(instances_path):
        for row in _parse_thatsmybis_inserts(instances_path):
            # (id, name, short_name, slug, order, expansion_id, created_at, updated_at)
            cur.execute(
                'INSERT OR IGNORE INTO instances (id, name, short_name, slug, "order", expansion_id) '
                "VALUES (?, ?, ?, ?, ?, ?)",
                (row[0], row[1], row[2], row[3], row[4], row[5])
            )

    print("Loading item_sources...")
    sources_path = os.path.join(tmb_dir, "item_sources.sql")
    if os.path.exists(sources_path):
        for row in _parse_thatsmybis_inserts(sources_path):
            # (id, name, slug, instance_id, npc_id, object_id, order, created_at, updated_at)
            cur.execute(
                'INSERT OR IGNORE INTO item_sources (id, name, slug, instance_id, npc_id, object_id, "order") '
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            )

    print("Loading item_item_sources...")
    iis_path = os.path.join(tmb_dir, "item_item_sources.sql")
    if os.path.exists(iis_path):
        for row in _parse_thatsmybis_inserts(iis_path):
            # (id, item_id, item_source_id, created_at, updated_at)
            cur.execute(
                "INSERT OR IGNORE INTO item_item_sources (id, item_id, item_source_id) VALUES (?, ?, ?)",
                (row[0], row[1], row[2])
            )

    # Create useful indices
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_invtype ON items(InventoryType)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_quality ON items(Quality)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_class ON items(class)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_level ON items(ItemLevel)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_iis_item ON item_item_sources(item_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_iis_source ON item_item_sources(item_source_id)")

    conn.commit()

    # Print stats
    cur.execute("SELECT COUNT(*) FROM items")
    print(f"  Total items: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM instances")
    print(f"  Total instances: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM item_sources")
    print(f"  Total item sources: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM item_item_sources")
    print(f"  Total item-source links: {cur.fetchone()[0]}")

    return conn


def get_item(conn, item_id):
    """Fetch a single item by entry ID. Returns sqlite3.Row or None."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE entry = ?", (item_id,))
    return cur.fetchone()


def get_item_source(conn, item_id):
    """Get the drop source info for an item. Returns list of (source_name, instance_name)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name as source_name, i.name as instance_name, i.short_name
        FROM item_item_sources iis
        JOIN item_sources s ON iis.item_source_id = s.id
        LEFT JOIN instances i ON s.instance_id = i.id
        WHERE iis.item_id = ?
    """, (item_id,))
    return cur.fetchall()


if __name__ == "__main__":
    import config
    conn = load_db(config.DB_PATH)

    # Quick test - look up Danduvil's equipped items
    test_ids = [25589, 25602, 25628, 25644, 25762, 25914, 25927, 25937,
                27733, 29786, 30258, 30267, 30275, 30352, 31519, 31527]
    print("\n=== Danduvil's Equipped Gear ===")
    for item_id in test_ids:
        item = get_item(conn, item_id)
        if item:
            stats = []
            for i in range(1, 11):
                st = item[f"stat_type{i}"]
                sv = item[f"stat_value{i}"]
                if st and sv:
                    from constants import STAT_TYPES
                    stat_name = STAT_TYPES.get(st, f"unk_{st}")
                    stats.append(f"{stat_name}={sv}")
            print(f"  [{item['entry']}] {item['name']} (iLvl {item['ItemLevel']}, "
                  f"Q{item['Quality']}) - {', '.join(stats) if stats else 'no stats (random enchant?)'}")

    conn.close()
