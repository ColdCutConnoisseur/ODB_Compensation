

from decimal import Decimal

from sales_person_attribs_crud import return_contractor_initial_job_count, return_contractor_has_direct_recruit
from sales_group_relationships_crud import return_team_ids_for_counting_team_jobs
from jobs_crud import return_all_closed_and_processed_jobs_count_for_employee
from tier_classifier import revise_compensation_tier_based_on_overwrite

import gui_config
import sales_people_config as spc


def fetch_current_job_count_for_contractor(database_name, contractor_id):
    """This will be all initial jobs + jobs deemed 'closed' and 'processed'"""

    # Fetch initial job count from 'sales_person_attribs' table
    initial_job_count = return_contractor_initial_job_count(database_name, contractor_id)

    processed_jobs_count =\
        return_all_closed_and_processed_jobs_count_for_employee(database_name, contractor_id)

    return initial_job_count + processed_jobs_count

def fetch_team_job_count(database_name, contractor_id):
    """"""
    team_ids = return_team_ids_for_counting_team_jobs(database_name, contractor_id)

    total_team_jobs = 0
    
    for con_id in team_ids:

        count_for_id = fetch_current_job_count_for_contractor(database_name, con_id)

        total_team_jobs += count_for_id

    return total_team_jobs



def DEPRcalculate_reward_payouts_for_job(is_job_eligible, database_name, group_lead_id, legacy_lead_id, job_gross_profit):
    """
    

    Args:
        is_job_eligible (bool): is the job eligible for 'rewards' split?
        job_gross_profit (float): 
        group_lead_id (str): team group lead id -- used for split % lookup
        legacy_lead_id (str): team legacy lead id -- used for split % lookup
    """

    group_lead_payout = 0
    legacy_lead_payout = 0

    if not is_job_eligible:
        return [group_lead_payout, legacy_lead_payout]

    # Job is eligible for 'rewards'
    elif is_job_eligible:

        if group_lead_id is not None:

            group_lead_job_count = fetch_current_job_count_for_contractor(database_name, group_lead_id)

            group_lead_team_job_count = fetch_team_job_count(database_name, group_lead_id)

            group_lead_has_recruit = return_contractor_has_direct_recruit(database_name, group_lead_id)

            group_lead_tier = revise_compensation_tier_based_on_overwrite(
                                        database_name,
                                        group_lead_id,
                                        group_lead_job_count,
                                        group_lead_team_job_count,
                                        group_lead_has_recruit
            )

            group_lead_split_percent = spc.ProgramTiers.TIER_PAYOUTS[group_lead_tier][0]

            group_lead_payout = Decimal(job_gross_profit) * Decimal(group_lead_split_percent)

        if legacy_lead_id is not None:

            legacy_lead_job_count = fetch_current_job_count_for_contractor(database_name, legacy_lead_id)

            legacy_lead_team_job_count = fetch_team_job_count(database_name, legacy_lead_id)

            legacy_lead_has_recruit = return_contractor_has_direct_recruit(database_name, legacy_lead_id)

            legacy_lead_tier = revise_compensation_tier_based_on_overwrite(
                                        database_name,
                                        legacy_lead_id,
                                        legacy_lead_job_count,
                                        legacy_lead_team_job_count,
                                        legacy_lead_has_recruit
            )

            legacy_lead_split_percent = spc.ProgramTiers.TIER_PAYOUTS[legacy_lead_tier][1]

            legacy_lead_payout = Decimal(job_gross_profit) * Decimal(legacy_lead_split_percent)

        return [group_lead_payout, legacy_lead_payout]
