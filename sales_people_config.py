
import os

class ReturnTypes:
    RecordAlreadyExists = 'RecordAlreadyExists'

# DB Stuff
DB_NAME = "ODB_DB"
HOST = "localhost"
PGS_USER = "postgres"
PASSWORD = os.environ['PGS_PW']

# DB Tables
TABLE_NAME = "sales_people"

# Testing
TEST_DB_NAME = "test_odb"

# Rewards Tiers
class ProgramTiers:
    TIER_1A = "Tier 1a"
    TIER_1B = "Tier 1b"
    TIER_1C = "Tier 1c"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"
    TIER_4 = "Tier 4"
    TIER_5 = "Tier 5"
    TIER_6 = "Tier 6"

    TIER_OPTIONS = ["N/A", "Tier 1a", "Tier 1b", "Tier 1c", "Tier 2",
                    "Tier 3", "Tier 4", "Tier 5", "Tier 6"]

    TIER_PAYOUTS = {
        "Tier 1a" : [0.15, 0.05],
        "Tier 1b" : [0.15, 0.05],
        "Tier 1c" : [0.15, 0.05],
        "Tier 2"  : [0.10, 0.05],
        "Tier 3"  : [0.10, 0.05],
        "Tier 4"  : [0.10, 0.05],
        "Tier 5"  : [0.05, 0.00]
    }
