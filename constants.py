# constants.py - Mangos DB mappings and WoW constants for TBC Classic

# Mangos stat_type codes -> human readable names
STAT_TYPES = {
    0:  "mana",
    1:  "health",
    3:  "agility",
    4:  "strength",
    5:  "intellect",
    6:  "spirit",
    7:  "stamina",
    12: "defense_rating",
    13: "dodge_rating",
    14: "parry_rating",
    15: "block_rating",
    16: "melee_hit_rating",
    17: "ranged_hit_rating",
    18: "spell_hit_rating",
    19: "melee_crit_rating",
    20: "ranged_crit_rating",
    21: "spell_crit_rating",
    22: "melee_hit_taken_rating",
    23: "ranged_hit_taken_rating",
    24: "spell_hit_taken_rating",
    25: "melee_crit_taken_rating",
    26: "ranged_crit_taken_rating",
    27: "spell_crit_taken_rating",
    28: "melee_haste_rating",
    29: "ranged_haste_rating",
    30: "spell_haste_rating",
    31: "hit_rating",
    32: "crit_rating",
    33: "hit_taken_rating",
    34: "crit_taken_rating",
    35: "resilience_rating",
    36: "haste_rating",
    37: "expertise_rating",
    38: "attack_power",
    39: "ranged_attack_power",
    40: "feral_attack_power",
    41: "spell_healing_done",
    42: "spell_damage_done",
    43: "mana_regen",
    44: "armor_penetration_rating",
    45: "spell_power",
    46: "health_regen",
    47: "spell_penetration",
    48: "block_value",
}

# Unified stat aliases - map specific ratings to generic categories
# TBC uses both specific (16=melee_hit) and generic (31=hit_rating) codes
STAT_ALIASES = {
    "melee_hit_rating": "hit_rating",
    "ranged_hit_rating": "hit_rating",
    "spell_hit_rating": "spell_hit_rating",  # keep separate for casters
    "melee_crit_rating": "crit_rating",
    "ranged_crit_rating": "crit_rating",
    "spell_crit_rating": "spell_crit_rating",
    "melee_haste_rating": "haste_rating",
    "ranged_haste_rating": "haste_rating",
    "spell_haste_rating": "spell_haste_rating",
}

# WoW inventory_type codes -> slot names
INVENTORY_TYPES = {
    0:  "non_equip",
    1:  "head",
    2:  "neck",
    3:  "shoulder",
    4:  "shirt",
    5:  "chest",
    6:  "waist",
    7:  "legs",
    8:  "feet",
    9:  "wrists",
    10: "hands",
    11: "finger",
    12: "trinket",
    13: "one_hand",
    14: "shield",
    15: "ranged",
    16: "back",
    17: "two_hand",
    18: "tabard",
    19: "chest_robe",
    20: "main_hand",
    21: "off_hand",
    22: "held_in_off_hand",
    23: "ammo",
    24: "thrown",
    25: "ranged_gun",
    26: "quiver",
    28: "relic",
}

# AMR slot IDs -> slot names (WoW equipment slot indices)
AMR_SLOTS = {
    1:  "head",
    2:  "neck",
    3:  "shoulder",
    5:  "chest",
    6:  "waist",
    7:  "legs",
    8:  "feet",
    9:  "wrists",
    10: "hands",
    11: "finger1",
    12: "finger2",
    13: "trinket1",
    14: "trinket2",
    15: "back",
    16: "main_hand",
    17: "off_hand",
    18: "ranged_relic",
}

# Item quality codes
QUALITY_NAMES = {
    0: "Poor",       # Gray
    1: "Common",     # White
    2: "Uncommon",   # Green
    3: "Rare",       # Blue
    4: "Epic",       # Purple
    5: "Legendary",  # Orange
}

# Class bitmask values for AllowableClass field
# AllowableClass = -1 means all classes
# Otherwise it's a bitmask: 1 << (classId - 1)
CLASS_MASKS = {
    "warrior":  1,
    "paladin":  2,
    "hunter":   4,
    "rogue":    8,
    "priest":   16,
    "shaman":   64,
    "mage":     128,
    "warlock":  256,
    "druid":    1024,
}

