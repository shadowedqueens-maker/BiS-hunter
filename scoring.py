# scoring.py - Stat-weight scoring engine for Protection and Retribution Paladin

from constants import STAT_TYPES, STAT_ALIASES

# Stat weights by spec - higher = more valuable
# These are approximate community-consensus weights for TBC Classic
STAT_WEIGHTS = {
    "prot": {
        # Survivability
        "defense_rating": 2.5,     # Critical until 490 def cap (requires 156 rating at 70)
        "stamina": 1.8,
        "dodge_rating": 1.3,
        "parry_rating": 1.2,
        "block_rating": 1.1,
        "block_value": 0.9,
        "armor": 0.015,            # Per-point (raw values are high, 100 armor ~ 1.5 score)

        # Threat (prot pally threat scales with spell damage)
        "spell_power": 1.6,
        "spell_damage_done": 1.6,
        "spell_healing_done": 0.0,  # Healing power doesn't help threat
        "hit_rating": 1.2,
        "spell_hit_rating": 1.1,
        "melee_hit_rating": 1.2,
        "expertise_rating": 1.0,

        # Secondary
        "intellect": 0.6,          # Mana pool matters for prot pally
        "strength": 0.4,           # Block value contribution (1 str = 0.5 BV) + minor AP
        "agility": 0.3,            # Minor dodge/armor contribution
        "spirit": 0.0,
        "crit_rating": 0.3,
        "melee_crit_rating": 0.3,
        "spell_crit_rating": 0.3,
        "haste_rating": 0.1,
        "attack_power": 0.05,
        "resilience_rating": 0.0,

        # Resistances (minor value for specific fights)
        "fire_res": 0.1,
        "nature_res": 0.1,
        "frost_res": 0.1,
        "shadow_res": 0.1,
        "arcane_res": 0.1,
    },

    "ret": {
        # Primary DPS stats
        "strength": 2.2,           # 1 STR = 2 AP for Paladin
        "hit_rating": 2.0,         # Until 9% cap (~142 rating at 70)
        "melee_hit_rating": 2.0,
        "expertise_rating": 1.8,
        "crit_rating": 1.4,
        "melee_crit_rating": 1.4,
        "haste_rating": 1.1,
        "attack_power": 0.55,      # Half of strength's value (1 STR = 2 AP)
        "armor_penetration_rating": 0.8,

        # Secondary
        "agility": 0.65,           # Crit + armor contribution
        "stamina": 0.15,           # Survival, minor priority for DPS
        "intellect": 0.3,          # Mana matters somewhat for ret
        "spell_power": 0.4,        # Ret abilities scale partially with spell power
        "spell_damage_done": 0.4,
        "spirit": 0.0,

        # Not useful for ret
        "defense_rating": 0.0,
        "dodge_rating": 0.0,
        "parry_rating": 0.0,
        "block_rating": 0.0,
        "block_value": 0.0,
        "resilience_rating": 0.0,
        "spell_hit_rating": 0.2,   # Some spells benefit
        "spell_crit_rating": 0.3,
    },
}

# DPS weight for weapon evaluation (per 1 DPS)
WEAPON_DPS_WEIGHT = {
    "prot": 0.5,    # Prot doesn't care much about weapon DPS
    "ret": 3.5,     # Ret cares a LOT about weapon DPS (Seal of Command, etc.)
}


def get_item_stats(item_row):
    """Extract all stats from an item row as a dict of {stat_name: value}."""
    stats = {}
    for i in range(1, 11):
        stat_type = item_row[f"stat_type{i}"]
        stat_value = item_row[f"stat_value{i}"]
        if stat_type and stat_value:
            stat_name = STAT_TYPES.get(stat_type, f"unknown_{stat_type}")
            # Resolve aliases to canonical names
            stat_name = STAT_ALIASES.get(stat_name, stat_name)
            stats[stat_name] = stats.get(stat_name, 0) + stat_value

    # Add armor
    if item_row["armor"]:
        stats["armor"] = item_row["armor"]

    # Add block value
    if item_row["block"]:
        stats["block_value"] = item_row["block"]

    return stats


def score_item(item_row, spec):
    """Score an item based on stat weights for a given spec.

    Args:
        item_row: sqlite3.Row from the items table
        spec: "prot" or "ret"

    Returns:
        float score (higher = better for that spec)
    """
    weights = STAT_WEIGHTS.get(spec, {})
    stats = get_item_stats(item_row)
    score = 0.0

    for stat_name, value in stats.items():
        weight = weights.get(stat_name, 0.0)
        score += value * weight

    # Add weapon DPS contribution
    if item_row["dmg_min1"] and item_row["dmg_max1"] and item_row["delay"]:
        delay = item_row["delay"]
        if delay > 0:
            avg_dmg = (item_row["dmg_min1"] + item_row["dmg_max1"]) / 2.0
            dps = avg_dmg / (delay / 1000.0)
            score += dps * WEAPON_DPS_WEIGHT.get(spec, 0)

    return round(score, 1)


def compare_items(item_a, item_b, spec):
    """Compare two items for a spec. Returns (score_a, score_b, delta)."""
    score_a = score_item(item_a, spec)
    score_b = score_item(item_b, spec)
    return score_a, score_b, round(score_a - score_b, 1)


def format_item_score(item_row, spec):
    """Format a single item's score breakdown for display."""
    weights = STAT_WEIGHTS.get(spec, {})
    stats = get_item_stats(item_row)
    total = score_item(item_row, spec)

    parts = []
    for stat_name, value in sorted(stats.items(), key=lambda x: -abs(x[1] * weights.get(x[0], 0))):
        weight = weights.get(stat_name, 0.0)
        contribution = value * weight
        if abs(contribution) >= 0.1:
            parts.append(f"{stat_name}={value} (x{weight}={contribution:+.1f})")

    return f"Score: {total:.1f} | {', '.join(parts)}"


if __name__ == "__main__":
    import config
    from db_loader import load_db, get_item

    conn = load_db(config.DB_PATH)

    # Score Danduvil's current gear for both specs
    test_ids = [25589, 25602, 25628, 25644, 25762, 25914, 25927, 25937,
                27733, 29786, 30258, 30267, 30275, 30352, 31519, 31527]

    print("\n=== Item Scores: Prot vs Ret ===")
    for item_id in test_ids:
        item = get_item(conn, item_id)
        if item:
            prot_score = score_item(item, "prot")
            ret_score = score_item(item, "ret")
            print(f"  [{item_id}] {item['name']:40s} Prot: {prot_score:6.1f}  Ret: {ret_score:6.1f}")

    # Compare a BiS item vs current
    print("\n=== Comparison: Honed Voidaxe vs King's Defender ===")
    current = get_item(conn, 25762)  # Honed Voidaxe
    bis = get_item(conn, 28749)      # King's Defender
    if current and bis:
        print(f"  Current: {current['name']}")
        print(f"    {format_item_score(current, 'prot')}")
        print(f"  BiS:     {bis['name']}")
        print(f"    {format_item_score(bis, 'prot')}")

    conn.close()
