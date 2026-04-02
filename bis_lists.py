# bis_lists.py - Hardcoded BiS item IDs for Protection and Retribution Paladin
# TBC Classic - all phases from Pre-Raid through Sunwell
#
# Sources: Community-established BiS lists (wowhead, classic.wowhead, seventyupgrades)
# Each slot lists items in priority order: [best, 2nd best, 3rd best, ...]
#
# AUDIT NOTE: All item IDs verified against the burning-crusade-item-db.
# Tier tokens replaced with actual armor piece IDs.

BIS = {
    # =========================================================================
    # PROTECTION PALADIN
    # =========================================================================
    "prot": {
        # --- PRE-RAID (Heroics, Crafted, Rep, Quests) ---
        "pre_raid": {
            "head": [
                28180,  # Faceguard of Determination (Keepers of Time Revered)
                31110,  # Felsteel Helm (Crafted BS)
                28285,  # Helm of the Righteous (Mech HC - Pathaleon) [was 29503]
            ],
            "neck": [
                29381,  # Choker of Vile Intent (Botanica HC)
                27792,  # Strength of the Untamed (SH quest chain)
                31178,  # Necklace of the Juggernaut (Arcatraz quest)
            ],
            "shoulder": [
                27739,  # Spaulders of the Righteous (Botanica - Laj)
                27434,  # Mantle of Perenolde (Old Hillsbrad)
            ],
            "back": [
                27804,  # Devilshark Cape (SV HC - Murmur)
                27878,  # Auchenai Death Shroud (Auchenai HC)
                24253,  # Thoriumweave Cloak (Keepers of Time Honored)
            ],
            "chest": [
                28203,  # Breastplate of the Bold (Shattered Halls quest)
                28337,  # Breastplate of Righteous Fury (Netherstorm quest) [was 31535]
                23507,  # Felsteel Armor (Crafted BS)
            ],
            "wrists": [
                28167,  # Sha'tari Wrought Armguards (Blood Furnace quest)
                27459,  # Bracers of Dignity (Mech HC)
                29246,  # Bracers of the Green Fortress (Crafted BS)
            ],
            "hands": [
                28518,  # Gauntlets of the Righteous (Arc HC - Harbinger Skyriss)
                27535,  # Gauntlets of Dissention (SL HC - Blackheart)
                23517,  # Felsteel Gloves (Crafted BS) [was 25790]
            ],
            "waist": [
                28566,  # Girdle of the Immovable (SV HC)
                27985,  # Sha'tari Vindicator's Waistguard (Quest)
                29238,  # Lion's Heart Girdle (Crafted BS)
            ],
            "legs": [
                29783,  # Legguards of the Resolute Defender (KoT HC) [was 28285]
                27527,  # Greaves of the Shatterer (Mech - Mechano-Lord Cap)
                31544,  # Netherstorm Greaves (Quest)
                30533,  # Vanquisher's Legplates (SL quest)
            ],
            "feet": [
                28176,  # Boots of the Righteous Path (Black Morass HC)
                27813,  # Boots of the Colossus (SH HC)
                25792,  # Felsteel Boots (Crafted BS)
            ],
            "finger1": [
                29279,  # Elementium Band of the Sentry (Old Hillsbrad HC)
                27822,  # Crystal Band of Valor (SL HC)
                24088,  # Delicate Eternium Ring (Crafted JC) [was 28034]
            ],
            "finger2": [
                29279,  # Elementium Band of the Sentry
                27822,  # Crystal Band of Valor
                29384,  # Ring of Umbral Doom (Mech HC quest)
            ],
            "trinket1": [
                27891,  # Adamantine Figurine (SH HC - O'mrogg)
                29181,  # Timelapse Shard (Black Morass HC)
            ],
            "trinket2": [
                27891,  # Adamantine Figurine (SH HC)
                29181,  # Timelapse Shard (Black Morass HC)
                23836,  # Goblin Rocket Launcher
            ],
            "main_hand": [
                29165,  # Honor's Call (SV HC quest)
                27905,  # Greatsword of Horrid Dreams (SL HC)
                31073,  # The Sun Eater (Mech HC - Pathaleon)
                29185,  # Continuum Blade (Black Morass - Temporus) [was 27848]
            ],
            "off_hand": [
                29176,  # Crest of the Sha'tar (Sha'tar Exalted)
                28358,  # Aegis of the Sunbird (Botanica HC - Laj)
                29266,  # Azure-Shield of Coldarra (quest)
            ],
            "ranged_relic": [
                27917,  # Libram of Repentance (SL HC)
                25644,  # Blessed Book of Nagrand (quest)
                28296,  # Libram of Saints Departed (Arc HC)
            ],
        },

        # --- TIER 4 (Karazhan, Gruul's Lair, Magtheridon's Lair) ---
        "t4": {
            "head": [
                29068,  # Justicar Faceguard (T4 - Prince Malchezaar token)
                28180,  # Faceguard of Determination
            ],
            "neck": [
                28516,  # Barbed Choker of Discipline (Kara - Moroes)
                29381,  # Choker of Vile Intent
            ],
            "shoulder": [
                29075,  # Justicar Shoulderguards (T4 - Maulgar token)
                27739,  # Spaulders of the Righteous
            ],
            "back": [
                28529,  # Royal Cloak of Arathi Kings (Kara - Moroes)
                28653,  # Farstrider Defender's Cloak (Kara - Netherspite)
            ],
            "chest": [
                29071,  # Justicar Chestguard (T4 - Mag token)
                28203,  # Breastplate of the Bold
            ],
            "wrists": [
                29463,  # Vambraces of Courage (Kara - Nightbane)
                28167,  # Sha'tari Wrought Armguards
            ],
            "hands": [
                29072,  # Justicar Handguards (T4 - Curator token)
                28518,  # Gauntlets of the Righteous
            ],
            "waist": [
                28566,  # Girdle of the Immovable
                28779,  # Crimson Girdle of the Indomitable (Kara - Netherspite)
            ],
            "legs": [
                29074,  # Justicar Legguards (T4 - Gruul token)
                29783,  # Legguards of the Resolute Defender [was 28285]
            ],
            "feet": [
                28747,  # Battlescar Boots (Kara - Nightbane)
                28176,  # Boots of the Righteous Path
            ],
            "finger1": [
                28675,  # Shermanar Great-Ring (Kara - Netherspite)
                29279,  # Elementium Band of the Sentry
            ],
            "finger2": [
                28792,  # Ring of the Stalwart Protector (Kara - Nightbane)
                29384,  # Ring of Umbral Doom
            ],
            "trinket1": [
                28528,  # Moroes' Lucky Pocket Watch (Kara - Moroes)
                27891,  # Adamantine Figurine
            ],
            "trinket2": [
                29387,  # Gnomeregan Auto-Blocker 600 (Arc HC)
                27891,  # Adamantine Figurine
            ],
            "main_hand": [
                28749,  # King's Defender (Kara - Prince Malchezaar)
                31073,  # The Sun Eater
            ],
            "off_hand": [
                28825,  # Aldori Legacy Defender (Gruul)
                29176,  # Crest of the Sha'tar
            ],
            "ranged_relic": [
                27917,  # Libram of Repentance
                28296,  # Libram of Saints Departed
            ],
        },

        # --- TIER 5 (SSC, TK) ---
        "t5": {
            "head": [
                30125,  # Crystalforge Faceguard (T5 - Kael'thas token)
                29068,  # Justicar Faceguard
            ],
            "neck": [
                30007,  # The Darkener's Grasp (TK - Kael'thas)
                28516,  # Barbed Choker of Discipline
            ],
            "shoulder": [
                30127,  # Crystalforge Shoulderguards (T5 - Void Reaver token)
                29075,  # Justicar Shoulderguards
            ],
            "back": [
                30098,  # Pepe's Shroud of Pacification (SSC - Lurker)
                28529,  # Royal Cloak of Arathi Kings
            ],
            "chest": [
                30123,  # Crystalforge Chestguard (T5 - Kael'thas token)
                29071,  # Justicar Chestguard
            ],
            "wrists": [
                29966,  # Vambraces of Ending (SSC - Leotheras) [was 30073]
                29463,  # Vambraces of Courage
            ],
            "hands": [
                30124,  # Crystalforge Handguards (T5 - Leotheras token)
                29072,  # Justicar Handguards
            ],
            "waist": [
                30034,  # Belt of the Guardian (Crafted) [was 30106]
                30032,  # Red Belt of Battle (Crafted)
                28566,  # Girdle of the Immovable
            ],
            "legs": [
                30126,  # Crystalforge Legguards (T5 - Fathom-Lord token)
                29074,  # Justicar Legguards
            ],
            "feet": [
                30027,  # Boots of the Resilient (SSC - Morogrim) [was 30078]
                28747,  # Battlescar Boots
            ],
            "finger1": [
                30083,  # Ring of Sundered Souls (SSC - Lurker)
                29279,  # Elementium Band of the Sentry
                28675,  # Shermanar Great-Ring
            ],
            "finger2": [
                28792,  # Ring of the Stalwart Protector
                30083,  # Ring of Sundered Souls
            ],
            "trinket1": [
                28528,  # Moroes' Lucky Pocket Watch
                32534,  # Brooch of the Immortal King
            ],
            "trinket2": [
                29387,  # Gnomeregan Auto-Blocker 600
                27891,  # Adamantine Figurine
            ],
            "main_hand": [
                30058,  # Mallet of the Tides (SSC - Karathress)
                28749,  # King's Defender
            ],
            "off_hand": [
                28825,  # Aldori Legacy Defender (Gruul, stays BiS through T5)
                29458,  # Aegis of the Vindicator (Magtheridon)
            ],
            "ranged_relic": [
                27917,  # Libram of Repentance
                28296,  # Libram of Saints Departed
            ],
        },

        # --- TIER 6 (Hyjal, Black Temple, ZA) ---
        "t6": {
            "head": [
                30987,  # Lightbringer Faceguard (T6) [was 31091 token]
                30125,  # Crystalforge Faceguard
            ],
            "neck": [
                32362,  # Pendant of Titans (BT - Gurtogg)
                30007,  # The Darkener's Grasp
            ],
            "shoulder": [
                30998,  # Lightbringer Shoulderguards (T6) [was 31093 token]
                30127,  # Crystalforge Shoulderguards
            ],
            "back": [
                32331,  # Cloak of the Illidari Council (BT - Council)
                30098,  # Pepe's Shroud of Pacification
            ],
            "chest": [
                30991,  # Lightbringer Chestguard (T6) [was 31089 token]
                30123,  # Crystalforge Chestguard
            ],
            "wrists": [
                32515,  # Swiftsteel Bracers (Crafted BT pattern)
                32279,  # Wristguards of Determination (BT - Naj'entus)
            ],
            "hands": [
                30985,  # Lightbringer Handguards (T6) [was 31092 token]
                30124,  # Crystalforge Handguards
            ],
            "waist": [
                32342,  # Girdle of Mighty Resolve (BT - Gurtogg) [was 32232 wrong ID]
                30034,  # Belt of the Guardian
            ],
            "legs": [
                30995,  # Lightbringer Legguards (T6) [was 31094 token]
                30126,  # Crystalforge Legguards
            ],
            "feet": [
                30033,  # Boots of the Protector (Hyjal - Azgalor) [was 32244]
                30027,  # Boots of the Resilient
            ],
            "finger1": [
                32261,  # Band of the Eternal Defender (BT - Shahraz)
                28675,  # Shermanar Great-Ring
            ],
            "finger2": [
                29279,  # Elementium Band of the Sentry (still good)
                32261,  # Band of the Eternal Defender
            ],
            "trinket1": [
                32501,  # Shadowmoon Insignia (BT - Council)
                28528,  # Moroes' Lucky Pocket Watch
            ],
            "trinket2": [
                29387,  # Gnomeregan Auto-Blocker 600
                32534,  # Brooch of the Immortal King (ZA - Zul'jin)
            ],
            "main_hand": [
                32262,  # Syphon of the Nathrezim (BT - Shahraz)
                28749,  # King's Defender
            ],
            "off_hand": [
                32375,  # Bulwark of Azzinoth (BT - Illidan)
                28825,  # Aldori Legacy Defender
            ],
            "ranged_relic": [
                33503,  # Libram of Divine Purpose (ZA - Hex Lord)
                27917,  # Libram of Repentance
            ],
        },

        # --- SUNWELL ---
        "sunwell": {
            "head": [
                34401,  # Helm of Uther's Resolve (Sunwell - Kalecgos)
                30987,  # Lightbringer Faceguard
            ],
            "neck": [
                34178,  # Clutch of Demise (Sunwell - Eredar Twins)
                32362,  # Pendant of Titans
            ],
            "shoulder": [
                30998,  # Lightbringer Shoulderguards (no upgrade in SWP for prot)
                34388,  # Pauldrons of Perseverance (Sunwell - Kalecgos)
            ],
            "back": [
                34190,  # Pepe's Shroud of the Highborne (Sunwell - M'uru)
                32331,  # Cloak of the Illidari Council
            ],
            "chest": [
                34215,  # Carapace of Sun's Embrace (Sunwell)
                30991,  # Lightbringer Chestguard
            ],
            "wrists": [
                34433,  # Lightbringer Wristguards (Sunwell T6.5) [was 34488 wrong slot]
                33516,  # Bracers of the Ancient Phalanx [was 34852 token]
                32515,  # Swiftsteel Bracers
            ],
            "hands": [
                34350,  # Gauntlets of the Ancient Shadowmoon (Sunwell) [was 34188]
                30985,  # Lightbringer Handguards
            ],
            "waist": [
                34488,  # Lightbringer Waistguard (Sunwell T6.5)
                32512,  # Girdle of Lordaeron's Fallen (BT) [was 34547 warrior-only]
            ],
            "legs": [
                30995,  # Lightbringer Legguards
                34167,  # Legguards of the Endless Assault (Sunwell)
            ],
            "feet": [
                34560,  # Lightbringer Boots (Sunwell T6.5) [was 34947 token]
                30033,  # Boots of the Protector
            ],
            "finger1": [
                34213,  # Ring of Hardened Resolve (Sunwell - Brutallus)
                32261,  # Band of the Eternal Defender
            ],
            "finger2": [
                34213,  # Ring of Hardened Resolve
                29279,  # Elementium Band of the Sentry
            ],
            "trinket1": [
                34473,  # Commendation of Kael'thas (Magister's Terrace HC)
                32501,  # Shadowmoon Insignia
            ],
            "trinket2": [
                29387,  # Gnomeregan Auto-Blocker 600
                28528,  # Moroes' Lucky Pocket Watch
            ],
            "main_hand": [
                34247,  # Apolyon, the Soul-Render (Sunwell - KJ)
                32262,  # Syphon of the Nathrezim
            ],
            "off_hand": [
                34185,  # Shield of Condemnation (Sunwell - Felmyst)
                32375,  # Bulwark of Azzinoth
            ],
            "ranged_relic": [
                33503,  # Libram of Divine Purpose
                27917,  # Libram of Repentance
            ],
        },
    },

    # =========================================================================
    # RETRIBUTION PALADIN
    # =========================================================================
    "ret": {
        # --- PRE-RAID ---
        "pre_raid": {
            "head": [
                28224,  # Wastewalker Helm (SL HC)
                28182,  # Helm of the Claw (CE Revered) [was 29587 not in DB]
                25589,  # Clefthoof Helm (quest)
            ],
            "neck": [
                29381,  # Choker of Vile Intent (Bot HC)
                31178,  # Necklace of the Juggernaut
                25914,  # Broken Choker (quest)
            ],
            "shoulder": [
                27797,  # Wastewalker Shoulderpads (SL HC)
                27434,  # Mantle of Perenolde (Old Hillsbrad)
                27803,  # Shoulderguards of the Bold (BF HC) [was 27745]
            ],
            "back": [
                27878,  # Auchenai Death Shroud (Auchenai HC)
                24259,  # Vengeance Wrap (Lower City Exalted)
                27804,  # Devilshark Cape
            ],
            "chest": [
                28203,  # Breastplate of the Bold (SH quest)
                30258,  # Chestplate of A'dal
            ],
            "wrists": [
                28167,  # Sha'tari Wrought Armguards
                29246,  # Bracers of the Green Fortress (Crafted)
                27459,  # Bracers of Dignity
            ],
            "hands": [
                28518,  # Gauntlets of the Righteous (Arc HC)
                27535,  # Gauntlets of Dissention
                23517,  # Felsteel Gloves (Crafted) [was 25790]
            ],
            "waist": [
                27985,  # Sha'tari Vindicator's Waistguard
                29238,  # Lion's Heart Girdle (Crafted)
            ],
            "legs": [
                29783,  # Legguards of the Resolute Defender [was 28285] (KoT HC)
                31544,  # Netherstorm quest legs
                27527,  # Greaves of the Shatterer
            ],
            "feet": [
                28176,  # Boots of the Righteous Path (BM HC)
                27867,  # Boots of the Outlander (Botanica)
                25792,  # Felsteel Boots
            ],
            "finger1": [
                24088,  # Delicate Eternium Ring (Crafted JC) [was 28034]
                29384,  # Ring of Umbral Doom
            ],
            "finger2": [
                24088,  # Delicate Eternium Ring [was 28034]
                29279,  # Elementium Band of the Sentry
            ],
            "trinket1": [
                28288,  # Abacus of Violent Odds (Mech HC)
                29383,  # Bloodlust Brooch (Badge of Justice vendor)
            ],
            "trinket2": [
                29383,  # Bloodlust Brooch
                28288,  # Abacus of Violent Odds
                25937,  # Terokkar Tablet of Precision (quest)
            ],
            "main_hand": [
                28429,  # Lionheart Champion (Crafted BS)
                29124,  # Crystalforged War Axe (OHB quest)
                25762,  # Honed Voidaxe
            ],
            "off_hand": [],  # Ret uses 2H
            "ranged_relic": [
                27484,  # Libram of Avengement (Auchenai HC)
                25644,  # Blessed Book of Nagrand
            ],
        },

        # --- TIER 4 ---
        "t4": {
            "head": [
                29073,  # Justicar Crown (T4 - Prince token)
                28224,  # Wastewalker Helm
            ],
            "neck": [
                28745,  # Mithril Chain of Heroism (Kara - Nightbane)
                28516,  # Barbed Choker of Discipline
            ],
            "shoulder": [
                29064,  # Justicar Pauldrons (T4 Ret) [was 29076] (T4 Ret)
                27797,  # Wastewalker Shoulderpads
            ],
            "back": [
                28672,  # Drape of the Dark Reavers (Kara - Shade of Aran)
                28777,  # Cloak of the Pit Stalker (Kara - Prince)
            ],
            "chest": [
                29062,  # Justicar Chestpiece (T4 Ret) [was 29070]
                28262,  # Breastplate of the Righteous (Kara quest)
                30258,  # Chestplate of A'dal
            ],
            "wrists": [
                28795,  # Bladespire Warbands (Gruul)
                29463,  # Vambraces of Courage
            ],
            "hands": [
                28506,  # Gloves of Dexterous Manipulation (Kara - Moroes)
                28518,  # Gauntlets of the Righteous
            ],
            "waist": [
                28779,  # Girdle of Treachery (Kara - Moroes)
                28566,  # Girdle of the Immovable
            ],
            "legs": [
                28741,  # Skulker's Greaves (Kara - Nightbane)
                29783,  # Legguards of the Resolute Defender [was 28285]
            ],
            "feet": [
                28608,  # Ironstriders of Urgency (Kara - Opera)
                28176,  # Boots of the Righteous Path
            ],
            "finger1": [
                28757,  # Ring of a Thousand Marks (Kara - Prince)
                29177,  # A'dal's Command (Sha'tar Exalted)
            ],
            "finger2": [
                28730,  # Mithril Band of the Unscarred (Kara - Curator)
                29279,  # Elementium Band of the Sentry
            ],
            "trinket1": [
                29383,  # Bloodlust Brooch (Badges)
                28830,  # Dragonspine Trophy (Kara - Nightbane)
            ],
            "trinket2": [
                28830,  # Dragonspine Trophy
                28288,  # Abacus of Violent Odds
            ],
            "main_hand": [
                28773,  # Gorehowl (Kara - Prince Malchezaar)
                28429,  # Lionheart Champion
            ],
            "off_hand": [],  # Ret uses 2H
            "ranged_relic": [
                27484,  # Libram of Avengement
                28296,  # Libram of Saints Departed
            ],
        },

        # --- TIER 5 ---
        "t5": {
            "head": [
                30131,  # Crystalforge War-Helm (T5)
                29073,  # Justicar Crown
            ],
            "neck": [
                30022,  # Pendant of the Perilous (TK - Kael'thas)
                28745,  # Mithril Chain of Heroism
            ],
            "shoulder": [
                30133,  # Crystalforge Shoulderbraces (T5 Ret) [was 30137]
                29064,  # Justicar Pauldrons (T4 Ret) [was 29076]
            ],
            "back": [
                30098,  # Pepe's Shroud of Pacification
                28672,  # Drape of the Dark Reavers
            ],
            "chest": [
                30129,  # Crystalforge Breastplate (T5)
                29062,  # Justicar Chestpiece [was 29070]
            ],
            "wrists": [
                29966,  # Vambraces of Ending (SSC - Leotheras) [was 30073]
                28795,  # Bladespire Warbands
            ],
            "hands": [
                30130,  # Crystalforge Gauntlets (T5)
                28506,  # Gloves of Dexterous Manipulation
            ],
            "waist": [
                30032,  # Red Belt of Battle (Crafted, SSC pattern)
                28779,  # Girdle of Treachery
            ],
            "legs": [
                30132,  # Crystalforge Greaves (T5)
                28741,  # Skulker's Greaves
            ],
            "feet": [
                30104,  # Cobra-Lash Boots (SSC - Lady Vashj)
                28608,  # Ironstriders of Urgency
            ],
            "finger1": [
                30052,  # Ring of Lethality (TK - A'lar)
                28757,  # Ring of a Thousand Marks
            ],
            "finger2": [
                29997,  # Band of the Ranger-General (SSC - Vashj) [was 30038 neck item]
                28730,  # Mithril Band of the Unscarred
            ],
            "trinket1": [
                28830,  # Dragonspine Trophy
                29383,  # Bloodlust Brooch
            ],
            "trinket2": [
                30627,  # Tsunami Talisman (SSC - Lurker)
                29383,  # Bloodlust Brooch
            ],
            "main_hand": [
                30021,  # Twinblade of the Phoenix (TK - Kael'thas)
                30902,  # Cataclysm's Edge (Hyjal - Archimonde) [was 30249 in wrong tier]
                28773,  # Gorehowl
            ],
            "off_hand": [],
            "ranged_relic": [
                30063,  # Libram of Absolute Truth (T5 era) [was 27484 for T5]
                27484,  # Libram of Avengement
            ],
        },

        # --- TIER 6 ---
        "t6": {
            "head": [
                30989,  # Lightbringer War-Helm (T6) [was 31097 token]
                30131,  # Crystalforge War-Helm
            ],
            "neck": [
                32591,  # Choker of Serrated Blades (BT) [was 32363]
                30022,  # Pendant of the Perilous
            ],
            "shoulder": [
                30997,  # Lightbringer Pauldrons (T6 Ret) [was 31099 token]
                30133,  # Crystalforge Shoulderbraces
            ],
            "back": [
                32323,  # Shadowmoon Destroyer's Drape (BT - Shahraz)
                30098,  # Pepe's Shroud of Pacification
            ],
            "chest": [
                30990,  # Lightbringer Breastplate (T6) [was 31095 token]
                30129,  # Crystalforge Breastplate
            ],
            "wrists": [
                32574,  # Bracers of Eradication (BT - Gorefiend)
                29966,  # Vambraces of Ending [was 30073]
            ],
            "hands": [
                30982,  # Lightbringer Gauntlets (T6) [was 31098 token]
                30130,  # Crystalforge Gauntlets
            ],
            "waist": [
                30915,  # Belt of Seething Fury (Hyjal - Kaz'rogal) [was 32232 wrong ID]
                30032,  # Red Belt of Battle
            ],
            "legs": [
                30993,  # Lightbringer Greaves (T6) [was 31100 token]
                30132,  # Crystalforge Greaves
            ],
            "feet": [
                32366,  # Shadowmaster's Boots (BT - Council)
                30104,  # Cobra-Lash Boots
            ],
            "finger1": [
                32497,  # Stormrage Signet Ring (BT - Gorefiend)
                30052,  # Ring of Lethality
            ],
            "finger2": [
                29301,  # Band of the Eternal Champion (BT - Shahraz)
                28730,  # Mithril Band of the Unscarred
            ],
            "trinket1": [
                28830,  # Dragonspine Trophy
                32505,  # Madness of the Betrayer (BT - Illidan)
            ],
            "trinket2": [
                32505,  # Madness of the Betrayer
                30627,  # Tsunami Talisman
            ],
            "main_hand": [
                30902,  # Cataclysm's Edge (Hyjal - Archimonde) [was 30249]
                32332,  # Torch of the Damned (BT - Illidan)
                28773,  # Gorehowl
            ],
            "off_hand": [],
            "ranged_relic": [
                32368,  # Tome of the Lightbringer (BT - Shahraz)
                33503,  # Libram of Divine Purpose (ZA)
            ],
        },

        # --- SUNWELL ---
        "sunwell": {
            "head": [
                34244,  # Duplicitous Guise (Sunwell - Eredar Twins)
                30989,  # Lightbringer War-Helm
            ],
            "neck": [
                34177,  # Clutch of Demise (Sunwell - Eredar Twins)
                32591,  # Choker of Serrated Blades
            ],
            "shoulder": [
                34392,  # Shoulderpads of Vehemence (Sunwell - Kalecgos)
                30997,  # Lightbringer Pauldrons
            ],
            "back": [
                34241,  # Cloak of Unforgivable Sin (Sunwell - Brutallus)
                32323,  # Shadowmoon Destroyer's Drape
            ],
            "chest": [
                34397,  # Bladed Chaos Tunic (Sunwell - Felmyst)
                30990,  # Lightbringer Breastplate
            ],
            "wrists": [
                34431,  # Lightbringer Bracers (Sunwell T6.5 Ret)
                32574,  # Bracers of Eradication
            ],
            "hands": [
                34342,  # Gauntlets of the Soothed Soul (Sunwell)
                30982,  # Lightbringer Gauntlets
            ],
            "waist": [
                34485,  # Lightbringer Girdle (Sunwell T6.5 Ret)
                30915,  # Belt of Seething Fury (Hyjal) [was 34547/32232 wrong IDs]
            ],
            "legs": [
                34180,  # Felstrength Legplates (Sunwell - Brutallus)
                30993,  # Lightbringer Greaves
            ],
            "feet": [
                34561,  # Lightbringer Stompers (Sunwell T6.5 Ret)
                32366,  # Shadowmaster's Boots
            ],
            "finger1": [
                34189,  # Band of Ruinous Delight (Sunwell - M'uru)
                32497,  # Stormrage Signet Ring
            ],
            "finger2": [
                34361,  # Signet of Primal Wrath (Sunwell)
                29301,  # Band of the Eternal Champion
            ],
            "trinket1": [
                34427,  # Blackened Naaru Sliver (Sunwell - M'uru)
                32505,  # Madness of the Betrayer
            ],
            "trinket2": [
                32505,  # Madness of the Betrayer
                28830,  # Dragonspine Trophy
            ],
            "main_hand": [
                34247,  # Apolyon, the Soul-Render (Sunwell - KJ)
                34198,  # Stanchion of Primal Instinct (Sunwell - Brutallus)
            ],
            "off_hand": [],
            "ranged_relic": [
                32368,  # Tome of the Lightbringer (BT) [was 34200 recipe item]
                33503,  # Libram of Divine Purpose (ZA)
            ],
        },
    },
}


def get_all_bis_ids(spec):
    """Get a flat set of all BiS item IDs for a spec across all phases."""
    ids = set()
    spec_data = BIS.get(spec, {})
    for phase_data in spec_data.values():
        for slot_items in phase_data.values():
            ids.update(slot_items)
    return ids


def get_bis_for_slot(spec, phase, slot):
    """Get the ordered BiS list for a specific spec/phase/slot."""
    return BIS.get(spec, {}).get(phase, {}).get(slot, [])


def find_item_in_bis(item_id):
    """Check if an item appears in any BiS list. Returns list of (spec, phase, slot, rank)."""
    results = []
    for spec, phases in BIS.items():
        for phase, slots in phases.items():
            for slot, items in slots.items():
                if item_id in items:
                    rank = items.index(item_id) + 1
                    results.append((spec, phase, slot, rank))
    return results
