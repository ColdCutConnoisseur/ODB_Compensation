
# ODB Jobs / Comp Summary




## Production Setup
4 Tables

Table1 -- Sales person to group leads relationships (sales_group_relationships_crud.py)

Table2 -- Sales person ID --> Sales person Name (sales_people_crud.py)

Table3 -- Sales person ID --> Num Jobs Completed [current state]

Table4 -- Completed Jobs [Find new jobs / just completed to process] (jobs_crud.py)



We'll setup Table2 first.  Make sure that 'ODB_DB' database is created in pgAdmin.

[ ] create utility script for Table 4  (currently just run run_initial_setup_for_closed_jobs_table(DB_NAME) in jobs_crud.py).  This pulls all closed jobs from Acculynx and throws it in a database table.  




## Testing

Table1 tests --> test_group_relationships.py

Table2 tests --> NOT CREATED YET



## TODO
NOTE: Maybe filter after date in which ODB started using Acculynx? (get all jobs call in api_interface.py)

TODO:  Zero financials -- still count as job count / do not sort out by gross profit margin

       -- These old jobs had 'cross reference' codes including 'IN, WI, IL' (from acculynx_api)


## Considerations
[ ] Only allow create_new group_relationship if 'sales_person_id' exists in sales_people table.
[ ] Check to see if there are further filters to apply to closed jobs before counting them.