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



if __name__ == "__main__":
    create_group_relationships_table(spc.DB_NAME)