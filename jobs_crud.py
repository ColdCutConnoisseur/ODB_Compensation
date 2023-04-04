"""Handle CRUD operations for handling closed jobs


closed_jobs db table used for finding newly closed jobs and for employee job counts

"""


import psycopg2

from acculynx_api_interface import (get_all_closed_jobs,
                                    get_all_closed_jobs_since_observe_date,
                                    get_all_closed_jobs_short_date_range,
                                    retrieve_representative_for_job_by_job_id)
import sales_people_config as spc



def connect_to_db(database_name):
    """Connect to database and return the connection"""
    db_creds = f"host={spc.HOST} dbname={database_name} user={spc.PGS_USER} password={spc.PASSWORD}"
    conn = psycopg2.connect(db_creds)
    return conn


def create_closed_jobs_table(database_name):
    """Create initial 'closed_jobs' table if it doesn't exist"""
    conn = connect_to_db(database_name)
    cur = conn.cursor()

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
                  GROUP_LEAD_ID varchar(255),
                  GROUP_LEAD_PAYOUT numeric,
                  LEGACY_LEAD_ID varchar(255),
                  LEGACY_LEAD_PAYOUT numeric,
                  PROCESSED_FOR_PAYOUT boolean
                );""")
    
    conn.commit()
    cur.close()
    conn.close()


def return_all_job_ids_in_database(database_name):
    """Fetch all existing job ids from database table"""
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    cur.execute("""SELECT JOB_ID FROM closed_jobs""")

    all_job_ids = cur.fetchall()
    all_job_ids = [list(item)[0] for item in all_job_ids]
    
    conn.commit()
    cur.close()
    conn.close()

    return all_job_ids


def run_initial_setup_for_closed_jobs_table(database_name):
    """Used for setup--populate initial table with all 'closed' jobs from Acculynx API"""
    create_closed_jobs_table(database_name)

    all_job_ids = return_all_job_ids_in_database(database_name)
    
    # Fetch all closed jobs from Acculynx API
    # closed_jobs_per_acculynx = get_all_closed_jobs()
    closed_jobs_per_acculynx = get_all_closed_jobs_since_observe_date()

    # Compare against 'all_job_ids' to see which jobs need to be added
    filtered_new_jobs = [j for j in closed_jobs_per_acculynx if j.job_id not in all_job_ids]

    print(f"Num new jobs since last call: {len(filtered_new_jobs)}")

    insert_sql_statement = """INSERT INTO closed_jobs (
                              JOB_LINK,
                              CREATED_DATE,
                              MILESTONE_DATE,
                              MODIFIED_DATE,
                              CURRENT_MILESTONE,
                              JOB_NAME,
                              JOB_ID,
                              JOB_NUMBER,
                              SALES_PERSON_ID,
                              GROUP_LEAD_ID,
                              GROUP_LEAD_PAYOUT,
                              LEGACY_LEAD_ID,
                              LEGACY_LEAD_PAYOUT,
                              PROCESSED_FOR_PAYOUT
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    # Connect to DB
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    # Then for filtered jobs, retrieve and attach associated sales person to job
    for unhandled_job in filtered_new_jobs:
        current_job_id = unhandled_job.job_id
        print(f"Fetching representative for {current_job_id}...")

        sales_person_data = retrieve_representative_for_job_by_job_id(current_job_id)
        sales_person_id = sales_person_data['user']['id']
        unhandled_job.sales_person_id = sales_person_id

        # Append job tuple to statement
        job_args = [unhandled_job.job_link, unhandled_job.created_date,
                    unhandled_job.milestone_date, unhandled_job.modified_date,
                    unhandled_job.current_milestone, unhandled_job.job_name,
                    unhandled_job.job_id, unhandled_job.job_number,
                    unhandled_job.sales_person_id, None, None, None, None, False]

        cur.execute(insert_sql_statement, job_args)

    conn.commit()
    cur.close()
    conn.close()


def update_jobs_table(database_name):
    run_initial_setup_for_closed_jobs_table(database_name)


def clear_jobs_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    cur.execute("""TRUNCATE TABLE closed_jobs;""")

    conn.commit()
    cur.close()
    conn.close()


def drop_jobs_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    cur.execute("""DROP TABLE closed_jobs;""")

    conn.commit()
    cur.close()
    conn.close()
    

# QUERYING
def return_all_closed_jobs_count_for_employee(database_name, employee_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    count_query = """SELECT COUNT(JOB_ID) FROM closed_jobs
                     WHERE sales_person_id = %s"""

    cur.execute(count_query, [employee_id])

    closed_jobs_count = list(cur.fetchone())[0]

    cur.close()
    conn.close()

    return closed_jobs_count

def return_all_closed_and_processed_jobs_count_for_employee(database_name, employee_id, existing_conn=None):
    if existing_conn:
        conn = existing_conn

    else:
        conn = connect_to_db(database_name)

    cur = conn.cursor()

    count_query = """SELECT COUNT(JOB_ID) FROM closed_jobs
                     WHERE sales_person_id = %s
                       AND PROCESSED_FOR_PAYOUT = %s"""

    cur.execute(count_query, [employee_id, True])

    closed_and_processed_jobs_count = list(cur.fetchone())[0]

    cur.close()

    if not existing_conn:
        conn.close()

    return closed_and_processed_jobs_count

def find_newly_closed_jobs(database_name):
    all_job_ids = return_all_job_ids_in_database(database_name)
    
    # Fetch all closed jobs from Acculynx API
    closed_jobs_per_acculynx = get_all_closed_jobs_short_date_range()

    # Compare against 'all_job_ids' to see which jobs need to be added
    filtered_new_jobs = [j for j in closed_jobs_per_acculynx if j.job_id not in all_job_ids]

    return filtered_new_jobs

def return_unprocessed_jobs(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    unprocessed_jobs_query = """SELECT JOB_NUMBER, SALES_PERSON_ID FROM closed_jobs
                                WHERE PROCESSED_FOR_PAYOUT = %s"""

    cur.execute(unprocessed_jobs_query, [False])

    unprocessed_jobs = [list(tup) for tup in cur.fetchall()]

    cur.close()
    conn.close()

    return unprocessed_jobs

def update_job_as_processed(database_name, job_number, group_lead_id,
            group_lead_payout_amount, legacy_lead_id, legacy_lead_payout_amount):
    job_number = int(job_number)

    conn = connect_to_db(database_name)
    cur = conn.cursor()

    update_job_statement = """UPDATE closed_jobs
                              SET GROUP_LEAD_ID = %s, GROUP_LEAD_PAYOUT = %s, LEGACY_LEAD_ID = %s, 
                              LEGACY_LEAD_PAYOUT = %s, PROCESSED_FOR_PAYOUT = %s
                              WHERE JOB_NUMBER = %s"""

    cur.execute(update_job_statement, [group_lead_id, group_lead_payout_amount, legacy_lead_id, legacy_lead_payout_amount, True, job_number])

    conn.commit()
    cur.close()
    conn.close()



if __name__ == "__main__":
    # drop_jobs_table(spc.DB_NAME)
    run_initial_setup_for_closed_jobs_table(spc.DB_NAME)
    