PALADIN_CLASS_MASK = 2

# Item class codes (the 'class' column in unmodified.sql)
ITEM_CLASS_CONSUMABLE = 0
ITEM_CLASS_CONTAINER = 1
ITEM_CLASS_WEAPON = 2
ITEM_CLASS_GEM = 3
ITEM_CLASS_ARMOR = 4
ITEM_CLASS_REAGENT = 5
ITEM_CLASS_PROJECTILE = 6
ITEM_CLASS_TRADE_GOODS = 7
ITEM_CLASS_RECIPE = 9
ITEM_CLASS_QUIVER = 11
ITEM_CLASS_QUEST = 12
ITEM_CLASS_KEY = 13
ITEM_CLASS_MISC = 15

# Armor subclass codes
ARMOR_SUBCLASS_MISC = 0
ARMOR_SUBCLASS_CLOTH = 1
ARMOR_SUBCLASS_LEATHER = 2
ARMOR_SUBCLASS_MAIL = 3
ARMOR_SUBCLASS_PLATE = 4
ARMOR_SUBCLASS_SHIELD = 6
ARMOR_SUBCLASS_LIBRAM = 7  # Paladin relic
ARMOR_SUBCLASS_IDOL = 8    # Druid relic
ARMOR_SUBCLASS_TOTEM = 9   # Shaman relic

# Weapon subclass codes relevant to paladin
WEAPON_SUBCLASS_AXE_1H = 0
WEAPON_SUBCLASS_AXE_2H = 1
WEAPON_SUBCLASS_MACE_1H = 4
WEAPON_SUBCLASS_MACE_2H = 5
WEAPON_SUBCLASS_SWORD_1H = 7
WEAPON_SUBCLASS_SWORD_2H = 8
WEAPON_SUBCLASS_POLEARM = 6

# Equipment slots that exist for comparison
GEAR_SLOTS = [
    "head", "neck", "shoulder", "back", "chest",
    "wrists", "hands", "waist", "legs", "feet",
    "finger1", "finger2", "trinket1", "trinket2",
    "main_hand", "off_hand", "ranged_relic",
]

# Map inventory_type to which gear slots it can fill
INVENTORY_TYPE_TO_SLOTS = {
    1:  ["head"],
    2:  ["neck"],
    3:  ["shoulder"],
    5:  ["chest"],
    6:  ["waist"],
    7:  ["legs"],
    8:  ["feet"],
    9:  ["wrists"],
    10: ["hands"],
    11: ["finger1", "finger2"],
    12: ["trinket1", "trinket2"],
    13: ["main_hand", "off_hand"],    # one-hand weapons
    14: ["off_hand"],                  # shield
    16: ["back"],
    17: ["main_hand"],                 # two-handers use main_hand slot
    20: ["main_hand"],                 # main hand only weapons
    21: ["off_hand"],                  # off hand weapons
    22: ["off_hand"],                  # held in off hand (books etc)
    28: ["ranged_relic"],              # librams, idols, totems
}

# Phases and their associated instance IDs (from thatsmybis item_sources)
PHASES = {
    "pre_raid": {
        "name": "Pre-Raid",
        "instance_ids": [],  # Heroics, crafted, rep, quests - no raid instance
    },
    "t4": {
        "name": "Tier 4 (Kara/Gruul/Mag)",
        "instance_ids": [9, 10, 11],  # Karazhan, Gruul's Lair, Magtheridon's Lair
    },
    "t5": {
        "name": "Tier 5 (SSC/TK)",
        "instance_ids": [12, 14],  # Serpentshrine Cavern, Tempest Keep
    },
    "t6": {
        "name": "Tier 6 (Hyjal/BT/ZA)",
        "instance_ids": [13, 15, 16],  # Hyjal, Black Temple, Zul'Aman
    },
    "sunwell": {
        "name": "Sunwell Plateau",
        "instance_ids": [17],
    },
}

# TBC world bosses instance
WORLD_BOSSES_INSTANCE_IDS = [18]  # Doom Lord Kazzak, Doomwalker
