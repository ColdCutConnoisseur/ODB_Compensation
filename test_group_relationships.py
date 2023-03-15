"""
    
CONSIDERATIONS: 
    
    [ ] Only allow create_new if 'sales_person_id' exists in sales_people table


"""

import unittest

import psycopg2

from sales_group_relationships_crud import (connect_to_db,
                                            create_group_relationships_table,
                                            create_new_relationship,
                                            retrieve_group_relationship_by_sales_person,
                                            update_group_relationship,
                                            delete_group_relationship)
import sales_people_config as spc

class DBOperationsTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Connecting to test database and creating test table...")
        test_db_name = "test_odb"
        create_group_relationships_table(test_db_name)


    def setUp(self):
        self.database_name = "test_odb"
        

    def test_create_new_relationship_no_group_lead_no_legacy_lead(self):
        test_sales_person_id = "11898189-ab22-4749-91e4-81eb0f2ccf47"
        create_new_relationship(self.database_name, test_sales_person_id)

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, None, None)

        self.assertEqual(expected, retrieval)


    def test_create_new_relationship_no_group_lead(self):
        test_sales_person_id = "2a28ea6e-df8a-454c-8e63-1a18b8a28478"
        test_legacy_lead_id = "5a58b9b9-ea61-4c42-ba9d-c4de53d29b2e"
        create_new_relationship(self.database_name, test_sales_person_id, legacy_lead_id=test_legacy_lead_id)

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, None, test_legacy_lead_id)

        self.assertEqual(expected, retrieval)


    def test_create_new_relationship_record_already_exists(self):
        test_sales_person_id = "2a28ea6e-df8a-454c-8e63-1a18b8a28478"
        test_group_lead_id = "5a58b9b9-ea61-4c42-ba9d-c4de53d29b2e"
        result = create_new_relationship(self.database_name, test_sales_person_id, group_lead_id=test_group_lead_id)

        self.assertEqual(result, spc.ReturnTypes.RecordAlreadyExists)


    def test_create_new_relationship_no_legacy_lead(self):
        test_sales_person_id = "65f9340f-3b7f-4cc7-a06e-36f04b1b2653"
        test_group_lead_id = "5a58b9b9-ea61-4c42-ba9d-c4de53d29b2e"
        create_new_relationship(self.database_name, test_sales_person_id, group_lead_id=test_group_lead_id)

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, test_group_lead_id, None)

        self.assertEqual(expected, retrieval)


    def test_create_new_relationship_all_data_provided(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"
        test_group_lead_id = "63f6ce1d-41d4-462f-b58b-6ebeaa272983"
        test_legacy_lead_id = "0a2cf51e-385d-40e9-9915-5d90a0991239"
        create_new_relationship(self.database_name, test_sales_person_id, test_group_lead_id, test_legacy_lead_id)

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, test_group_lead_id, test_legacy_lead_id)

        self.assertEqual(expected, retrieval)


    def test_record_retrieval(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"
        retrieval = retrieve_group_relationship_by_sales_person(self.database_name, test_sales_person_id)

        test_group_lead_id = "63f6ce1d-41d4-462f-b58b-6ebeaa272983"
        test_legacy_lead_id = "0a2cf51e-385d-40e9-9915-5d90a0991239"

        expected = (test_sales_person_id, test_group_lead_id, test_legacy_lead_id)

        self.assertEqual(retrieval, expected)


    def test_record_update_nullify_group_lead_and_legacy(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"

        revised_group_lead_id = None
        revised_legacy_lead_id = None

        update_group_relationship(
                    self.database_name,
                    test_sales_person_id,
                    group_lead_id=revised_group_lead_id,
                    legacy_lead_id=revised_legacy_lead_id
                    )

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, revised_group_lead_id, revised_legacy_lead_id)

        self.assertEqual(retrieval, expected)


    def test_record_update_set_group_lead(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"

        revised_group_lead_id = "ecb9301b-e3d4-4795-9a88-1fde54341e65"
        revised_legacy_lead_id = None

        update_group_relationship(
                    self.database_name,
                    test_sales_person_id,
                    group_lead_id=revised_group_lead_id,
                    legacy_lead_id=revised_legacy_lead_id
                    )

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, revised_group_lead_id, revised_legacy_lead_id)

        self.assertEqual(retrieval, expected)


    def test_record_update_set_legacy_lead(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"

        revised_group_lead_id = None
        revised_legacy_lead_id = "0a2cf51e-385d-40e9-9915-5d90a0991239"

        update_group_relationship(
                    self.database_name,
                    test_sales_person_id,
                    group_lead_id=revised_group_lead_id,
                    legacy_lead_id=revised_legacy_lead_id
                    )

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, revised_group_lead_id, revised_legacy_lead_id)

        self.assertEqual(retrieval, expected)


    def test_record_update_both_group_lead_and_legacy(self):
        test_sales_person_id = "8354edfd-44b7-438e-a685-6421ce01ec90"

        revised_group_lead_id = "afb061a5-c5fa-42eb-a97f-532024b2ac66"
        revised_legacy_lead_id = "f0e81b04-add2-4ff4-a1bb-0d5adc32455b"

        update_group_relationship(
                    self.database_name,
                    test_sales_person_id,
                    group_lead_id=revised_group_lead_id,
                    legacy_lead_id=revised_legacy_lead_id
                    )

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        expected = (test_sales_person_id, revised_group_lead_id, revised_legacy_lead_id)

        self.assertEqual(retrieval, expected)


    def test_delete_record(self):
        test_sales_person_id = "c79eec63-f8d3-4240-a6bb-449447f24aa4"
        create_new_relationship(self.database_name, test_sales_person_id)
        delete_group_relationship(self.database_name, test_sales_person_id)

        conn = connect_to_db(self.database_name)
        cur = conn.cursor()

        cur.execute("""SELECT * FROM group_relationships
                       WHERE SALES_PERSON_ID = %s;
                    """, [test_sales_person_id])
        retrieval = cur.fetchone()
        cur.close()
        conn.close()

        self.assertEqual(None, retrieval)


    @classmethod
    def tearDownClass(cls):
        test_db_name = "test_odb"

        conn = connect_to_db(test_db_name)
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE group_relationships;")
        
        conn.commit()
        cur.close()
        conn.close()




if __name__ == "__main__":
    unittest.main()