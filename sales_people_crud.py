
import sys

import psycopg2

import sales_people_config as spc
from acculynx_api_interface import get_all_company_users


def update_sales_people_table():
    """Make sure that 'sales_people' table is current.  If it doesn't exist, create"""
    db_creds = f"host={spc.HOST} dbname={spc.DB_NAME} user={spc.PGS_USER} password={spc.PASSWORD}"

    conn = psycopg2.connect(db_creds)
    cur = conn.cursor()

    # cur.execute(f"DROP TABLE {spc.TABLE_NAME}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {spc.TABLE_NAME} (ID varchar(255), FULLNAME varchar(255));")
    cur.execute(f"SELECT * FROM {spc.TABLE_NAME};")

    records = cur.fetchall()
    #print(f"Fetched records: {records}")
    #print("Company Users per Acculynx:\n")

    users = get_all_company_users()

    user_ids_in_db = []

    if records:
        user_id_idx = 0
        user_ids_in_db = [list(rec)[user_id_idx] for rec in records]

    if users:
        for user_id, user_name in users.items():

            # Check if user_id already exists in db
            if user_id in user_ids_in_db:
                print(f"User_id <{user_id}> already exists in following db table: {spc.TABLE_NAME}")

            else:
                # Insert (if not present already)
                print("ID not present in db table")
                print(f"Adding record [ {user_id} , {user_name} ] into {spc.TABLE_NAME} table...")
                cur.execute(f"INSERT INTO {spc.TABLE_NAME} VALUES (%s, %s);", (user_id, user_name))
                print("Record added!")

    else:
        print("No users returned in 'update_sales_people_table' call")

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    update_sales_people_table()