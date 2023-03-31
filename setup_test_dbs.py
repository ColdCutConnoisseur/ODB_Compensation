
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


def setup_test_sales_person_attribs_table():
    conn = connect_to_test_db()

    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS sales_person_attribs"+\
               " (SALES_PERSON_ID varchar(255), INITIAL_JOB_COUNT integer,"+\
               " HAS_RECRUIT boolean, REWARDS_TIER_OVERWRITE varchar(255));")

    sql_insert_statements = [
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('dfbcb2a9-3486-462d-92d5-fd8cbc581a79', 81, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('5a3ba0f1-f5e1-4c83-9d0e-cc3b51cb7ee5', 77, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('7d606c2d-4ddd-4404-b11f-1edb39c95b2d', 253, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('516988b2-3032-4f8f-a0be-1b5f42f9c1e4', 68, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('22132f16-522c-4e9b-acb2-4f79aaa319ed', 302, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('b6067bd7-36ea-4114-94ac-76229d3b4d33', 115, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('8354edfd-44b7-438e-a685-6421ce01ec90', 286, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('d52d899b-033d-48a7-9e6e-96e52609e383', 88, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('1dfda72e-10dd-412a-8ed5-309f1be66985', 161, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('afb061a5-c5fa-42eb-a97f-532024b2ac66', 49, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('0a2cf51e-385d-40e9-9915-5d90a0991239', 33, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('c79eec63-f8d3-4240-a6bb-449447f24aa4', 51, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('11898189-ab22-4749-91e4-81eb0f2ccf47', 20, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('b176ed04-ca4e-4b9b-91a1-d9f808265ae9', 21, false, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', 370, true, NULL);",
        "INSERT INTO sales_person_attribs (sales_person_id, initial_job_count, has_recruit, rewards_tier_overwrite) VALUES ('e5e96861-f5a8-41d2-ad5b-b420f3c0d15c', 267, false, 'Tier 4');"
    ]

    for insert_statement in sql_insert_statements:
        cur.execute(insert_statement)

    conn.commit()
    cur.close()
    conn.close()


def create_fake_jobs():
    conn = connect_to_test_db()

    cur = conn.cursor()

    cur.execute("DROP TABLE closed_jobs")

    cur.execute("""CREATE TABLE IF NOT EXISTS closed_jobs
                (
                  JOB_LINK varchar(255),
                  CREATED_DATE timestamp,
                  MILESTONE_DATE timestamp,
                  MODIFIED_DATE timestamp,
                  CURRENT_MILESTONE varchar(255),
                  JOB_NAME varchar(255),
                  JOB_ID varchar(255),
                  JOB_NUMBER int,
                  SALES_PERSON_ID varchar(255),
                  GROUP_LEAD_PAYOUT numeric,
                  LEGACY_LEAD_PAYOUT numeric,
                  PROCESSED_FOR_PAYOUT boolean
                );""")

    sql_insert_statements = [
        "INSERT INTO closed_jobs (job_link, created_date, milestone_date, modified_date, current_milestone, job_name, job_id, job_number, sales_person_id, group_lead_payout, legacy_lead_payout, processed_for_payout) VALUES ('https://api.acculynx.com/api/v2/jobs/1b399c5c-290f-4bd9-88a7-bb705bbdc03e', '2022-09-22 02:46:55', '2023-03-24 18:19:14', '2023-03-24 18:19:14', 'Closed', '5213: Terran & Anthony D''''Andrea', '1b399c5c-290f-4bd9-88a7-bb705bbdc03e', 5213, 'c7e723c3-9fe1-47a4-99dd-ddc6a66448bc', 0.0, 0.0, false);",
        "INSERT INTO closed_jobs (job_link, created_date, milestone_date, modified_date, current_milestone, job_name, job_id, job_number, sales_person_id, group_lead_payout, legacy_lead_payout, processed_for_payout) VALUES ('https://api.acculynx.com/api/v2/jobs/1b399c5c-290f-4bd9-88a7-bb705bbdhu47', '2022-09-22 02:46:55', '2023-03-24 18:19:14', '2023-03-24 18:19:14', 'Closed', '5214: Marco Pancelli', '1b399c5c-290f-4bd9-88a7-bb705bbdhu47', 5214, 'e5e96861-f5a8-41d2-ad5b-b420f3c0d15c', 0.0, 0.0, false);",
         "INSERT INTO closed_jobs (job_link, created_date, milestone_date, modified_date, current_milestone, job_name, job_id, job_number, sales_person_id, group_lead_payout, legacy_lead_payout, processed_for_payout) VALUES ('https://api.acculynx.com/api/v2/jobs/0j87hc5c-290f-4bd9-88a7-bb705bbjke5e', '2022-09-22 02:46:55', '2023-03-24 18:19:14', '2023-03-24 18:19:14', 'Closed', '5222: Bert Squibert', '0j87hc5c-290f-4bd9-88a7-bb705bbjke5e', 5222, '4799f346-8358-42b8-9c52-2728137a49f3', 0.0, 0.0, false);"
    ]

    for insert_statement in sql_insert_statements:
        cur.execute(insert_statement)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    #setup_test_group_relationships_table()
    #setup_test_sales_person_attribs_table()
    create_fake_jobs()