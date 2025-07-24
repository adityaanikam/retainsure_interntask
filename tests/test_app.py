import unittest
import json
import sys
import os

# Add the parent directory to the path to import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class UserApiTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize the database."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "User Management System")

    def test_get_all_users(self):
        """Test fetching all users."""
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('john@example.com', response.data.decode('utf-8'))

    def test_create_user(self):
        """Test creating a new user."""
        new_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "newpassword"
        }
        response = self.app.post('/users',
                                 data=json.dumps(new_user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['message'], 'User created')
        self.assertIn('user_id', response_data)

    def test_login_success(self):
        """Test a successful login."""
        login_credentials = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.app.post('/login',
                                 data=json.dumps(login_credentials),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['status'], 'success')

    def test_login_failure(self):
        """Test a failed login with a wrong password."""
        login_credentials = {
            "email": "john@example.com",
            "password": "wrongpassword"
        }
        response = self.app.post('/login',
                                 data=json.dumps(login_credentials),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['status'], 'failed')

if __name__ == '__main__':
    unittest.main()