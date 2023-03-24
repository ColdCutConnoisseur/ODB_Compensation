"""Handle CRUD operations for handling sales person attribs, i.e. jobCount, hasRecruit, tierOverwrite, etc"""


import psycopg2

import sales_people_config as spc


def connect_to_db(database_name):
    """Connect to database and return the connection"""
    db_creds = f"host={spc.HOST} dbname={database_name} user={spc.PGS_USER} password={spc.PASSWORD}"
    conn = psycopg2.connect(db_creds)
    return conn

def create_sales_person_attributes_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sales_person_attribs"+\
               " (SALES_PERSON_ID varchar(255), INITIAL_JOB_COUNT integer,"+\
               " HAS_RECRUIT boolean, REWARDS_TIER_OVERWRITE varchar(255));")
    
    conn.commit()
    cur.close()
    conn.close()

def drop_sales_person_attributes_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("DROP TABLE sales_person_attribs;")
    
    conn.commit()
    cur.close()
    conn.close()

def retrieve_attributes_record(database_name, sales_person_id):
    conn = connect_to_db(database_name)

    cur = conn.cursor()

    query = "SELECT * FROM sales_person_attribs " +\
            "WHERE SALES_PERSON_ID = %s"

    cur.execute(query, [sales_person_id])

    returned_record = cur.fetchone()

    cur.close()
    conn.close()

    return returned_record

def create_or_update_attributes_record(database_name, sales_person_id,
            initial_job_count=0, has_recruit=False, rewards_tier_overwrite=None):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    # First check if sales_person_id in database table
    existing_record = retrieve_attributes_record(database_name, sales_person_id)

    # If doesn't exist, add
    if existing_record is None:

        sql_statement = """INSERT INTO sales_person_attribs (SALES_PERSON_ID,
                           INITIAL_JOB_COUNT, HAS_RECRUIT, REWARDS_TIER_OVERWRITE)
                           VALUES (%s, %s, %s, %s)"""

        cur.execute(sql_statement, [sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite])

    # Otherwise, update
    elif existing_record:

        sql_statement = "UPDATE sales_person_attribs "+\
                        "SET INITIAL_JOB_COUNT=%s, HAS_RECRUIT=%s, REWARDS_TIER_OVERWRITE=%s"

        cur.execute(sql_statement, [initial_job_count, has_recruit, rewards_tier_overwrite])

    conn.commit()
    cur.close()
    conn.close()



# QUERIES
def return_contractor_initial_job_count(database_name, sales_person_id):
    conn = connect_to_db(database_name)

    cur = conn.cursor()

    query = "SELECT INITIAL_JOB_COUNT FROM sales_person_attribs " +\
            "WHERE SALES_PERSON_ID = %s"

    cur.execute(query, [sales_person_id])

    returned_record = cur.fetchone()

    if returned_record is None:
        returned_record = 0

    elif returned_record is not None:
        returned_record = list(returned_record)[0]

    cur.close()
    conn.close()

    return returned_record





if __name__ == "__main__":
    # drop_sales_person_attributes_table(spc.DB_NAME)
    create_sales_person_attributes_table(spc.DB_NAME)
