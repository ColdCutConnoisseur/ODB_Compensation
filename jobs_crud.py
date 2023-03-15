"""Handle CRUD operations for handling closed jobs


closed_jobs db table used for finding newly closed jobs and for employee job counts

"""


import psycopg2

from acculynx_api_interface import (get_all_closed_jobs,
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
                  SALES_PERSON_ID varchar(255)
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
    closed_jobs_per_acculynx = get_all_closed_jobs()

    # Compare against 'all_job_ids' to see which jobs need to be added
    filtered_new_jobs = [j for j in closed_jobs_per_acculynx if j.job_id not in all_job_ids]

    combined_sql_statement = """INSERT INTO closed_jobs (JOB_LINK, CREATED_DATE,
                              MILESTONE_DATE,
                              MODIFIED_DATE,
                              CURRENT_MILESTONE,
                              JOB_NAME,
                              JOB_ID,
                              JOB_NUMBER,
                              SALES_PERSON_ID
                            )
                            VALUES """

    # Then for filtered jobs, retrieve and attach associated sales person to job
    debug_counter = 0
    for unhandled_job in filtered_new_jobs:
        sales_person_data = retrieve_representative_for_job_by_job_id(unhandled_job.job_id)
        sales_person_id = sales_person_data['user']['id']
        unhandled_job.sales_person_id = sales_person_id

        # Append job tuple to statement
        job_tuple = f"""('{unhandled_job.job_link}', '{unhandled_job.created_date}', 
                         '{unhandled_job.milestone_date}', '{unhandled_job.modified_date}',
                         '{unhandled_job.current_milestone}', '{unhandled_job.job_name}',
                         '{unhandled_job.job_id}', '{unhandled_job.job_number}',
                         '{unhandled_job.sales_person_id}'),"""

        combined_sql_statement += job_tuple

        print(f"Handling unhandled job #{debug_counter}")
        debug_counter += 1

    if len(filtered_new_jobs) > 0:
        revised_sql_statement = combined_sql_statement[:-1]
        revised_sql_statement += ';'

        conn = connect_to_db(database_name)
        cur = conn.cursor()

        cur.execute(revised_sql_statement)

        conn.commit()
        cur.close()
        conn.close()


def clear_jobs_table(database_name):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    cur.execute("""TRUNCATE TABLE closed_jobs;""")

    conn.commit()
    cur.close()
    conn.close()
    

# QUERYING
def return_closed_jobs_count_for_employee(database_name, employee_id):
    conn = connect_to_db(database_name)
    cur = conn.cursor()

    count_query = """SELECT COUNT(JOB_ID) FROM closed_jobs
                     WHERE sales_person_id = %s"""

    cur.execute(count_query, [employee_id])

    closed_jobs_count = list(cur.fetchone())[0]

    conn.commit()
    cur.close()
    conn.close()

    return closed_jobs_count

def find_newly_closed_jobs(database_name):
    all_job_ids = return_all_job_ids_in_database(database_name)
    
    # Fetch all closed jobs from Acculynx API
    closed_jobs_per_acculynx = get_all_closed_jobs_short_date_range()

    # Compare against 'all_job_ids' to see which jobs need to be added
    filtered_new_jobs = [j for j in closed_jobs_per_acculynx if j.job_id not in all_job_ids]

    return filtered_new_jobs

if __name__ == "__main__":
    run_initial_setup_for_closed_jobs_table(spc.DB_NAME)
    