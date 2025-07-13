import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_webhook(self):
        response = self.client.post('/bot-api/webhook', json={
            "queryResult": {
                "intent": {"displayName": "What are the top products"},
                "queryText": "What are the top products"
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("fulfillmentText", response.json)

if __name__ == "__main__":
    unittest.main()
