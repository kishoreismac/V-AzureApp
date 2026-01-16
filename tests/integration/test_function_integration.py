import os
import unittest
import requests

class TestPostDeployHTTP(unittest.TestCase):
    def test_http_trigger_live(self):
        url = os.environ["FUNCTION_URL"]
        r = requests.get(url, timeout=20)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Hello, IntegrationTest", r.text)

if __name__ == "__main__":
    unittest.main()
