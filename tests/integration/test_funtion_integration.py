import unittest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from function_app import app
from azure.functions import HttpRequest

class TestFunctionIntegration(unittest.TestCase):
    """Integration tests for Azure Functions"""
    
    def test_http_trigger_integration(self):
        """Integration test simulating real HTTP request"""
        # Create a real HttpRequest object
        req = HttpRequest(
            method='GET',
            url='http://localhost:7071/api/http_trigger',
            params={'name': 'IntegrationTest'},
            body=None,
            headers={}
        )
        
        response = app.http_trigger(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, IntegrationTest', response.get_body().decode())
    
    def test_http_trigger_post_integration(self):
        """Test POST request with JSON body"""
        req = HttpRequest(
            method='POST',
            url='http://localhost:7071/api/http_trigger',
            params={},
            body=json.dumps({'name': 'PostUser'}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        response = app.http_trigger(req)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, PostUser', response.get_body().decode())
    
    def test_command_endpoint_safe(self):
        """Test the safe command endpoint"""
        req = HttpRequest(
            method='GET',
            url='http://localhost:7071/api/test_command',
            params={'input': 'safeinput'},
            body=None,
            headers={}
        )
        
        response = app.test_command(req)
        
        # Should return 200 for valid input
        self.assertEqual(response.status_code, 200)
        self.assertIn('Command output', response.get_body().decode())
    
    def test_command_endpoint_unsafe(self):
        """Test command endpoint with unsafe input"""
        req = HttpRequest(
            method='GET',
            url='http://localhost:7071/api/test_command',
            params={'input': 'test;rm -rf /'},  # Try injection
            body=None,
            headers={}
        )
        
        response = app.test_command(req)
        
        # Should return 400 for invalid input
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_body().decode())

if __name__ == '__main__':
    unittest.main()