
import psycopg2

import sales_people_config as spc

def connect_to_test_db():
    db_creds = f"host={spc.HOST} dbname={spc.TEST_DB_NAME} user={spc.PGS_USER} password={spc.PASSWORD}"
    conn = psycopg2.connect(db_creds)
    return conn

def setup_test_group_relationships_table():
    conn = connect_to_test_db()

    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS group_relationships"+\
               " (SALES_PERSON_ID varchar(255), GROUP_LEAD_ID varchar(255),"+\
               " LEGACY_GROUP_LEAD_ID varchar(255));")

    sql_insert_statements = [
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('bb86c952-224d-4a6e-8718-e9468ea3308f', '1dfda72e-10dd-412a-8ed5-309f1be66985', '22132f16-522c-4e9b-acb2-4f79aaa319ed');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('1cd4b2ec-3660-4a45-8251-497aaaf5d546', '1dfda72e-10dd-412a-8ed5-309f1be66985', '22132f16-522c-4e9b-acb2-4f79aaa319ed');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('ecb9301b-e3d4-4795-9a88-1fde54341e65', '1dfda72e-10dd-412a-8ed5-309f1be66985', '22132f16-522c-4e9b-acb2-4f79aaa319ed');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('1dfda72e-10dd-412a-8ed5-309f1be66985', '22132f16-522c-4e9b-acb2-4f79aaa319ed', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('0a2cf51e-385d-40e9-9915-5d90a0991239', '22132f16-522c-4e9b-acb2-4f79aaa319ed', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('dfbcb2a9-3486-462d-92d5-fd8cbc581a79', '22132f16-522c-4e9b-acb2-4f79aaa319ed', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('6e47dfc0-55cc-4d3d-aed7-c63312aa3c02', '22132f16-522c-4e9b-acb2-4f79aaa319ed', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('4799f346-8358-42b8-9c52-2728137a49f3', '5a3ba0f1-f5e1-4c83-9d0e-cc3b51cb7ee5', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('22132f16-522c-4e9b-acb2-4f79aaa319ed', NULL, NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', NULL, NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('5a3ba0f1-f5e1-4c83-9d0e-cc3b51cb7ee5', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('e5e96861-f5a8-41d2-ad5b-b420f3c0d15c', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('82519346-0397-479b-a543-0c62dfc4987c', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('afb061a5-c5fa-42eb-a97f-532024b2ac66', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', NULL);",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('f23f08f2-2b27-4151-9ac1-5d4536127518', '7d606c2d-4ddd-4404-b11f-1edb39c95b2d', '8354edfd-44b7-438e-a685-6421ce01ec90');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('7d606c2d-4ddd-4404-b11f-1edb39c95b2d', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('b6067bd7-36ea-4114-94ac-76229d3b4d33', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('516988b2-3032-4f8f-a0be-1b5f42f9c1e4', '8354edfd-44b7-438e-a685-6421ce01ec90', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('c2f90791-6668-45c3-a425-c5616f851231', '516988b2-3032-4f8f-a0be-1b5f42f9c1e4', '8354edfd-44b7-438e-a685-6421ce01ec90');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('65f9340f-3b7f-4cc7-a06e-36f04b1b2653', 'c79eec63-f8d3-4240-a6bb-449447f24aa4', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('b176ed04-ca4e-4b9b-91a1-d9f808265ae9', 'c79eec63-f8d3-4240-a6bb-449447f24aa4', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('11898189-ab22-4749-91e4-81eb0f2ccf47', 'c79eec63-f8d3-4240-a6bb-449447f24aa4', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc');",
        "INSERT INTO group_relationships (sales_person_id, group_lead_id, legacy_group_lead_id) VALUES ('c79eec63-f8d3-4240-a6bb-449447f24aa4', 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', NULL);",
    ]

    for insert_statement in sql_insert_statements:
        cur.execute(insert_statement)

    conn.commit()
    cur.close()
    conn.close()


def setup_test_group_relationships_table():
    conn = connect_to_test_db()

    cur = conn.cursor()


if __name__ == "__main__":
    #setup_test_group_relationships_table()
    pass