# BiSHunter - TBC Classic Gear Advisor

A gear optimization tool for World of Warcraft: The Burning Crusade Classic. Parses AskMrRobot character exports, cross-references against a complete TBC item database (24,000+ items), and tells you exactly what gear to keep, what to vendor/disenchant, and what to farm next — for both your main spec and off spec.

## Features

- **Web UI** — WoW-themed dark interface with visual character sheet, inventory management, and upgrade tables
- **Wowhead Integration** — Authentic WoW item tooltips powered by Wowhead's TBC Classic embed system
- **AMR Export Parsing** — Paste your AskMrRobot export string and get a full breakdown of your equipped gear and inventory
- **Dual Spec Support** — Evaluate gear for both your main spec and off spec simultaneously (e.g., Prot main / Ret off)
- **BiS Lists** — Community-consensus Best-in-Slot lists for every phase (Pre-Raid through Sunwell)
- **Stat-Weight Scoring** — Items not on BiS lists are scored using spec-appropriate stat weights
- **Upgrade Priority** — See exactly what to farm next, where it drops, and how much of an upgrade it is
- **Vendor/DE Recommendations** — Identify gear that's safe to sell or disenchant because it's outclassed for both specs
- **CLI Mode** — Also works as a command-line tool for quick analysis

## Supported Specs

Currently supports:
- **Protection Paladin** (tank)
- **Retribution Paladin** (DPS)

## Requirements

- Python 3.8+
- Flask (`pip install flask`)
- The [burning-crusade-item-db](https://github.com/nexus-devs/burning-crusade-item-db) SQL dumps

## Setup

```bash
# Clone the repo
git clone https://github.com/shadowedqueens-maker/BiS-hunter.git
cd BiS-hunter

# Install dependencies
pip install -r requirements.txt

# Download the TBC item database
git clone https://github.com/nexus-devs/burning-crusade-item-db.git

# Update DB_PATH in config.py to point to your item database directory
```

## Usage

### Web UI (recommended)

```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

1. Paste your AskMrRobot export string
2. Select your main spec and off spec
3. Click **Analyze Gear**

### CLI Mode

```bash
# Run with the export string configured in config.py
python main.py

# Or pass an AMR export string directly
python main.py "$50;US;Dreamscythe;Danduvil;..."
```

## Web UI Tabs

- **Character** — Visual paper doll layout showing all equipped gear with quality colors, item levels, and dual-spec scores. Hover any item for Wowhead tooltips.
- **Inventory** — Categorized view of bag/bank items: Keep for Main Spec, Keep for Off Spec, and Vendor/Disenchant with gold totals.
- **Upgrades** — Per-phase upgrade priority tables. Toggle between main/off spec view. Shows BiS items you still need, score deltas, and drop sources.

## Project Structure

```
BiSHunter/
├── app.py            # Flask web application
├── main.py           # CLI entry point
├── config.py         # Paths, character config, AMR export string
├── constants.py      # WoW data mappings (stat types, slots, phases)
├── db_loader.py      # SQL dump parser -> in-memory SQLite
├── amr_parser.py     # AskMrRobot export string parser
├── bis_lists.py      # Hardcoded BiS item IDs per spec/phase/slot
├── scoring.py        # Stat-weight scoring engine
├── recommender.py    # Gear categorization and upgrade recommendations
├── requirements.txt  # Python dependencies
├── templates/
│   └── index.html    # Web UI template
└── static/
    ├── css/style.css # WoW-themed dark UI
    └── js/
        ├── app.js      # Main controller
        └── renderer.js # DOM builders with Wowhead tooltip integration
```

## How Scoring Works

Each item is scored by multiplying its stats by spec-appropriate weights:

**Protection Paladin** priorities: Defense Rating > Stamina > Spell Power (threat) > Dodge > Parry > Block > Hit

**Retribution Paladin** priorities: Strength > Hit Rating > Expertise > Crit > Haste > Attack Power

Items on the hardcoded BiS lists are always flagged as "keep" regardless of score. The scoring engine is used as a fallback for items not on any BiS list.

## Roadmap

- [ ] WoW addon with in-game UI
- [ ] Support for additional classes/specs
- [ ] Gem and enchant recommendations
- [ ] Import from Warcraft Logs / WoW Armory
- [ ] Full AskMrRobot-style optimization for TBC Classic

## License

MIT
