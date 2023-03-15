
import os

# DB Stuff
DB_NAME = "ODB_DB"
HOST = "localhost"
PGS_USER = "postgres"
PASSWORD = os.environ['PGS_PW']

# DB Tables
TABLE_NAME = "sales_people"
# DEPR GROUPS_TABLE_NAME = "group_relationships"

# Testing
TEST_DB_NAME = "ODB_TEST"



class ReturnTypes:
    RecordAlreadyExists = 'RecordAlreadyExists'