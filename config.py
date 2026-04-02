# config.py - Paths and character configuration

import os

# Path to the TBC item database SQL dumps
DB_PATH = r"C:\Users\danie\Downloads\burning-crusade-item-db-main"

# Character configuration
CHARACTER = {
    "name": "Danduvil",
    "server": "Dreamscythe",
    "region": "US",
    "faction": "Alliance",
    "race_id": 2,
    "level": 69,
    "class": "PALADIN",
    "main_spec": "prot",
    "off_spec": "ret",
}

# Danduvil's AMR export string
AMR_EXPORT = (
    "$50;US;Dreamscythe;Danduvil;;1;2;69;0:0;1;"
    ".s1;PALADIN;5000000000000000000005310000000000000000000523005130033125331051;"
    ".q1;25589s1;13s6;26s13;16s18;118s16;152s2;13s15;10s14;1796s12;2053s8;472s5;9s10;8s3;77s9;1167s7;8s11;"
    ".inv;2901;4047;1099;2261;207;630;1239;266;4406;0;1532;2589;700;696;5;846;76;921;54;27;"
    "490f41;7f36;56f36;152f5;226;609;1459;353;1;2;420;178;514;192;286;647;131e1883;105;197;194;64;24;177;"
    "122;7;29;293;229;4;2;1;1;1;79;57;1;140;152913;88285$"
)

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
