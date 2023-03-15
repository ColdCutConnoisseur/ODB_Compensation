"""Main module for Acculynx API interactions


get_jobs() --> returns dict in form {'count': 108, 'pageSize': 25, 'pageStartIndex': 0, 'items': [<job_json>, ...]




Current considerations:
    Job classifications like: 'inspection' (obviously don't want this counted towards the job count, correct?)

    note for above: 
    
              {'workType':   {
                              '_link': 'https://api.acculynx.com/api/v2/work-types/6',
                              'categoryId': 6,
                              'name':       'Inspection'
                              }
               }

    Are jobs linked to managers / knockers / etc by 'contact'?
        - If so....

        [ ] Create 'contact' mapping of id / hash to 'name'

        ** No, it's not linked through 'contact' (it's 'users' endpoint)






TODO:  Zero financials -- still count as job count / do not sort out by gross profit margin

       -- These old jobs had 'cross reference' codes including 'IN, WI, IL'
"""

import sys
import pprint

import requests
from requests.auth import AuthBase


from acculynx_config import ACCULYNX_API_KEY, ACCULYNX_API_BASE_URL, DEF_NUM_RESULTS

class AcculynxAuth(AuthBase):
    def __init__(self):
        pass

    def __call__(self, r):
        r.headers = {
            'Authorization' : 'Bearer ' + ACCULYNX_API_KEY,
            'Content-Type'  : 'application/json'
        }
        return r
        

class Job:
    def __init__(self, data_dict):
        self.job_link = data_dict['_link']
        self.created_date = data_dict['createdDate']
        self.milestone_date = data_dict['milestoneDate']
        self.modified_date = data_dict['modifiedDate']
        self.current_milestone = data_dict['currentMilestone']
        self.job_name = data_dict['jobName']
        self.job_id = data_dict['id']
        self.job_number = data_dict['jobNumber']
        self.sales_person_id = None


def DEPRget_jobs():
    endpoint = "/jobs"

    parameters = {
        'pageSize' : 25,
        'pageStartIndex' : 0,
        'startDate' : '2023-01-01',
        'endDate' : '2023-07-07',
        'dateFilterType' : 'MilestoneDate',
        'milestones' : 'closed',
    }

    r = requests.get(ACCULYNX_API_BASE_URL + endpoint, params=parameters, auth=AcculynxAuth())

    if r.status_code == 200:
        as_json = r.json()
        return as_json

    else:
        print("Bad return in call to 'get_jobs'")
        return {}




def DEPRget_job_by_id(job_id):
    link = f'https://api.acculynx.com/api/v2/jobs/{job_id}'

    r = requests.get(link, auth=AcculynxAuth())

    if r.status_code == 200:
        as_json = r.json()
        return as_json

    else:
        print("Bad return in call to 'get_job_by_id_test'")
        return {}


def DEPRtest_retrieve_contact():
    link = 'https://api.acculynx.com/api/v2/contacts/a0d456dd-ff53-ea11-9115-0cc47aa3a68a'

    r = requests.get(link, auth=AcculynxAuth())

    if r.status_code == 200:
        as_json = r.json()
        return as_json

    else:
        print("Bad return in call to 'get_job_by_id_test'")
        return {}


def retrieve_representative_for_job_by_job_id(job_id):
    link = f'https://api.acculynx.com/api/v2/jobs/{job_id}/representatives/company'
    r = requests.get(link, auth=AcculynxAuth())

    if r.status_code == 200:
        as_json = r.json()
        return as_json

    else:
        print("Bad return in call to 'get_job_by_id_test'")
        return {}



def follow_link():
    # GOOD CALL FOR GETTING REP NAME
    link = 'https://api.acculynx.com/api/v2/users/e5e96861-f5a8-41d2-ad5b-b420f3c0d15c'

    r = requests.get(link, auth=AcculynxAuth())

    if r.status_code == 200:
        as_json = r.json()
        return as_json

    else:
        print("Bad return in call to 'get_job_by_id_test'")
        return {}



def get_all_company_users():
    endpoint = '/users'

    results_counter = 0
    results = {}

    should_call = True

    while should_call:
        parameters = {
            'pageSize' : DEF_NUM_RESULTS,
            'pageStartIndex' : results_counter,
        }

        r = requests.get(ACCULYNX_API_BASE_URL + endpoint, params=parameters, auth=AcculynxAuth())

        if r.status_code == 200:
            as_json = r.json()

            # Combine results in 'results' dict
            result_items = as_json['items']
            user_ids_and_names = {item['id'] : item['displayName'] for item in result_items}

            results.update(user_ids_and_names)

            results_counter += DEF_NUM_RESULTS

            num_results_per_api = as_json['count']

            if results_counter >= num_results_per_api:
                assert len(list(results.keys())) == int(num_results_per_api), "Incorrect amount of 'Users' pulled!"
                return results

        else:
            print("Bad return in call to 'get_job_by_id_test'")
            return results

def get_all_closed_jobs_short_date_range():
    """Purpose of this is less overhead per call once most jobs already exist within database table"""
    endpoint = "/jobs"

    results_counter = 0
    results = []

    should_call = True

    while should_call:

        # NOTE: Maybe filter after date in which ODB started using Acculynx?

        parameters = {
            'pageSize' : DEF_NUM_RESULTS,
            'pageStartIndex' : results_counter,
            'startDate' : '2023-03-01',
            'dateFilterType' : 'MilestoneDate',
            'milestones' : 'closed'
        }

        r = requests.get(ACCULYNX_API_BASE_URL + endpoint, params=parameters, auth=AcculynxAuth())

        if r.status_code == 200:
            as_json = r.json()

            # Combine results in 'results' dict
            result_items = as_json['items']
            addl_jobs = [Job(item) for item in result_items]

            results += addl_jobs                                             # NOTE: Dupe checking?

            results_counter += DEF_NUM_RESULTS

            num_results_per_api = as_json['count']

            if results_counter >= num_results_per_api:
                assert len(results) == int(num_results_per_api), "Incorrect amount of 'Closed Jobs' pulled!"
                return results

        else:
            print("Bad return in call to 'get_all_closed_jobs'")
            return []

def get_all_closed_jobs():
    endpoint = "/jobs"

    results_counter = 0
    results = []

    should_call = True

    while should_call:

        # NOTE: Maybe filter after date in which ODB started using Acculynx?

        parameters = {
            'pageSize' : DEF_NUM_RESULTS,
            'pageStartIndex' : results_counter,
            'milestones' : 'closed',
        }

        r = requests.get(ACCULYNX_API_BASE_URL + endpoint, params=parameters, auth=AcculynxAuth())

        if r.status_code == 200:
            as_json = r.json()

            # Combine results in 'results' dict
            result_items = as_json['items']
            addl_jobs = [Job(item) for item in result_items]

            results += addl_jobs                                             # NOTE: Dupe checking?

            results_counter += DEF_NUM_RESULTS

            num_results_per_api = as_json['count']

            if results_counter >= num_results_per_api:
                assert len(results) == int(num_results_per_api), "Incorrect amount of 'Closed Jobs' pulled!"
                return results

        else:
            print("Bad return in call to 'get_all_closed_jobs'")
            return []


if __name__ == "__main__":
    pprint.PrettyPrinter(indent=4)
    
    all_closed_jobs = get_all_closed_jobs()
    pprint.pprint(all_closed_jobs)
