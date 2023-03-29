"""Handle CRUD operations for handling group relationships, i.e. sales person, group lead, legacy lead"""


import psycopg2

import sales_people_config as spc


def connect_to_db(database_name):
    """Connect to database and return the connection"""
    db_creds = f"host={spc.HOST} dbname={database_name} user={spc.PGS_USER} password={spc.PASSWORD}"
    conn = psycopg2.connect(db_creds)
    return conn

def create_group_relationships_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS group_relationships"+\
               " (SALES_PERSON_ID varchar(255), GROUP_LEAD_ID varchar(255),"+\
               " LEGACY_GROUP_LEAD_ID varchar(255));")
    
    conn.commit()
    cur.close()
    conn.close()

def create_new_relationship(database_name, sales_person_id, group_lead_id=None, legacy_lead_id=None):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("SELECT SALES_PERSON_ID FROM group_relationships;")

    existing_sales_person_ids = cur.fetchall()
    existing_sales_person_ids = [list(id_)[0] for id_ in existing_sales_person_ids]

    if sales_person_id in existing_sales_person_ids:
        print(f"Group Relationship already exists for {sales_person_id}.")
        print("If you want to change this relationship, use the 'update' functionality.")
        return spc.ReturnTypes.RecordAlreadyExists

    else:
        if not group_lead_id and not legacy_lead_id:
            insert_statement = """INSERT INTO group_relationships (
                                  SALES_PERSON_ID, GROUP_LEAD_ID, LEGACY_GROUP_LEAD_ID) 
                                  VALUES (%s, NULL, NULL);"""
            cur.execute(insert_statement, [sales_person_id])

        elif not group_lead_id and legacy_lead_id:
            insert_statement = """INSERT INTO group_relationships (
                                  SALES_PERSON_ID, GROUP_LEAD_ID, LEGACY_GROUP_LEAD_ID) 
                                  VALUES (%s, NULL, %s);"""
            cur.execute(insert_statement, (sales_person_id, legacy_lead_id))

        elif group_lead_id and not legacy_lead_id:
            insert_statement = """INSERT INTO group_relationships (
                                  SALES_PERSON_ID, GROUP_LEAD_ID, LEGACY_GROUP_LEAD_ID)
                                  VALUES (%s, %s, NULL);"""
            cur.execute(insert_statement, (sales_person_id, group_lead_id))

        else:
            insert_statement = """INSERT INTO group_relationships (
                                  SALES_PERSON_ID, GROUP_LEAD_ID, LEGACY_GROUP_LEAD_ID)
                                  VALUES (%s, %s, %s);"""
            cur.execute(insert_statement, (sales_person_id, group_lead_id, legacy_lead_id))
    
    conn.commit()
    cur.close()
    conn.close()

