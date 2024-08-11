import sys
import unittest
sys.path.append("..")
from server.services.menu_item import MenuItem

class TestMenuItem(unittest.TestCase):

    def test_fetch_complete_menu_success(self):
        response = MenuItem.fetch_complete_menu()
        self.assertEqual(response['action'], "FETCH_COMPLETE_MENU")
        self.assertGreater(len(response['data']), 0)
        self.assertEqual(len(response['data'][0]), 6)
        print("All assert passed")

if __name__ == '__main__':
    unittest.main()