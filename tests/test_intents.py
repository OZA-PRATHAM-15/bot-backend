import unittest
from intents.analytics import get_top_products, get_hover_overview, get_zero_hovers

class TestAnalyticsIntents(unittest.TestCase):
    def test_get_top_products(self):
        result = get_top_products()
        self.assertTrue("1." in result)

    def test_get_hover_overview(self):
        result = get_hover_overview()
        self.assertIn("Total hovers recorded", result)

    def test_get_zero_hovers(self):
        result = get_zero_hovers()
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
