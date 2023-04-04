"""Functionality for returning current Rewards Program Tier for contractors"""

import sales_people_config as spc
from sales_person_attribs_crud import return_contractor_rewards_tier_overwrite

def return_reward_tier_for_sales_person(num_closed_contractor_jobs, num_closed_team_jobs, has_direct_recruit):
    """Given num closed personal / team jobs, return the appropriate comp tier"""
    if (num_closed_contractor_jobs >= 150) and (num_closed_team_jobs >= 1000) and (has_direct_recruit):
        return spc.ProgramTiers.TIER_6

    elif (num_closed_contractor_jobs >= 125) and (num_closed_team_jobs >= 500) and (has_direct_recruit):
        return spc.ProgramTiers.TIER_5

    elif (num_closed_contractor_jobs >= 100) and (num_closed_team_jobs >= 250) and (has_direct_recruit):
        return spc.ProgramTiers.TIER_4

    elif (num_closed_contractor_jobs >= 50) and (num_closed_team_jobs >= 100) and (has_direct_recruit):
        return spc.ProgramTiers.TIER_3

    elif num_closed_contractor_jobs >= 20:
        return spc.ProgramTiers.TIER_2

    elif num_closed_contractor_jobs >= 10:
        return spc.ProgramTiers.TIER_1C

    elif num_closed_contractor_jobs >= 5:
        return spc.ProgramTiers.TIER_1B

    else:
        return spc.ProgramTiers.TIER_1A



def revise_compensation_tier_based_on_overwrite(database_name, contractor_id, num_closed_contractor_jobs,
            num_closed_team_jobs, has_direct_recruit, existing_conn=None):
    """Make sure that the comp tier is at minimum the overwritten level (if one exists)"""
    natural_tier = return_reward_tier_for_sales_person(num_closed_contractor_jobs,
                                                        num_closed_team_jobs, has_direct_recruit)

    if not existing_conn:
        contractor_overwrite = return_contractor_rewards_tier_overwrite(database_name, contractor_id)

    else:
        contractor_overwrite = return_contractor_rewards_tier_overwrite(database_name, contractor_id, existing_conn=existing_conn)

    if contractor_overwrite is None:
        return natural_tier

    else:
        return_tier = natural_tier

        # Comparison
        natural_index = spc.ProgramTiers.TIER_OPTIONS.index(natural_tier)
        overwrite_index = spc.ProgramTiers.TIER_OPTIONS.index(contractor_overwrite)

        if overwrite_index > natural_index:
            return_tier = contractor_overwrite

        return return_tier


