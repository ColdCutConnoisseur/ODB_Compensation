
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
# DEPR GROUPS_TABLE_NAME = "group_relationships"

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