def retrieve_group_relationship_by_sales_person(database_name, sales_person_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM group_relationships WHERE SALES_PERSON_ID = %s;""", [sales_person_id])
    retrieved_record = cur.fetchone()
    cur.close()
    conn.close()
    return retrieved_record

def update_group_relationship(database_name, sales_person_id, group_lead_id=None, legacy_lead_id=None):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    if not group_lead_id and not legacy_lead_id:
        update_statement = """UPDATE group_relationships
                              SET GROUP_LEAD_ID = NULL, LEGACY_GROUP_LEAD_ID = NULL
                              WHERE SALES_PERSON_ID = %s;"""
        cur.execute(update_statement, [sales_person_id])
            
    elif not group_lead_id and legacy_lead_id:
        update_statement = """UPDATE group_relationships
                              SET GROUP_LEAD_ID = NULL, LEGACY_GROUP_LEAD_ID = %s
                              WHERE SALES_PERSON_ID = %s;"""
        cur.execute(update_statement, (legacy_lead_id, sales_person_id))

    elif group_lead_id and not legacy_lead_id:
        update_statement = """UPDATE group_relationships
                              SET GROUP_LEAD_ID = %s, LEGACY_GROUP_LEAD_ID = NULL
                              WHERE SALES_PERSON_ID = %s;"""
        cur.execute(update_statement, (group_lead_id, sales_person_id))

    else:
        update_statement = """UPDATE group_relationships
                              SET GROUP_LEAD_ID = %s, LEGACY_GROUP_LEAD_ID = %s
                              WHERE SALES_PERSON_ID = %s;"""
        cur.execute(update_statement, (group_lead_id, legacy_lead_id, sales_person_id))

    conn.commit()
    cur.close()
    conn.close()

def delete_group_relationship(database_name, sales_person_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()
    cur.execute("""DELETE FROM group_relationships WHERE SALES_PERSON_ID = %s""", [sales_person_id])
    conn.commit()
    cur.close()
    conn.close()

# QUERIES
def unique_values(input_list):
    unique = list(set(input_list))
    return unique

def fetch_all_people_one_level_down(database_name, sales_person_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    # Query where sales person is legacy_lead
    leg_lead_query = "SELECT GROUP_LEAD_ID FROM group_relationships WHERE LEGACY_GROUP_LEAD_ID = %s;"

    cur.execute(leg_lead_query, [sales_person_id])

    fetched_group_leads = cur.fetchall()

    fetched_group_leads = unique_values([list(tup)[0] for tup in fetched_group_leads])

    # Any relationships where sales_person_id is GROUP_LEAD_ID
    group_lead_query = "SELECT SALES_PERSON_ID FROM group_relationships WHERE GROUP_LEAD_ID = %s;"

    cur.execute(group_lead_query, [sales_person_id])

    fetched_sales_people = cur.fetchall()

    fetched_sales_people = unique_values([list(tup)[0] for tup in fetched_sales_people])

    combined_list = fetched_group_leads + fetched_sales_people

    combined_list = unique_values(combined_list)

    cur.close()
    conn.close()

    return combined_list

def fetch_two_level_relationships(database_name, sales_person_id):
    children = fetch_all_people_one_level_down(database_name, sales_person_id)

    grandchildren = []

    for child in children:
        fetched_grandchildren = fetch_all_people_one_level_down(database_name, child)
        grandchildren += fetched_grandchildren

    # Remove Dupes
    grandchildren = unique_values(grandchildren)
    return [children, grandchildren]

def fetch_sales_person_and_group_lead_where_contractor_is_legacy(database_name, sales_person_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    # Query where sales person id is legacy_lead
    leg_lead_query = "SELECT SALES_PERSON_ID, GROUP_LEAD_ID FROM group_relationships WHERE LEGACY_GROUP_LEAD_ID = %s;"

    cur.execute(leg_lead_query, [sales_person_id])

    fetched_team_ids = cur.fetchall()

    fetched_team_ids = unique_values([list(tup)[0] for tup in fetched_team_ids])

    cur.close()
    conn.close()

    return fetched_team_ids

def fetch_sales_person_where_contractor_is_group_lead(database_name, sales_person_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    # Query where sales person id is group_lead
    group_lead_query = "SELECT SALES_PERSON_ID FROM group_relationships WHERE GROUP_LEAD_ID = %s;"

    cur.execute(group_lead_query, [sales_person_id])

    fetched_team_ids = cur.fetchall()

    fetched_team_ids = unique_values([list(tup)[0] for tup in fetched_team_ids])

    cur.close()
    conn.close()

    return fetched_team_ids

def return_team_ids_for_counting_team_jobs(database_name, sales_person_id):
    as_legacy = fetch_sales_person_and_group_lead_where_contractor_is_legacy(database_name, sales_person_id)
    as_group_lead = fetch_sales_person_where_contractor_is_group_lead(database_name, sales_person_id)

    combined_list = as_legacy + as_group_lead

    combined_list = unique_values(combined_list)

    return combined_list
    

if __name__ == "__main__":
    create_group_relationships_table(spc.DB_NAME)

    # Testing
    c, g = fetch_two_level_relationships(spc.DB_NAME, "c7e723c3-9fe1-47a4-99dd-ddc6a66448bc")

    print(c)
    print(g)
