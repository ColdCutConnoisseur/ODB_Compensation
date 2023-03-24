import unittest

import psycopg2

from sales_person_attribs_crud import (connect_to_db,
                                       create_sales_person_attributes_table,
                                       create_or_update_attributes_record,
                                       retrieve_attributes_record)
import sales_people_config as spc

class DBOperationsTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Connecting to test database and creating test table...")
        test_db_name = spc.TEST_DB_NAME
        create_sales_person_attributes_table(test_db_name)

    def setUp(self):
        self.test_db_name = spc.TEST_DB_NAME

    @classmethod
    def tearDownClass(cls):
        test_db_name = spc.TEST_DB_NAME
        conn = connect_to_db(test_db_name)
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE sales_person_attribs;")
        
        conn.commit()
        cur.close()
        conn.close()

        
    def test_default_args_create_attrib_record(self):
        sales_person_id = "3fhtyerj-khfhka-09-jfhak"

        create_or_update_attributes_record(self.test_db_name, sales_person_id,
            preacculynx_job_count=0, has_recruit=False, rewards_tier_overwrite=None)

        returned_record = retrieve_attributes_record(self.test_db_name, sales_person_id)

        should_be_tuple = ("3fhtyerj-khfhka-09-jfhak", 0, False, None)

        self.assertEqual(should_be_tuple, returned_record)

    def test_query_nonexistent_id_is_none(self):
        sales_person_id = "h8fhyrid-9djr8737-fjjie8-98j"

        returned_record = retrieve_attributes_record(self.test_db_name, sales_person_id)

        self.assertEqual(None, returned_record)

    def test_overwrite_job_count(self):
        sales_person_id = "3fhtyerj-khfhka-09-jfhak"

        create_or_update_attributes_record(self.test_db_name, sales_person_id,
            preacculynx_job_count=48, has_recruit=False, rewards_tier_overwrite=None)

        returned_record = retrieve_attributes_record(self.test_db_name, sales_person_id)

        should_be_tuple = ("3fhtyerj-khfhka-09-jfhak", 48, False, None)

        self.assertEqual(should_be_tuple, returned_record)

    def test_overwrite_has_recruit(self):
        sales_person_id = "3fhtyerj-khfhka-09-jfhak"

        create_or_update_attributes_record(self.test_db_name, sales_person_id,
            preacculynx_job_count=48, has_recruit=True, rewards_tier_overwrite=None)

        returned_record = retrieve_attributes_record(self.test_db_name, sales_person_id)

        should_be_tuple = ("3fhtyerj-khfhka-09-jfhak", 48, True, None)

        self.assertEqual(should_be_tuple, returned_record)


    def test_overwrite_tier_overwrite(self):
        sales_person_id = "3fhtyerj-khfhka-09-jfhak"

        create_or_update_attributes_record(self.test_db_name, sales_person_id,
            preacculynx_job_count=48, has_recruit=False, rewards_tier_overwrite="Tier 4")

        returned_record = retrieve_attributes_record(self.test_db_name, sales_person_id)

        should_be_tuple = ("3fhtyerj-khfhka-09-jfhak", 48, False, "Tier 4")

        self.assertEqual(should_be_tuple, returned_record)


    
        
if __name__ == "__main__":
    unittest.main()