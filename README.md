# BiSHunter - TBC Classic Gear Advisor

A gear optimization tool for World of Warcraft: The Burning Crusade Classic. Parses AskMrRobot character exports, cross-references against a complete TBC item database, and tells you exactly what gear to keep, what to vendor/disenchant, and what to farm next — for both your main spec and off spec.

## Features

- **AMR Export Parsing** — Paste your AskMrRobot export string and get a full breakdown of your equipped gear and inventory
- **Dual Spec Support** — Evaluate gear for both your main spec and off spec simultaneously (e.g., Prot main / Ret off)
- **BiS Lists** — Hardcoded community-consensus Best-in-Slot lists for every phase (Pre-Raid through Sunwell)
- **Stat-Weight Scoring** — Items not on BiS lists are scored using spec-appropriate stat weights
- **Upgrade Priority** — See exactly what to farm next, where it drops, and how much of an upgrade it is
- **Vendor/DE Recommendations** — Identify gear that's safe to sell or disenchant because it's outclassed for both specs

## Supported Specs

Currently supports:
- **Protection Paladin** (tank)
- **Retribution Paladin** (DPS)

## Requirements

- Python 3.8+
- The [burning-crusade-item-db](https://github.com/nexus-devs/burning-crusade-item-db) SQL dumps (included as a dependency path in config)
- No external Python packages required (stdlib only)

## Setup

1. Clone this repo
2. Download or clone the [TBC item database](https://github.com/nexus-devs/burning-crusade-item-db)
3. Update `config.py` with:
   - `DB_PATH` — path to the item database directory
   - `AMR_EXPORT` — your AskMrRobot export string
   - `CHARACTER` — your character's main/off spec settings

## Usage

```bash
# Run with the export string configured in config.py
python main.py

# Or pass an AMR export string directly
python main.py "$50;US;Dreamscythe;Danduvil;..."
```

## Output

The tool generates a structured report with sections:

1. **Currently Equipped** — Your gear with scores for both specs
2. **Keep for Main Spec** — Inventory items that are BiS or upgrades for your main spec
3. **Keep for Off Spec** — Inventory items valuable for your off spec
4. **Vendor / Disenchant** — Items safe to sell, with vendor prices
5. **Upgrades to Farm** — Per-phase BiS items you're missing, sorted by priority, with drop sources

## Project Structure

```
BiSHunter/
├── main.py           # CLI entry point
├── config.py         # Paths, character config, AMR export string
├── constants.py      # WoW data mappings (stat types, slots, phases)
├── db_loader.py      # SQL dump parser -> in-memory SQLite
├── amr_parser.py     # AskMrRobot export string parser
├── bis_lists.py      # Hardcoded BiS item IDs per spec/phase/slot
├── scoring.py        # Stat-weight scoring engine
├── recommender.py    # Gear categorization and upgrade recommendations
└── README.md
```

## How Scoring Works

Each item is scored by multiplying its stats by spec-appropriate weights:

**Protection Paladin** priorities: Defense Rating > Stamina > Spell Power (threat) > Dodge > Parry > Block > Hit

**Retribution Paladin** priorities: Strength > Hit Rating > Expertise > Crit > Haste > Attack Power

Items on the hardcoded BiS lists are always flagged as "keep" regardless of score. The scoring engine is used as a fallback for items not on any BiS list.

## Future Plans

- WoW addon with in-game UI
- Support for additional classes/specs
- Gem and enchant recommendations
- Import from other sources (Warcraft Logs, WoW Armory)

## License

MIT
