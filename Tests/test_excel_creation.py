import unittest
import Frontend.Input.excel_creation as excel

class TestExcelDAOCreation(unittest.TestCase):
    def setUp(self):
        # Clear state before each test
        excel.dao_creation_steps.clear()
        excel.daos.clear()
        self.session_id = "testsession"

    def test_excel_set_dao_name(self):
        result = excel.excel_set_dao_name(self.session_id, "TestDAO")
        self.assertIn("DAO name set to 'TestDAO'", result)
        self.assertIn(self.session_id, excel.dao_creation_steps)
        self.assertEqual(excel.dao_creation_steps[self.session_id]["name"], "TestDAO")
        print("The test_excel_set_dao_name has passed successfully!")
        print(f"Session: {self.session_id}, DAO name: {excel.dao_creation_steps[self.session_id]['name']}")

    def test_excel_set_num_founders(self):
        excel.excel_set_dao_name(self.session_id, "TestDAO")
        result = excel.excel_set_num_founders(self.session_id, 2)
        self.assertIn("Number of founders set to 2", result)
        self.assertEqual(excel.dao_creation_steps[self.session_id]["num_founders"], 2)
        self.assertEqual(excel.dao_creation_steps[self.session_id]["founders"], [])
        print("The test_excel_set_num_founders has passed successfully!")
        print(f"Session: {self.session_id}, Num founders: {excel.dao_creation_steps[self.session_id]['num_founders']}")

    def test_excel_add_founder(self):
        excel.excel_set_dao_name(self.session_id, "TestDAO")
        excel.excel_set_num_founders(self.session_id, 2)
        result1 = excel.excel_add_founder(self.session_id, "Mihail")
        self.assertIn("Founder 'Mihail' added", result1)
        result2 = excel.excel_add_founder(self.session_id, "Ben")
        self.assertIn("All founders added", result2)
        self.assertEqual(excel.dao_creation_steps[self.session_id]["founders"], ["Mihail", "Ben"])
        print("The test_excel_add_founder has passed successfully!")
        print(f"Session: {self.session_id}, Founders: {excel.dao_creation_steps[self.session_id]['founders']}")

    def test_excel_set_token_and_supply(self):
        excel.excel_set_dao_name(self.session_id, "TestDAO")
        excel.excel_set_num_founders(self.session_id, 1)
        excel.excel_add_founder(self.session_id, "Mihail")
        result = excel.excel_set_token_and_supply(self.session_id, "REVO", 1000000)
        self.assertIn("Token 'REVO' and initial supply 1000000 set", result)
        self.assertEqual(excel.dao_creation_steps[self.session_id]["token_name"], "REVO")
        self.assertEqual(excel.dao_creation_steps[self.session_id]["initial_supply"], 1000000)
        print("The test_excel_set_token_and_supply has passed successfully!")
        print(f"Session: {self.session_id}, Token: {excel.dao_creation_steps[self.session_id]['token_name']}, Initial supply: {excel.dao_creation_steps[self.session_id]['initial_supply']}")

    def test_excel_finalize_dao(self):
        excel.excel_set_dao_name(self.session_id, "TestDAO")
        excel.excel_set_num_founders(self.session_id, 1)
        excel.excel_add_founder(self.session_id, "Mihail")
        excel.excel_set_token_and_supply(self.session_id, "REVO", 1000000)
        result = excel.excel_finalize_dao(self.session_id)
        self.assertIn("DAO created with ID:", result)
        self.assertEqual(len(excel.daos), 1)
        self.assertNotIn(self.session_id, excel.dao_creation_steps)
        print("The test_excel_finalize_dao has passed successfully!")
        print(f"Result: {result}, DAOs: {list(excel.daos.keys())}")

if __name__ == "__main__":
    unittest.main()