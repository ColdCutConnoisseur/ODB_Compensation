


import unittest


from acculynx_api_interface import Job, retrieve_representative_for_job_by_job_id
from jobs_crud import connect_to_db, create_closed_jobs_table
import sales_people_config as spc

class TestJob(unittest.TestCase):


    def setUp(self):
        create_closed_jobs_table(spc.TEST_DB_NAME)
        
        data_dict = {'_link' : 'holder',
                     'createdDate' : 'holder',
                     'milestoneDate' : 'holder',
                     'modifiedDate' : 'holder',
                     'currentMilestone' : 'holder',
                     'jobName' : "651: Patty O'Connel",
                     'id' : 'holder',
                     'jobNumber' : 'holder'}

        self.sample_job = Job(data_dict)

    def test_insert_escape(self):
        self.assertEqual(self.sample_job.job_name, "651: Patty O''Connel")

    
    def test_insert_into_db_table(self):
        filtered_new_jobs = [self.sample_job]

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
            # sales_person_data = retrieve_representative_for_job_by_job_id(unhandled_job.job_id)
            # sales_person_id = sales_person_data['user']['id']
            unhandled_job.sales_person_id = "TEST_ID"

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

            conn = connect_to_db(spc.TEST_DB_NAME)
            cur = conn.cursor()

            cur.execute(revised_sql_statement)

            conn.commit()
            cur.close()
            conn.close()



if __name__ == "__main__":
    unittest.main()