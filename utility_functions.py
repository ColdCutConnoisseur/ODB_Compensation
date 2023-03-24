



from sales_person_attribs_crud import return_contractor_initial_job_count
from jobs_crud import return_all_closed_and_processed_jobs_count_for_employee







def fetch_current_job_count_for_contractor(database_name, contractor_id):
    """This will be all initial jobs + jobs deemed 'closed' and 'processed'"""

    # Fetch initial job count from 'sales_person_attribs' table
    initial_job_count = return_contractor_initial_job_count(database_name, contractor_id)

    processed_jobs_count =\
        return_all_closed_and_processed_jobs_count_for_employee(database_name, contractor_id)

    return initial_job_count + processed_jobs_count

