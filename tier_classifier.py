"""NOTE: You will have to add in logic / functionality for overwritten promotions"""



import sales_people_config as spc


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



def revise_compensation_tier_based_on_overwrite():
    """FUTURE ADD-IN: Make sure that the comp tier is at minimum the overwritten level"""
    pass

