
import sys

import psycopg2

import sales_people_config as spc
from acculynx_api_interface import get_all_company_users


def update_sales_people_table(database_name):
    """Make sure that 'sales_people' table is current.  If it doesn't exist, create"""
    db_creds = f"host={spc.HOST} dbname={database_name} user={spc.PGS_USER} password={spc.PASSWORD}"

    conn = psycopg2.connect(db_creds)
    cur = conn.cursor()

    cur.execute(f"CREATE TABLE IF NOT EXISTS sales_people (ID varchar(255), FULLNAME varchar(255));")
    cur.execute(f"SELECT * FROM sales_people;")

    records = cur.fetchall()

    users = get_all_company_users()

    user_ids_in_db = []

    if records:
        user_id_idx = 0
        user_ids_in_db = [list(rec)[user_id_idx] for rec in records]

    if users:
        for user_id, user_name in users.items():

            # Check if user_id already exists in db
            if user_id in user_ids_in_db:
                print(f"User_id <{user_id}> already exists in following db table: sales_people")

            else:
                # Insert (if not present already)
                print("ID not present in db table")
                print(f"Adding record [ {user_id} , {user_name} ] into sales_people table...")
                cur.execute(f"INSERT INTO sales_people VALUES (%s, %s);", (user_id, user_name))
                print("Record added!")

    else:
        print("No users returned in 'update_sales_people_table' call")

    conn.commit()
    cur.close()
    conn.close()


def return_sales_people_ids_and_names_as_dict(database_name):
    db_creds = f"host={spc.HOST} dbname={database_name} user={spc.PGS_USER} password={spc.PASSWORD}"

    conn = psycopg2.connect(db_creds)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM sales_people;")

    records_list = cur.fetchall()

    as_lists = [list(item) for item in records_list]

    as_dict = {item[1] : item[0] for item in as_lists}

    return as_dict


if __name__ == "__main__":
    DATABASE = spc.DB_NAME
    
    update_sales_people_table(DATABASE)